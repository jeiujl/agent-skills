#!/usr/bin/env python3
"""Build a dated study plan from a JSON spec. Standard library only.

Handles the parts that are easy to get wrong by hand: real dates and weekdays,
fitting sessions into stated hours, spaced reviews at expanding intervals,
interleaved practice, mock exams before each exam, and juggling several
courses at once.

Usage:
    python3 plan.py spec.json                  # markdown plan to stdout
    python3 plan.py spec.json --csv plan.csv   # also write CSV
    python3 plan.py spec.json --ics plan.ics   # also write a calendar file

Spec (JSON):
{
  "start": "2026-10-27",              # first study day (default: today)
  "session_minutes": 50,              # one focused block
  "start_time": "18:00",              # first block each day (for .ics)
  "break_minutes": 10,                # gap between blocks (for .ics)
  "availability": {"mon": 2, "tue": 1.5, "wed": 2, "thu": 1, "fri": 0.5, "sat": 3, "sun": 3},  # hours
  "blackout": ["2026-10-31"],         # days with no studying
  "buffer_day": "auto",               # weekly catch-up day: "auto" (lightest day), a weekday like "fri", or "none"
  "courses": [
    {"name": "ECON 101", "exam": "2026-12-12", "exam_time": "09:00",
     "topics": [{"name": "Elasticity", "weight": 3, "confidence": 2}]}
  ]
}
weight: 1-3 (exam importance). confidence: 1-5 (5 = solid).
"""

import argparse
import csv
import datetime as dt
import json
import math
import sys

DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
REVIEW_GAPS = [1, 3, 7, 14, 28]  # days after first learning


def d(s):
    return dt.date.fromisoformat(s)


def load(path):
    with open(path) as f:
        spec = json.load(f)
    spec.setdefault("start", dt.date.today().isoformat())
    spec.setdefault("session_minutes", 50)
    spec.setdefault("start_time", "18:00")
    spec.setdefault("break_minutes", 10)
    spec.setdefault("blackout", [])
    spec.setdefault("buffer_day", "auto")
    avail = spec.get("availability") or {k: 2 for k in DAYS}
    spec["availability"] = {k.lower()[:3]: float(v) for k, v in avail.items()}
    for c in spec["courses"]:
        c["exam_date"] = d(c["exam"])
        for t in c["topics"]:
            t.setdefault("weight", 2)
            t.setdefault("confidence", 3)
            t["priority"] = t["weight"] * (6 - t["confidence"])
            # weak, heavy topics get a second learning block
            t["learn_blocks"] = 2 if (t["confidence"] <= 2 and t["weight"] >= 3) else 1
    return spec


def buffer_weekday(spec):
    b = str(spec["buffer_day"]).lower()[:3]
    if b in DAYS:
        return DAYS.index(b)
    if b in ("non", "off", "fal", "0"):
        return None
    open_days = [(h, DAYS.index(k)) for k, h in spec["availability"].items() if h > 0 and k in DAYS]
    return min(open_days)[1] if len(open_days) >= 4 else None  # too few study days to give one up


