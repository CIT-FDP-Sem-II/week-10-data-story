# Assessment A3 — Data Analysis Report

**Due: Week 10 · Weight: 15% · Individual · A single Jupyter notebook**

One notebook, three components. `analysis.ipynb` in this repo is the worked
template — replace its content with your own dataset and your own Semester 1
tool.

---

## Set A (IT background)

### Component 1 — Cleaning pipeline

- [ ] **Documented pandas operations** — every step says what and why
- [ ] **Before/after validation** — each claim proved in a cell, not asserted
- [ ] **Data quality summary table**

### Component 2 — Distributional analysis and evaluation

- [ ] **Distributional analysis using matplotlib**
- [ ] **20-question AI evaluation dataset with expected outputs**
- [ ] **Measured accuracy** against a Semester 1 tool
- [ ] Failure patterns identified

### Component 3 — Data story

- [ ] **4-chart data story** answering one real question
- [ ] **400-word technical brief**, structured **claim → evidence → implication**

### Graded on

| Criterion | What the grader looks for |
|---|---|
| **Cleaning rigour** | Every step justified; order defensible; nothing deleted that was not an exact duplicate |
| **Statistical correctness** | Mean vs median read correctly; a multimodal column not described as having a centre; missing data accounted for |
| **Argument structure of the brief** | Claim first; evidence tests an alternative explanation; limitation inside the claim, not footnoted |

---

## Set B (non-IT background)

Claude-assisted code accepted; the **interpretation must be individually
written**.

### Component 1
- [ ] Cleaning pipeline with **plain-language comments** — what each step
      does and why

### Component 2
- [ ] For each chart, **2–3 sentences on what the data shape means**
- [ ] **15-question** evaluation set with expected answers
- [ ] Full distributional analysis **not required**
- [ ] Adversarial inputs **not required**

### Component 3
- [ ] 4-chart data story
- [ ] **300-word** plain-language brief for a **non-technical reader**

### Graded on

| Criterion | What the grader looks for |
|---|---|
| **Clarity of interpretation** | Can you say what the chart means, not just what it shows? |
| **Evaluation set quality** | Does it include questions the material does not cover? |
| **Strength of data story** | Does the claim follow from the charts? |

---

## The four things most often missed

**1. No caveat chart.** Three charts that support the claim and none that
shows what is missing. Chart 4 in the worked example is 20% of the marks for
component 3 and takes five minutes.

**2. A truncated y-axis.** Starting a comparison bar chart at 60 instead of 0
makes a 6-point gap look like a collapse. Every number stays true and the
chart still lies.

**3. An overall accuracy number with no breakdown.** "85% accurate" over a
mixed dataset hides the only thing worth knowing — whether the failures are
on the questions where being wrong does harm.

**4. A brief with no limitation.** If nothing in the brief could be wrong,
it is advocacy. Name what would change your mind.

---

## Before you submit

- [ ] `python tools/build_notebook.py` runs and `analysis.ipynb` is valid
- [ ] **Every code cell in the notebook runs top to bottom without error**
- [ ] `python -m pytest tests` passes
- [ ] The brief is 400 words (Set B: 300), claim first
- [ ] Four charts, one of which shows what is **missing**
- [ ] Evaluation accuracy reported **by category**
- [ ] Peer review completed using `worksheets/peer-review.md`
