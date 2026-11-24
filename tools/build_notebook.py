"""Build analysis.ipynb - the single notebook Assessment A3 asks for.

    python tools/build_notebook.py

The notebook is generated rather than hand-written so that it stays valid
JSON and so that a change to the structure is a change to one file rather
than to a few hundred lines of escaped notebook. Edit this, re-run it, and
commit both.

The notebook has the three components A3 requires:
    1. Cleaning pipeline       (Week 8)
    2. Distributions + eval    (Week 9)
    3. Data story + brief      (Week 10)
"""

import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
NOTEBOOK = ROOT / "analysis.ipynb"


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.strip().split("\n")}


def code(text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.strip().split("\n"),
    }


CELLS = [
    md("""
# Data Analysis Report

**Assessment A3** · CIT AI-Native Engineering Program · Semester 2

| | |
|---|---|
| **Name** | *(your name)* |
| **Set** | A / B |
| **Dataset** | Student enrolments, 316 raw rows |

Three components:

1. **Cleaning pipeline** — documented pandas operations, before/after
   validation, data quality summary table
2. **Distributional analysis** — matplotlib, plus a 20-question AI evaluation
   dataset with measured accuracy
3. **Data story** — four charts and a 400-word technical brief

> Replace the worked example throughout with **your own** dataset and **your
> own** Semester 1 tool. The structure stays; the content is yours.
"""),

    code("""
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "src"))

import matplotlib.pyplot as plt
import pandas as pd

pd.set_option("display.width", 120)
"""),

    # --- component 1 -----------------------------------------------------
    md("""
---

# 1. Cleaning Pipeline

## 1.1 The data before cleaning

Audit first. Never clean anything you have not looked at.
"""),

    code("""
raw = pd.read_csv("data/enrolments_raw.csv", dtype=str, keep_default_na=False)
print(raw.shape)
raw.head()
"""),

    code("""
# The audit. Each of these exposes one category of fault.
print("distinct courses:", raw["course"].nunique())
print("exact duplicates:", raw.duplicated().sum())
print()
print("campus values - note that 'N/A' is TEXT, so isna() will not see it:")
print(raw["campus"].value_counts().head())
print()
print("what isna() claims:", raw.isna().sum().sum())
"""),

    md("""
**Finding.** `isna()` reports zero missing values and the dataset has many.
`"N/A"`, `""` and `"   "` are all text. Every count built on `isna()` before
step 2 of the pipeline is wrong, and nothing warns you.

> *Your turn: list the faults you found, with how you found each one.*

## 1.2 The cleaning plan

Written **before** the code. Each step says what, why, and how it is checked.
The order is not arbitrary — see `CLEANING_PLAN.md`.

| # | Step | Why here |
|---|---|---|
| 1 | Strip whitespace, fix encoding | Everything downstream compares strings |
| 2 | Convert disguised nulls | Until then `isna()` lies |
| 3 | Fix types | Cannot test a negative fee while it is text |
| 4 | Standardise categories | Four spellings become one |
| 5 | Parse dates | Needs step 1 |
| 6 | Remove duplicates | **After** standardising, or near-duplicates survive |
| 7 | Handle impossible values | Needs the right type to test |

## 1.3 Run the pipeline
"""),

    code("""
from clean import clean, summary_table

cleaned, report = clean(raw.copy())
print(summary_table(report))
"""),

    md("""
## 1.4 Before / after validation

| Check | Target | Result |
|---|---|---|
| Distinct courses | 3 | |
| Exact duplicates | 0 | |
| `fee_paid` dtype | integer | |
| `enrolled_on` dtype | datetime | |
| Ages outside 16–80 | 0 | |
| **Rows lost** | **only exact duplicates** | |

> *Fill in the Result column from the output above.*
"""),

    code("""
# Prove it rather than asserting it.
checks = {
    "distinct courses": cleaned["course"].nunique(),
    "exact duplicates": int(cleaned.duplicated().sum()),
    "fee_paid dtype": str(cleaned["fee_paid"].dtype),
    "enrolled_on dtype": str(cleaned["enrolled_on"].dtype),
    "ages outside 16-80": int((~cleaned["age"].dropna().between(16, 80)).sum()),
    "rows lost": report["rows_in"] - report["rows_out"],
    "of which duplicates": report["exact_duplicates"],
}
for name, value in checks.items():
    print(f"{name:<22}{value}")
"""),

    md("""
### The four decisions

| Decision | Why |
|---|---|
| **Do not impute** missing grades | Filling them invents those students' performance, and section 2 would then measure our arithmetic |
| **Map courses explicitly**, not `.lower()` | `"CS"` lowercases to `"cs"`, not to `"computer science"` |
| **Report** near-duplicates, do not drop | We do not know if they are a broken export or two real records |
| **Null** impossible values, do not drop rows | One bad cell should not cost four good ones |

### The fault with no fix

Some dates are `dd/mm/yyyy`, some `mm/dd/yyyy`. `03/04/2025` is 3 April or
4 March and **nothing in the data says which**. The pipeline counts them and
reports the number. The number is the finding.
"""),

    code("""
print(f"ambiguous dates: {report['ambiguous_dates']} of {report['rows_out']} rows "
      f"({100 * report['ambiguous_dates'] / report['rows_out']:.0f}%)")
"""),

    # --- component 2 -----------------------------------------------------
    md("""
---

# 2. Distributional Analysis and AI Evaluation

## 2.1 Summary statistics — and why they are not enough
"""),

    code("""
from distributions import describe_shape

stats = pd.DataFrame([describe_shape(cleaned[c], c)
                      for c in ["final_grade", "age", "fee_paid"]]).set_index("column")
stats
"""),

    md("""
**Finding.** `fee_paid` has only three distinct values — one per course. Its
mean is a fee **no student pays**. The mean, median and standard deviation all
look perfectly reasonable; only the cardinality check catches it.

This is why `describe()` is not an analysis.

## 2.2 Distributions
"""),

    code("""
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

grades = cleaned["final_grade"].dropna()
axes[0].hist(grades, bins=22, edgecolor="white")
axes[0].axvline(grades.mean(), linestyle="--", label=f"mean {grades.mean():.1f}")
axes[0].set_title("Final grades")
axes[0].set_xlabel("grade")
axes[0].legend(frameon=False)

axes[1].hist(cleaned["age"].dropna(), bins=range(16, 50, 2), edgecolor="white")
axes[1].set_title("Ages")
axes[1].set_xlabel("age")

plt.tight_layout()
plt.show()
"""),

    md("""
> *Set B: write 2–3 sentences per chart on what the shape means.*

## 2.3 The evaluation dataset

20 questions with expected outputs — **10 the material covers, 10 it does
not.** A tool that is accurate on material it has and invents answers for
material it does not is dangerous, and a test set of only covered questions
scores it well and calls it good.
"""),

    code("""
questions = pd.read_csv("data/eval_questions.csv")
print(questions["category"].value_counts().to_string())
questions[["id", "question", "category"]].head(10)
"""),

    md("""
## 2.4 Measured accuracy

Run `python src/evaluate.py` from your **Week 9** repo (20 API calls), then
paste the results here.

| Category | Correct | Total |
|---|---|---|
| covered | | 10 |
| not covered | | 4 |
| false premise | | 2 |
| partially covered | | 1 |
| out of scope | | 1 |
| ambiguous | | 1 |
| multi-part | | 1 |
| **Overall** | | **20** |

**Failure patterns.** Which category was worst? What does that mean for
anyone using the tool?

> *Your analysis here. The overall number is the least useful one in the
> table.*
"""),

    # --- component 3 -----------------------------------------------------
    md("""
---

# 3. Data Story

**Question:** do students at one campus do worse, and if so by how much?

Four charts, in the order an argument goes — not in the order the analysis
happened.
"""),

    code("""
from data_story import CHARTS_IN_ORDER, findings

result = findings(cleaned)
print(result["by_campus"].to_string())
print(f"\\ngap: {result['gap']} points between {result['best']} and {result['worst']}")
print(f"missing grades by campus (%): {result['missing_pct']}")
"""),

    code("""
for function in CHARTS_IN_ORDER:
    figure, name = function(cleaned)
    plt.show()
"""),

    md("""
## 3.1 Reading the four charts

| Chart | Job | What it shows |
|---|---|---|
| 1 Context | Orient the reader | The overall grade distribution |
| 2 Claim | State the finding | The gap between campuses |
| 3 Evidence | Test the finding | Spread — is the gap real, or two outliers? |
| 4 **Caveat** | **What we do not know** | Missing grades are not spread evenly |

Chart 4 is the one most people leave out, and it is the one that makes the
other three trustworthy. **A story with no caveat chart is a sales pitch.**

Note also that chart 2's y-axis starts at zero. Truncating it would make a
6-point gap look like a collapse — the commonest way a chart lies while every
number on it stays true.

## 3.2 Technical brief (400 words)

> Structure: **claim → evidence → implication.** Claim first. The reader
> should know your finding before they know how you got it.
>
> See `TECHNICAL_BRIEF.md` for the worked version. Write your own below.

---

*(your 400 words here)*

---

## 3.3 Peer review

> Swap with a partner. Use `worksheets/peer-review.md`.
>
> The two questions that matter: **is the claim supported by the charts**, and
> **what would change your mind?**
"""),
]


def main():
    notebook = {
        "cells": CELLS,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.11"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    NOTEBOOK.write_text(json.dumps(notebook, indent=1), encoding="utf-8")
    markdown = sum(c["cell_type"] == "markdown" for c in CELLS)
    print(f"wrote {NOTEBOOK} - {len(CELLS)} cells "
          f"({markdown} markdown, {len(CELLS) - markdown} code)")


if __name__ == "__main__":
    main()
