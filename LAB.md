# Week 10 Lab — Communicating with Data

**Time: 2 hours · API calls used: 0**
**Assessment A3 is due this week — see [MANIFEST.md](MANIFEST.md).**

| # | Activity | Time | Code? |
|---|----------|------|-------|
| 1 | Pick the question and find the answer | 20 min | run only |
| 2 | Build the four charts | 30 min | yes |
| 3 | Write the 400-word brief | 30 min | no |
| 4 | Peer review | 20 min | no |
| 5 | Assemble the notebook | 20 min | run only |

---

## 1. Pick the question, find the answer (20 min)

```powershell
pip install -r requirements.txt
python src/data_story.py
```

A data story answers **one** question. Not "here is what I found in the data"
— one question, which a person who does not work with data could ask out
loud.

The worked question: *do students at one campus do worse, and if so by how
much?*

```
Chennai     70.6    Coimbatore  70.5    Madurai  64.0
gap: 6.6 points
missing grades: Chennai 3.6%, Coimbatore 3.8%, Madurai 20.0%
```

That second line is the story. The third line is what makes it honest.

---

## 2. Build the four charts (30 min)

Four charts, in the order an **argument** goes — not the order the analysis
happened:

| Chart | Job |
|---|---|
| 1 **Context** | Orient the reader. What does this data look like? |
| 2 **Claim** | The finding, as plainly as possible |
| 3 **Evidence** | Test it. Is the gap real, or two outliers? |
| 4 **Caveat** | **What we do not know** |

Two rules with no exceptions:

**Y-axis starts at zero on a comparison chart.** Truncating it turns a
6-point gap into an apparent collapse, and every number on the chart stays
true. There is a test for this.

**Chart 4 is not optional.** A story with no caveat chart is a sales pitch.
It is also the chart most people leave out, so it is the cheapest marks in
the assessment.

---

## 3. Write the 400-word brief (30 min, no code)

**Claim → evidence → implication.** Claim in sentence one. If the reader
stops after the first paragraph, they should still have your finding.

Read [TECHNICAL_BRIEF.md](TECHNICAL_BRIEF.md) for the worked version, then
write your own.

Three things that separate a brief from a report:

- **Specific numbers.** "6.6 points", "n=80" — not "significantly lower".
- **The alternative explanation named and tested.** Chart 3 exists to rule
  out "a few very low scores".
- **The limitation inside the claim**, not footnoted. If it changes what the
  reader should do, it belongs in the first paragraph.

And say **what not to act on**. The worked brief explicitly calls the
0.1-point Chennai/Coimbatore difference noise.

---

## 4. Peer review (20 min, no code)

Swap. `worksheets/peer-review.md`.

Read the brief **before** the charts. If the claim does not survive that, the
charts are decoration.

The two questions:

1. **Does the evidence support the claim, or merely accompany it?** A chart
   next to a claim is not evidence for it.
2. **What would change your mind?** If there is no answer, the brief is
   advocacy, not analysis.

---

## 5. Assemble the notebook (20 min)

```powershell
python tools/build_notebook.py
jupyter notebook analysis.ipynb
```

One notebook, three components: cleaning (Week 8), distributions and
evaluation (Week 9), data story (this week).

**Run every cell top to bottom before you submit.** A notebook that only
works in the order you happened to execute it is the single most common way
this assessment loses marks.

```powershell
python -m pytest tests          # 12 tests
```

---

## Before you leave

- [ ] One question picked, and answered with numbers
- [ ] Four charts built, in argument order
- [ ] **Chart 4 shows what is missing**
- [ ] No truncated axes
- [ ] 400-word brief, claim first (Set B: 300 words)
- [ ] The limitation is in the claim
- [ ] Peer review done, both questions answered
- [ ] Notebook runs top to bottom with no errors
- [ ] **[MANIFEST.md](MANIFEST.md) checked line by line — A3 is due**