def capacity(spec, day, idx, buf_wd):
    if day.isoformat() in spec["blackout"]:
        return 0, "blackout"
    near_exam = any(0 < (c["exam_date"] - day).days <= 3 for c in spec["courses"])
    if buf_wd is not None and day.weekday() == buf_wd and idx >= 3 and not near_exam:
        return 0, "buffer"
    hours = spec["availability"].get(DAYS[day.weekday()], 0)
    return int(hours * 60 // spec["session_minutes"]), ""


def build(spec):
    start = d(spec["start"])
    last_exam = max(c["exam_date"] for c in spec["courses"])
    if last_exam <= start:
        sys.exit("All exams are on or before the start date.")

    # per-course state
    for c in spec["courses"]:
        c["learn_queue"] = []
        for t in sorted(c["topics"], key=lambda t: -t["priority"]):
            c["learn_queue"] += [(t, i + 1) for i in range(t["learn_blocks"])]
        c["reviews"] = []          # (due_date, topic)
        c["learned"] = []
        c["mock_done"] = False
        c["minutes"] = 0

    plan, notes = [], []
    buf_wd = buffer_weekday(spec)
    day, idx = start, 0
    while day < last_exam:
        cap, special = capacity(spec, day, idx, buf_wd)
        active = [c for c in spec["courses"] if c["exam_date"] > day]
        if special:
            plan.append({"date": day, "block": "-", "course": "-",
                         "activity": "Catch-up / rest" if special == "buffer" else "Off",
                         "topics": "Finish anything that slipped" if special == "buffer" else ""})
        slots = cap
        blocks_today = []

        def add(course, activity, topics):
            blocks_today.append({"date": day, "course": course["name"], "activity": activity, "topics": topics})
            course["minutes"] += spec["session_minutes"]

        # 1. exam-adjacent fixed items
        for c in active:
            days_left = (c["exam_date"] - day).days
            if days_left == 1 and slots > 0:
                add(c, "Light review", "Formula/definition sheet, flashcards, past mistakes; no new material")
                slots -= 1
            elif days_left in (2, 3) and not c["mock_done"] and slots >= 2:
                add(c, "Mock exam (timed)", "Full practice exam under exam conditions")
                add(c, "Mock exam (timed)", "...continued")
                slots -= 2
                c["mock_done"] = True
                c["reviews"].append((day + dt.timedelta(days=1), {"name": "Mock exam mistakes", "priority": 99}))

        # the night before an exam that course gets only the light review
        busy = [c for c in active if (c["exam_date"] - day).days > 1]

        # 2. spaced reviews that are due (cap at half the day so learning still moves)
        due = sorted(((due, t, c) for c in busy for due, t in c["reviews"] if due <= day),
                     key=lambda x: (x[0], -x[1]["priority"]))
        review_cap = max(1, slots // 2) if slots else 0
        grouped = {}
        for due_d, t, c in due:
            names_so_far = grouped.setdefault(c["name"], (c, []))[1]
            if t["name"] not in names_so_far:
                names_so_far.append(t["name"])
        for name, (c, names) in grouped.items():
            if review_cap <= 0 or slots <= 0:
                break
            chunk = names[:4]
            add(c, "Retrieval review", ", ".join(chunk) + " (closed-book recall, then check)")
            slots -= 1
            review_cap -= 1
            c["reviews"] = [(dd, t) for dd, t in c["reviews"] if not (dd <= day and t["name"] in chunk)]

        # 3. new learning, courses ordered by urgency (remaining blocks per day left)
        while slots > 0:
            cands = [c for c in busy if c["learn_queue"]]  # busy already excludes the night before
            if not cands:
                break
            c = max(cands, key=lambda c: len(c["learn_queue"]) / max(1, (c["exam_date"] - day).days - 3))
            t, part = c["learn_queue"].pop(0)
            label = t["name"] + (f" (part {part}/{t['learn_blocks']})" if t["learn_blocks"] > 1 else "")
            add(c, "Learn", label + " - worked examples, then self-explain")
            slots -= 1
            if part == t["learn_blocks"]:
                c["learned"].append(t)
                for g in REVIEW_GAPS:
                    due_d = day + dt.timedelta(days=g)
                    if due_d < c["exam_date"] - dt.timedelta(days=1):
                        c["reviews"].append((due_d, t))

        # 4. leftover time: interleaved practice across learned topics
        practiced = {}
        while slots > 0:
            pool = [c for c in busy if c["learned"]]
            if not pool:
                break
            # nearest exam first, but spread blocks across courses
            c = min(pool, key=lambda c: (c["exam_date"] - day).days + 4 * practiced.get(c["name"], 0))
            practiced[c["name"]] = practiced.get(c["name"], 0) + 1
            ranked = sorted(c["learned"], key=lambda t: -t["priority"])
            k = (day.toordinal() + len(blocks_today)) % max(1, len(ranked))
            mix = (ranked[k:] + ranked[:k])[:3]
            add(c, "Mixed practice", "Interleaved problems: " + ", ".join(t["name"] for t in mix))
            slots -= 1

        for i, b in enumerate(blocks_today, 1):
            b["block"] = i
            plan.append(b)
        day += dt.timedelta(days=1)
        idx += 1

    for c in spec["courses"]:
        if c["learn_queue"]:
            missing = sorted({t["name"] for t, _ in c["learn_queue"]})
            notes.append(f"{c['name']}: not enough time to first-learn {len(missing)} topic(s): {', '.join(missing)}. "
                         "Add hours, start earlier, or cut low-weight topics.")
        if not c["mock_done"]:
            notes.append(f"{c['name']}: no room for a 2-block mock exam 2-3 days out. Free up a longer evening.")
    return plan, notes


def to_markdown(spec, plan, notes):
    L = ["# Study plan", ""]
    for c in spec["courses"]:
        L.append(f"- **{c['name']}** exam {c['exam_date'].strftime('%a %b %d')}"
                 f"{' ' + c['exam_time'] if c.get('exam_time') else ''}: "
                 f"{round(c['minutes'] / 60, 1)} h planned, {len(c['topics'])} topics")
    total = sum(c["minutes"] for c in spec["courses"]) / 60
    L.append(f"- Total: {round(total, 1)} h in {spec['session_minutes']}-min blocks")
    if notes:
        L += ["", "**Warnings**"] + [f"- {n}" for n in notes]
    L += ["", "| Date | # | Course | Activity | Focus | Done |", "|---|---|---|---|---|---|"]
    for p in plan:
        L.append(f"| {p['date'].strftime('%a %b %d')} | {p['block']} | {p['course']} | {p['activity']} | {p['topics']} | ☐ |")
    return "\n".join(L)


def write_csv(path, plan):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "weekday", "block", "course", "activity", "focus", "done"])
        for p in plan:
            w.writerow([p["date"].isoformat(), p["date"].strftime("%a"), p["block"], p["course"],
                        p["activity"], p["topics"], ""])


