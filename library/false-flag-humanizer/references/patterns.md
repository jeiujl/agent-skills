# Pattern catalog for academic writing

Adapted for essays and reports from Wikipedia's "Signs of AI writing" (the guide WikiProject AI Cleanup editors use) plus what's known about detector mechanics. Strength ratings: **strong** = worth an edit on one sighting; **medium** = edit when it repeats; **weak alone** = only meaningful alongside other tells.

The Wikipedia editors' own caveat applies here more than anywhere: these patterns appear in plenty of human writing, especially from students taught to write to a template or writing in a second language. A match is a reason to read closely, never proof.

---

## 1. Significance inflation (strong)

Ordinary facts framed as historic, pivotal, or profound, with no evidence for the weight.

- "stands as a testament to", "serves as a reminder", "marks a pivotal moment / turning point"
- "plays a crucial / vital / pivotal / significant role in"
- "leaves a lasting legacy / impact", "cannot be overstated", "shaping the future of"
- "in today's fast-paced / ever-changing / digital world", "now more than ever"
- "rich tapestry", "ever-evolving landscape", "the intricate interplay of"

**Fix:** state the actual fact or consequence. If the author thinks it matters, have them say what changed because of it.

## 2. Participle tails that announce meaning (strong)

A sentence ends with a comma plus an -ing phrase claiming significance instead of showing it.

- "..., highlighting / underscoring / emphasizing the importance of X"
- "..., reflecting / showcasing / demonstrating / illustrating X"
- "..., contributing to / paving the way for / setting the stage for X"

**Fix:** either delete the tail or turn it into a real claim with support ("This mattered because...").

## 3. Contrast staging (strong)

A contrast against something nobody claimed, used for emphasis.

- "It's not just X, it's Y." / "This isn't about X; it's about Y."
- "not only... but also" used repeatedly
- "X is more than just Y"

**Fix:** state Y directly. Keep a contrast only when someone actually holds the opposing view, and name them.

## 4. Forced triads (medium)

Lists of three by reflex: three adjectives, three examples, three parallel clauses, paragraph after paragraph. Also visible at larger scale: three body paragraphs with the same internal shape.

**Fix:** use the number of items the content has. Two good examples beat three where one is filler.

## 5. Transition chains (medium)

Sentence- or paragraph-initial connectors on autopilot: Moreover, Furthermore, Additionally, In addition, However, Overall, Ultimately, Consequently, Notably, Importantly, Thus.

**Fix:** delete most of them; the logic usually carries itself. Keep the ones that mark a real turn in reasoning.

## 6. Hedge and balance filler (medium)

- "It is important to note / consider / remember that"
- "It's worth noting that", "One could argue that"
- "While X has its benefits, it also has drawbacks" with no specifics on either side
- Ending every section on "both sides have merit"

**Fix:** delete the frame and keep the claim. If the essay is meant to argue, let it take a position.

## 7. Vague attribution (medium, and a grading problem)

"Experts argue", "studies show", "research suggests", "many believe", "critics have noted", "historians agree" with no citation.

**Fix:** cite the specific source the author used, or cut the claim.

## 8. Uniform rhythm (medium; detectors weight this)

Most sentences 15-25 words, same subject-verb-object shape, no fragments, few long sentences, paragraphs of near-identical length. This is the burstiness signal.

**Fix:** let length follow meaning. A short sentence after a long one for emphasis. One-sentence paragraphs where a point deserves it. Merge choppy runs.

## 9. Template structure (medium)

- Intro that restates the prompt, announces "In this essay, I will..."
- Every body paragraph: topic sentence, elaboration, example, "Overall," wrap-up
- "In conclusion," followed by a summary of each paragraph in order
- A closing "Challenges and future outlook" or a hopeful moral: "As we move forward...", "Only time will tell", "a brighter future"

**Fix:** respect the rubric, but let the conclusion do work: a consequence, an implication, a limitation, a question the essay opens. Vary paragraph internals.

## 10. Stock vocabulary (weak alone)

Overrepresented in model output; lists drift with each model generation, so treat as weak evidence: delve, tapestry, testament, intricate, nuanced, multifaceted, pivotal, crucial, vital, vibrant, robust, seamless, foster, leverage, navigate (figurative), realm, landscape (figurative), underscore, showcase, enhance, bolster, garner, embark, journey (figurative), beacon, interplay, meticulous, commendable, paramount, holistic, synergy, transformative, groundbreaking, game-changer.

**Fix:** replace only when the plain word is clearer ("use" for "leverage", "show" for "showcase"). Don't strip words the author genuinely uses elsewhere in their writing sample.

## 11. Elegant variation (weak alone)

Cycling synonyms to avoid repeating a noun: "the city... the metropolis... the urban center... the bustling hub."

**Fix:** repeat the plain noun or use a pronoun.

## 12. False ranges (weak alone)

"From X to Y" where X and Y aren't ends of a real spectrum: "from ancient traditions to cutting-edge innovation."

**Fix:** name the actual items or cut.

## 13. Promotional or travel-brochure tone (medium)

"breathtaking", "nestled in", "boasts", "a must-see", "stunning", "renowned", "world-class", "vibrant community".

**Fix:** neutral description with specifics.

## 14. Formatting tells (medium, when submitted as a document)

- Headings in Title Case for every section of a short essay; bullet points inside an essay
- Bold on key terms throughout the body
- Heavy em-dash use (weak alone; many humans write this way)
- Mixed curly and straight quotes, which can indicate pasted text
- Markdown remnants: `**`, `##`, leftover list markers

**Fix:** match the assignment's expected format. Normalize quotes. Remove markdown.

## 15. Chat and tool leftovers (strong, but rare in human work)

"Certainly!", "Here is a revised version", "I hope this helps", "As an AI", "as of my last update", "[Your Name]" placeholders, notes addressed to a reader who isn't the instructor. Sometimes left behind when a student pasted a passage back from a grammar or rewording tool.

**Fix:** remove. Ask the author where the passage came from, since it affects the defense.

## 16. Citation tells (strong)

References that don't exist, DOIs that don't resolve, generic or slightly wrong titles, real authors attached to papers they didn't write, `utm_source=chatgpt.com` in URLs, page numbers that don't match the source.

**Fix:** verify every reference is real and supports the claim it's attached to. Nothing damages credibility faster in an integrity case than one bad citation.

---

## Not reliable signs (don't "fix" these)

Correct grammar and spelling. Formal register in a formal assignment. A single em dash or one "delve". British or Canadian spelling. Clear organization. A thesis statement the rubric demands. These are normal in good human writing, and removing them makes the essay worse without making it more credible.

## Human signals worth keeping or strengthening

- Concrete, course-specific references: a lecture, a class discussion, a reading's page number, a lab result the author actually got
- A position the author holds and defends, including where they changed their mind
- Specific uncertainty ("I couldn't find data after 2019, so...") instead of blanket hedging
- Paragraph lengths that follow the content
- Domain terms used precisely and consistently
- Quotes followed by the author's own analysis rather than a restatement
- The author's own recurring phrasings and sentence habits from their writing sample
