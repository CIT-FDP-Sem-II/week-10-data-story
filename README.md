# Week 10 — Communicating with Data

**CIT AI-Native Engineering Program · Year 1 · Semester 2 · Module M3**

An analysis nobody acts on was not finished. This week turns the Week 8–9 work
into an argument someone can read in two minutes and decide on.

**Lab time: 2 hours. API calls: 0.** See [LAB.md](LAB.md).

> ### Assessment A3 is due this week
> 15% of the semester, submitted as **one Jupyter notebook**. The checklist
> is in **[MANIFEST.md](MANIFEST.md)**, for both sets.

## Contents

| Path | What it is |
|---|---|
| `analysis.ipynb` | **The A3 deliverable** — three components in one notebook |
| `tools/build_notebook.py` | Generates the notebook, so it stays valid JSON |
| `src/data_story.py` | The four charts and the findings the brief quotes |
| `TECHNICAL_BRIEF.md` | The worked 400-word brief, claim → evidence → implication |
| `worksheets/peer-review.md` | Reviewing someone else's story |
| `src/clean.py`, `src/distributions.py` | Copied forward from Weeks 8 and 9 |
| `data/` | Raw and cleaned data, plus the Week 9 evaluation dataset |
| `tests/` | 12 tests. No API key needed. |

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # mac/linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Running

```powershell
python src/data_story.py          # four charts + the numbers
python tools/build_notebook.py    # regenerate analysis.ipynb
jupyter notebook analysis.ipynb
python -m pytest tests -v         # 12 tests
```

> Everything in this repo runs offline and is **verified**: all four charts
> build, every one of the notebook's 11 code cells executes top to bottom,
> and the brief is checked for length and structure. There are no API calls
> this week.

## The four charts

An argument, not a gallery. The order is the order an argument goes in — not
the order the analysis happened.

| Chart | Job | In the worked example |
|---|---|---|
| 1 **Context** | Orient the reader | Grade distribution across all campuses |
| 2 **Claim** | The finding, plainly | Mean grade by campus — a 6.6-point gap |
| 3 **Evidence** | Test it | Boxplot: is the gap real, or two outliers? |
| 4 **Caveat** | **What we do not know** | 20% of Madurai grades are missing |

**Chart 4 is the one most people leave out, and it is the one that makes the
other three trustworthy.** A story with no caveat chart is a sales pitch.

## Two rules with no exceptions

**The y-axis starts at zero on a comparison chart.** Truncating it turns a
6.6-point gap into an apparent collapse while every number on the chart stays
true. It is the commonest honest-looking lie in data communication, and
`test_the_claim_chart_axis_is_not_truncated` enforces it.

**Colour carries meaning.** One colour for the thing under discussion, grey
for everything else. A different colour per category is prettier and says
nothing.

## The finding, and what makes it honest

```
Chennai    70.6  (n=80)    3.6% of grades missing
Coimbatore 70.5  (n=102)   3.8% of grades missing
Madurai    64.0  (n=84)   20.0% of grades missing
```

The gap is 6.6 points. But the campus with the lowest mean is also the one
we know **least** about — one in five of its grades is absent, against one in
twenty elsewhere.

If those grades are missing because students withdrew, the recorded mean
already excludes the weakest performers and the **real gap is wider**. If they
are missing for an administrative reason, 64.0 is fair. **Nothing in the data
distinguishes the two**, and saying so is the most valuable sentence in the
brief.

That is why 6.6 is reported as a **lower bound**, not an estimate.

## Why the notebook is generated

`analysis.ipynb` is built by `tools/build_notebook.py` rather than written by
hand. A notebook is JSON, and hand-editing JSON produces files that fail to
open. Editing the generator and re-running it keeps the notebook valid and
makes its structure reviewable as ordinary Python.

Commit both.

---

## Set B (non-IT background)

**`src/data_story.py`**
- `load()` — reads the cleaned data.
- `colours_for(campuses)` — returns a colour per bar: the highlight colour
  for the campus being discussed, grey for the rest. This is what makes the
  point visible without reading a legend.
- `chart_1_context(df)` — a histogram of all grades, so the reader knows what
  normal looks like before you tell them something is abnormal.
- `chart_2_claim(df)` — a bar chart of mean grade per campus, with the y-axis
  pinned from 0 to 100 so the comparison is honest.
- `chart_3_evidence(df)` — a boxplot, which shows the whole spread rather than
  just the average, so the reader can see whether the gap is in the typical
  student or just the worst ones.
- `chart_4_caveat(df)` — the percentage of grades **missing** at each campus.
- `findings(df)` — works out the numbers the brief quotes: the mean per
  campus, the size of the gap, and the missing percentages. Computed, so the
  brief cannot drift out of step with the data.

**`tools/build_notebook.py`**
- `md(text)` and `code(text)` — build one markdown cell or one code cell.
- `CELLS` — the notebook, in order, as a list.
- `main()` — wraps the cells in the standard notebook structure and writes
  the `.ipynb` file.

### What Set B may simplify

- **300-word brief** for a **non-technical reader**, instead of 400 technical.
- **2–3 sentences per chart** on what the shape means, instead of a full
  distributional analysis.
- **15-question** evaluation set instead of 20.
- Adversarial inputs not required.

### What Set B may **not** simplify

- **Four charts, one of which shows what is missing.**
- **Claim first.** The structure is the assessment in both sets.
- The notebook must **run top to bottom** without errors.