def write_ics(path, spec, plan):
    def esc(s):
        return s.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;").replace("\n", "\\n")
    h, m = map(int, spec["start_time"].split(":"))
    step = spec["session_minutes"] + spec["break_minutes"]
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//study-guide-builder//EN", "CALSCALE:GREGORIAN"]
    n = 0
    for p in plan:
        if p["block"] == "-":
            continue
        begin = dt.datetime.combine(p["date"], dt.time(h, m)) + dt.timedelta(minutes=step * (p["block"] - 1))
        end = begin + dt.timedelta(minutes=spec["session_minutes"])
        n += 1
        out += ["BEGIN:VEVENT", f"UID:study-{p['date'].isoformat()}-{p['block']}-{n}@study-guide-builder",
                f"DTSTAMP:{stamp}", f"DTSTART:{begin.strftime('%Y%m%dT%H%M%S')}",
                f"DTEND:{end.strftime('%Y%m%dT%H%M%S')}",
                f"SUMMARY:{esc(p['course'] + ': ' + p['activity'])}", f"DESCRIPTION:{esc(p['topics'])}",
                "END:VEVENT"]
    for c in spec["courses"]:
        out += ["BEGIN:VEVENT", f"UID:exam-{c['name'].replace(' ', '')}-{c['exam']}@study-guide-builder",
                f"DTSTAMP:{stamp}"]
        if c.get("exam_time"):
            eh, em = map(int, c["exam_time"].split(":"))
            b = dt.datetime.combine(c["exam_date"], dt.time(eh, em))
            out += [f"DTSTART:{b.strftime('%Y%m%dT%H%M%S')}",
                    f"DTEND:{(b + dt.timedelta(hours=2, minutes=30)).strftime('%Y%m%dT%H%M%S')}"]
        else:
            out += [f"DTSTART;VALUE=DATE:{c['exam_date'].strftime('%Y%m%d')}"]
        out += [f"SUMMARY:{esc(c['name'] + ' EXAM')}", "END:VEVENT"]
    out.append("END:VCALENDAR")
    with open(path, "w", newline="") as f:
        f.write("\r\n".join(out) + "\r\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("--csv")
    ap.add_argument("--ics")
    a = ap.parse_args()
    spec = load(a.spec)
    plan, notes = build(spec)
    print(to_markdown(spec, plan, notes))
    if a.csv:
        write_csv(a.csv, plan)
    if a.ics:
        write_ics(a.ics, spec, plan)


if __name__ == "__main__":
    main()
