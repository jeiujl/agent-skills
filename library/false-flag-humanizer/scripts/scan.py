#!/usr/bin/env python3
"""Pattern scanner for writing flagged as AI-generated.

NOT an AI detector. It does not estimate a probability or predict any tool's
score. It surfaces the statistical and stylistic features detectors are known
to react to, so a human can read those passages closely.

Usage:
    python3 scan.py essay.txt                 # report
    python3 scan.py essay.docx --json         # machine-readable
    python3 scan.py revised.txt --compare original.txt   # before/after metrics

Accepts .txt, .md, or .docx (stdlib-only extraction). Standard library only.
"""

import argparse
import json
import re
import statistics
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

# ---------------------------------------------------------------- loading

def load_text(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        with zipfile.ZipFile(path) as z:
            root = ET.fromstring(z.read("word/document.xml"))
        paras = []
        for p in root.iter(f"{{{ns['w']}}}p"):
            runs = [t.text or "" for t in p.iter(f"{{{ns['w']}}}t")]
            paras.append("".join(runs))
        return "\n\n".join(x for x in paras if x.strip())
    return path.read_text(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------- splitting

ABBREV = r"(?:e\.g|i\.e|etc|vs|Dr|Mr|Mrs|Ms|Prof|St|Jr|Sr|Fig|al|No|pp|p|vol|ch)"

def split_paragraphs(text):
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

def split_sentences(paragraph):
    # protect common abbreviations, then split on terminal punctuation
    protected = re.sub(rf"\b({ABBREV})\.", lambda m: m.group(1) + "\u0000", paragraph)
    parts = re.split(r"(?<=[.!?])[\"'”’)]?\s+(?=[\"'“‘(]?[A-Z0-9])", protected)
    return [s.replace("\u0000", ".").strip() for s in parts if s.strip()]

def words(s):
    return re.findall(r"[A-Za-z0-9’']+(?:-[A-Za-z0-9]+)*", s)

def line_of(text, offset):
    return text.count("\n", 0, offset) + 1

# ---------------------------------------------------------------- catalogs

PHRASES = {
    "significance inflation": [
        r"stands? as a testament", r"serves? as a (?:reminder|testament)",
        r"(?:a |an )?(?:pivotal|crucial|vital|significant|key) (?:role|moment|turning point)",
        r"plays? an? (?:crucial|vital|pivotal|key|significant|important) role",
        r"marks? a (?:pivotal|significant|major) ", r"turning point",
        r"lasting (?:legacy|impact)", r"cannot be overstated",
        r"in today'?s (?:fast-paced|ever-changing|modern|digital|rapidly evolving) world",
        r"now more than ever", r"rich tapestry", r"tapestry of",
        r"ever-(?:evolving|changing) landscape", r"intricate interplay",
        r"shaping the future", r"pav(?:e|es|ed|ing) the way",
    ],
    "hedge/balance filler": [
        r"it is (?:important|essential|crucial|worth noting) to (?:note|consider|remember|recognize)",
        r"it'?s (?:important|worth) (?:to note|noting)", r"it is worth noting",
        r"one could argue", r"it can be argued", r"has (?:both )?(?:its )?(?:benefits|advantages) and (?:drawbacks|disadvantages)",
        r"both sides have", r"a double-edged sword",
    ],
    "vague attribution": [
        r"(?:experts|scholars|researchers|critics|historians|many people|some people|many) (?:argue|believe|suggest|agree|note|have noted|say)",
        r"studies (?:show|have shown|suggest|indicate)", r"research (?:shows|suggests|indicates|has shown)",
        r"it is (?:widely|commonly|generally) (?:believed|accepted|known)",
    ],
    "template signposting": [
        r"in this (?:essay|paper|report),? (?:I|we) will", r"this (?:essay|paper) (?:will|aims to) (?:explore|discuss|examine)",
        r"^in conclusion", r"\bto sum up\b", r"\bin summary\b", r"as we move forward", r"only time will tell",
        r"brighter future", r"challenges and (?:future )?(?:prospects|opportunities|outlook)",
    ],
    "promotional tone": [
        r"breathtaking", r"nestled (?:in|among|within)", r"\bboasts\b", r"must-see", r"world-class",
        r"vibrant (?:community|culture|city)", r"renowned for", r"stunning",
    ],
    "chat/tool leftovers": [
        r"\bcertainly!", r"here is (?:a|the) (?:revised|rewritten|improved)", r"i hope this helps",
        r"as an ai", r"as of my (?:last|latest) (?:update|knowledge)", r"\[your name\]",
        r"utm_source=chatgpt", r"\bfeel free to\b", r"let me know if",
    ],
}

STOCK_WORDS = [
    "delve", "delves", "delving", "tapestry", "testament", "intricate", "nuanced", "multifaceted",
    "pivotal", "crucial", "vital", "vibrant", "robust", "seamless", "seamlessly", "foster", "fosters",
    "fostering", "leverage", "leveraging", "realm", "underscore", "underscores", "underscoring",
    "showcase", "showcases", "showcasing", "enhance", "enhances", "bolster", "garner", "embark",
    "beacon", "interplay", "meticulous", "meticulously", "commendable", "paramount", "holistic",
    "synergy", "transformative", "groundbreaking", "navigate", "navigating", "landscape", "journey",
]

TRANSITIONS = [
    "moreover", "furthermore", "additionally", "in addition", "however", "overall", "ultimately",
    "consequently", "notably", "importantly", "thus", "therefore", "hence", "in conclusion",
    "firstly", "secondly", "lastly", "finally", "similarly", "likewise", "nevertheless",
]

CONTRAST = [
    r"\bnot (?:just|only|merely|simply)\b", r"\bisn'?t (?:just|only|merely|simply|about)\b",
    r"\bmore than (?:just|merely)\b", r"\bit'?s not (?:about )?\w+(?: \w+){0,4}[,;] it'?s\b",
    r"\bnot because\b.{0,60}\bbut because\b",
]

PARTICIPLE_TAIL = re.compile(
    r",\s+(?:thereby\s+|thus\s+)?(highlighting|underscoring|emphasizing|emphasising|reflecting|showcasing|"
    r"demonstrating|illustrating|contributing|paving|setting|signaling|signalling|marking|ensuring|"
    r"fostering|solidifying|cementing|reinforcing|symbolizing|revealing)\b",
    re.IGNORECASE,
)

TRIAD = re.compile(r"\b[\w'-]+(?: [\w'-]+){0,3}, [\w'-]+(?: [\w'-]+){0,3},? (?:and|or) [\w'-]+(?: [\w'-]+)?", re.IGNORECASE)

# ---------------------------------------------------------------- analysis

def cv(values):
    if len(values) < 2 or statistics.mean(values) == 0:
        return 0.0
    return statistics.pstdev(values) / statistics.mean(values)

def analyze(text):
    paras = split_paragraphs(text)
    sentences = [s for p in paras for s in split_sentences(p)]
    slen = [len(words(s)) for s in sentences if words(s)]
    total_words = len(words(text))
    plen = [len(words(p)) for p in paras]

    # longest run of consecutive sentences within +/-4 words of each other
    run = best = 1 if slen else 0
    for a, b in zip(slen, slen[1:]):
        run = run + 1 if abs(a - b) <= 4 else 1
        best = max(best, run)

    band = sum(1 for n in slen if 15 <= n <= 25)

    openers = {}
    transition_openers = 0
    for s in sentences:
        low = s.lower().lstrip("\"'“‘(")
        first = (words(low) or [""])[0]
        openers[first] = openers.get(first, 0) + 1
        if any(low.startswith(t + ",") or low.startswith(t + " ") for t in TRANSITIONS):
            transition_openers += 1

    raw = []
    for cat, pats in PHRASES.items():
        for pat in pats:
            for m in re.finditer(pat, text, re.IGNORECASE | re.MULTILINE):
                raw.append((m.start(), m.end(), cat, m.group(0)))
    # drop matches contained inside a longer match, then order by position
    raw.sort(key=lambda x: (x[0], -(x[1] - x[0])))
    hits, last_end = [], -1
    for start, end, cat, txt in raw:
        if end <= last_end:
            continue
        hits.append({"category": cat, "match": txt, "line": line_of(text, start)})
        last_end = max(last_end, end)

    contrast = []
    for pat in CONTRAST:
        for m in re.finditer(pat, text, re.IGNORECASE):
            contrast.append({"match": m.group(0), "line": line_of(text, m.start())})

    tails = [{"match": m.group(0).strip(", "), "line": line_of(text, m.start())} for m in PARTICIPLE_TAIL.finditer(text)]
    triads = [{"match": m.group(0), "line": line_of(text, m.start())} for m in TRIAD.finditer(text)]

    stock = {}
    for w in words(text.lower()):
        if w in STOCK_WORDS:
            stock[w] = stock.get(w, 0) + 1

    em = text.count("—") + len(re.findall(r"\s--\s", text))
    curly = len(re.findall("[“”‘’]", text))
    straight = len(re.findall("[\"']", text))
    md = len(re.findall(r"\*\*|^#{1,6} |^\s*[-*] ", text, re.MULTILINE))

    per_k = lambda n: round(1000 * n / total_words, 1) if total_words else 0.0

    metrics = {
        "words": total_words,
        "sentences": len(slen),
        "paragraphs": len(paras),
        "sentence_len_mean": round(statistics.mean(slen), 1) if slen else 0,
        "sentence_len_sd": round(statistics.pstdev(slen), 1) if len(slen) > 1 else 0,
        "sentence_len_cv": round(cv(slen), 2),
        "pct_sentences_15_25_words": round(100 * band / len(slen)) if slen else 0,
        "longest_uniform_run": best,
        "shortest_sentence": min(slen) if slen else 0,
        "longest_sentence": max(slen) if slen else 0,
        "paragraph_len_cv": round(cv(plen), 2),
        "transition_openers_pct": round(100 * transition_openers / len(sentences)) if sentences else 0,
        "stock_words_per_1k": per_k(sum(stock.values())),
        "phrase_hits": len(hits),
        "contrast_frames": len(contrast),
        "participle_tails": len(tails),
        "triads": len(triads),
        "em_dashes_per_1k": per_k(em),
        "mixed_quotes": bool(curly and straight),
        "markdown_remnants": md,
    }

    top_openers = sorted(((k, v) for k, v in openers.items() if v >= 3 and k), key=lambda x: -x[1])[:6]

    return {
        "metrics": metrics,
        "top_openers": top_openers,
        "stock_words": dict(sorted(stock.items(), key=lambda x: -x[1])),
        "phrase_hits": hits,
        "contrast_frames": contrast,
        "participle_tails": tails,
        "triads": triads,
        "sentence_lengths": slen,
    }

# ---------------------------------------------------------------- flags

def flags(m):
    """Plain-language notes on metrics outside typical human ranges.
    Thresholds are rough heuristics, not calibrated against any detector."""
    out = []
    if m["sentences"] >= 8:
        if m["sentence_len_cv"] < 0.35:
            out.append(f"Low sentence-length variation (CV {m['sentence_len_cv']}; varied human prose is often 0.45+). Uniform rhythm is a burstiness signal.")
        if m["pct_sentences_15_25_words"] >= 60:
            out.append(f"{m['pct_sentences_15_25_words']}% of sentences are 15-25 words. Few short or long sentences.")
        if m["longest_uniform_run"] >= 6:
            out.append(f"{m['longest_uniform_run']} consecutive sentences of near-identical length.")
        if m["shortest_sentence"] >= 10:
            out.append("No short sentences at all (shortest is 10+ words).")
    if m["paragraphs"] >= 4 and m["paragraph_len_cv"] < 0.2:
        out.append(f"Paragraphs are nearly the same length (CV {m['paragraph_len_cv']}). Template structure.")
    if m["transition_openers_pct"] >= 20:
        out.append(f"{m['transition_openers_pct']}% of sentences open with a transition word.")
    if m["stock_words_per_1k"] >= 6:
        out.append(f"Stock-vocabulary density {m['stock_words_per_1k']}/1k words (weak alone; check against the author's sample).")
    if m["participle_tails"] >= 2:
        out.append(f"{m['participle_tails']} participle tails announcing significance (strong tell).")
    if m["contrast_frames"] >= 2:
        out.append(f"{m['contrast_frames']} contrast frames like 'not just X'. Check each opposes a real view.")
    if m["phrase_hits"] >= 3:
        out.append(f"{m['phrase_hits']} stock-phrase hits; see list below.")
    if m["words"] and m["triads"] >= max(3, m["words"] // 250):
        out.append(f"{m['triads']} lists of three. Check which are reflexive.")
    if m["em_dashes_per_1k"] >= 8:
        out.append(f"Em dashes at {m['em_dashes_per_1k']}/1k words (weak alone; keep if it matches the author's habit).")
    if m["mixed_quotes"]:
        out.append("Mixed curly and straight quotes; can indicate pasted passages. Normalize.")
    if m["markdown_remnants"]:
        out.append(f"{m['markdown_remnants']} markdown remnants (**, #, list markers).")
    if m["words"] < 250:
        out.append("Short text: detectors are least reliable under ~250 words, in both directions.")
    return out

# ---------------------------------------------------------------- output

def report(path, r):
    m = r["metrics"]
    L = [f"Pattern scan: {path}", "(Not a detector. No score is estimated. Read flagged passages closely.)", ""]
    L.append(f"{m['words']} words | {m['sentences']} sentences | {m['paragraphs']} paragraphs")
    L.append(f"Sentence length: mean {m['sentence_len_mean']}, sd {m['sentence_len_sd']}, CV {m['sentence_len_cv']}, "
             f"range {m['shortest_sentence']}-{m['longest_sentence']}, {m['pct_sentences_15_25_words']}% in 15-25 band")
    L.append(f"Paragraph length CV: {m['paragraph_len_cv']} | transition openers: {m['transition_openers_pct']}% | "
             f"em dashes: {m['em_dashes_per_1k']}/1k")
    L.append("")
    fl = flags(m)
    L.append("READ CLOSELY:" if fl else "No metric is outside typical ranges. Still read against references/patterns.md.")
    L += [f"  - {f}" for f in fl]

    def section(title, items, key="match"):
        if items:
            L.append("")
            L.append(f"{title} ({len(items)}):")
            for it in items[:25]:
                L.append(f"  line {it['line']}: {it[key]}" + (f"  [{it['category']}]" if "category" in it else ""))
            if len(items) > 25:
                L.append(f"  ... {len(items) - 25} more")

    section("Stock phrases", r["phrase_hits"])
    section("Participle tails", r["participle_tails"])
    section("Contrast frames", r["contrast_frames"])
    section("Lists of three", r["triads"])
    if r["stock_words"]:
        L.append("")
        L.append("Stock words: " + ", ".join(f"{k} x{v}" for k, v in r["stock_words"].items()))
    if r["top_openers"]:
        L.append("Repeated sentence openers: " + ", ".join(f"'{k}' x{v}" for k, v in r["top_openers"]))
    if r["sentence_lengths"]:
        L.append("")
        L.append("Sentence lengths in order: " + " ".join(map(str, r["sentence_lengths"])))
    return "\n".join(L)

def compare(before, after):
    keys = ["words", "sentence_len_cv", "pct_sentences_15_25_words", "longest_uniform_run",
            "shortest_sentence", "paragraph_len_cv", "transition_openers_pct", "stock_words_per_1k",
            "phrase_hits", "participle_tails", "contrast_frames", "triads", "em_dashes_per_1k"]
    L = [f"{'metric':<28}{'before':>10}{'after':>10}"]
    for k in keys:
        L.append(f"{k:<28}{str(before[k]):>10}{str(after[k]):>10}")
    L.append("")
    L.append(f"Flags before: {len(flags(before))} | after: {len(flags(after))}")
    return "\n".join(L)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--json", action="store_true", help="print JSON")
    ap.add_argument("--compare", metavar="BEFORE", help="original file to compare metrics against")
    a = ap.parse_args()

    path = Path(a.file)
    if not path.exists():
        sys.exit(f"File not found: {path}")
    res = analyze(load_text(path))

    if a.compare:
        before = analyze(load_text(Path(a.compare)))["metrics"]
        print(compare(before, res["metrics"]))
    elif a.json:
        res["flags"] = flags(res["metrics"])
        print(json.dumps(res, indent=2))
    else:
        print(report(path, res))

if __name__ == "__main__":
    main()
