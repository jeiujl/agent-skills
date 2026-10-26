---
name: study-guide-builder
description: Turns course materials (lecture slides, notes, PDFs, textbook chapters, syllabi, past exams, problem sets, recordings' transcripts) into a study guide shaped to the learner's preferences plus a dated study plan up to the exam. Use when the user says "make a study guide", "build me a study plan", "help me prep for my midterm/final", "organize my notes", "what should I study", "make flashcards from this", or drops a folder of course files.
---

# Study Guide Builder

Two deliverables from the user's own materials: a **study guide** laid out the way they like to learn, and a **study plan** with real dates that fits their hours. Format follows their preferences; method follows the evidence on what actually builds retention.

## Step 0 - Learner profile

Look for `~/.claude/study-profile.md`. If it exists, read it and skip to Step 1 (confirm anything that looks stale, e.g. last term's schedule). If not, run a short intake, one message or one AskUserQuestion round, max six questions:

1. **How material lands best** (pick any): dense one-page summaries / worked examples first / diagrams and concept maps / Q&A and flashcards / narrative "explain it like a story" / teaching it back.
2. **Schedule:** hours available per weekday, best time of day, longest focus block before they fade (default 50 min).
3. **Per course:** exam date and time, format (multiple choice, written, problem-solving, case), open or closed book, formula sheet allowed, current confidence 1-5, target grade.
4. **What has worked and failed before** ("rereading never sticks", "I cram the night before", "practice problems are the only thing that works").
5. **Output format:** Markdown (default), PDF, Word, Anki deck, Notion page.
6. Days they can't study (shifts, trips, other deadlines).

Save the answers to `~/.claude/study-profile.md` in a short, editable form. Update it whenever the user corrects something ("too long", "more examples", "I'm actually free Fridays").

**Learning styles, briefly:** a stated preference (visual, verbal, examples-first) is a good reason to pick a format and a poor reason to change the method. Research hasn't found that matching content to a "learning style" improves retention (Pashler et al., 2008). What does: retrieval practice and spaced practice (rated highest-utility in Dunlosky et al., 2013), interleaving, worked examples that fade into independent problems, self-explanation, and pairing words with visuals. Rereading, highlighting, and summarizing rate low. So a "visual learner" gets concept maps **and** closed-book recall. Mention this once, in a sentence, if they say they're a particular type; don't lecture.

## Step 1 - Ingest the materials

1. **Inventory everything** they gave you: file, type, what it covers, date or week. Read PDFs, slides, and docs fully (use the pdf/pptx/docx reading skills where available). For slides that are mostly images or diagrams, look at them, not just the extracted text.
2. **Find the scope.** Syllabus, exam announcement, or professor's review sheet decides what's in. If none exists, ask for scope and date before building; don't guess an exam's coverage.
3. **Mine past exams and problem sets first.** They're the highest-value material: list question types, topic frequency, point weights, and the verbs used (define, calculate, compare, evaluate).
4. **Build a topic map:** units → topics → concepts, each with a source pointer (`Lecture 7, slides 12-18`; `Ch. 4 p. 112`). Pointers let the user jump back to the original.
5. **Weight each topic:** exam weight × professor emphasis (lecture time, repetition, "this will be on the exam", appears on past exams) × the user's weakness. Score 1-3 for weight and carry their 1-5 confidence; the plan script uses both.
6. **Stay inside the materials.** When you have to fill a gap from general knowledge (a step the slides skip, a definition never given), mark it `[added - not in your materials, check]`. Flag contradictions between sources (slides say X, textbook says Y) instead of picking one silently.

## Step 2 - The study guide

Layout, adapted to the profile:

**Page 1 - Exam at a glance:** date, time, format, scope, weighting, allowed aids, and the 8-10 highest-yield topics in priority order.

**Per unit:**
- **Big picture** - 2-3 sentences: what problem this unit solves and how it connects to the others.
- **Core concepts** - for each:
  - plain-language explanation
  - precise definition, formula, or rule, exactly as the course states it
  - one worked example, from their materials when possible, with every step shown
  - common mistakes and traps (from past exams, marking notes, or the professor's warnings)
  - how it's tested (question types seen, typical marks)
- **Connections** - where this concept shows up again later or gets combined with others.
- **Self-test** - 5-10 questions per unit mixing recall, application, compare/contrast, and "explain why". Answers go in a key at the end of the unit, never inline under the question.

**End matter:**
- Formula / definition sheet. If a crib sheet is allowed, format it to the real constraints (one page, both sides, etc.).
- Interleaved practice set across units with full worked solutions.
- Flashcards as `flashcards.tsv` (front, back, tags; Anki imports this directly) if they want cards.

**Format adapters** (from the profile):
| Preference | Change |
|---|---|
| Diagrams / maps | Mermaid concept map per unit, comparison tables, process flow diagrams |
| Examples first | Open each concept with a worked problem, then generalize the rule |
| Dense summaries | One page per unit, bullets, no prose padding; self-tests still included |
| Q&A / flashcards | Each concept rendered as question → answer pairs, plus the card export |
| Narrative | Each unit told as a story of the problem and how the idea solves it, with self-explanation prompts ("why does this step work?") |
| Teach-back | End each unit with 3 prompts to explain aloud in 2 minutes, plus what a complete explanation must include |

For quantitative courses (finance, accounting, stats, calculus, econ), weight worked examples and practice problems over prose, and **verify every computed answer by running the calculation in code** before it goes in a key. A wrong answer key is worse than none.

## Step 3 - The study plan

Use the script; it handles real dates, weekdays, hour limits, spaced reviews, interleaving, mock exams, and multiple courses competing for time. Check today's date first.

```bash
python3 scripts/plan.py spec.json --csv study-plan.csv --ics study-plan.ics > study-plan.md
```

`spec.json` (full schema in the script's docstring):

```json
{
  "start": "YYYY-MM-DD",
  "session_minutes": 50,
  "start_time": "18:00",
  "availability": {"mon": 2, "tue": 1.5, "wed": 2, "thu": 1, "fri": 0.5, "sat": 3, "sun": 3},
  "blackout": ["YYYY-MM-DD"],
  "buffer_day": "auto",
  "courses": [
    {"name": "COURSE 101", "exam": "YYYY-MM-DD", "exam_time": "09:00",
     "topics": [{"name": "Topic", "weight": 3, "confidence": 2}]}
  ]
}
```

What the script builds: weak, heavy topics get two learning blocks; each learned topic is reviewed at roughly +1, +3, +7, +14 days (as the calendar allows); spare time becomes interleaved practice; a timed mock exam lands 2-3 days before each exam; the night before is light review only; one low-availability day a week is a catch-up buffer. It prints warnings when the hours can't cover the material. When that happens, tell the user plainly and offer the trade-offs: more hours, an earlier start, or which low-weight topics to cut.

After generating, sanity-check: dates and weekdays line up, no day exceeds their hours, every exam-scope topic appears, and nothing is scheduled on blackout days. Show the plan table in the reply; offer the `.ics` for their calendar.

**Session template** (put at the top of the plan so every block runs the same way):
1. 5 min: closed-book recall of the previous session's material. Write, then check.
2. Main block: the scheduled activity.
3. Last 5 min: three self-test questions on today's topic; log confidence 1-5 and what was missed.

## Step 4 - Keep it current

Create `study-log.md` next to the plan. When the user reports back ("bombed the elasticity questions", "skipped Thursday"), update topic confidence in the spec, re-run the script from today, and show only what changed. Wrong answers on self-tests and mock exams are the best signal for re-weighting.

## Output

Write files into `study/<course>/` (or the folder the user names):

- `study-guide.md` (or PDF/DOCX via those skills if requested)
- `practice-set.md` with worked solutions
- `flashcards.tsv` if wanted
- `study-plan.md`, `study-plan.csv`, `study-plan.ics`
- `spec.json` and `study-log.md` for updates

Then reply briefly: what was built, the top 3 priority topics and why, any coverage warnings, and where the files are.

## Quality bar

- Every topic in exam scope is covered, and every concept points back to its source.
- Nothing invented without the `[added]` tag.
- Every answer in every key has been worked through; numeric answers verified in code.
- The plan fits the hours they gave you, not the hours you wish they had.
- Self-tests ask for recall and application, not recognition of a phrase from the notes.
