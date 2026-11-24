"""Distributional analysis of the cleaned Week 8 dataset. No API calls.

    python src/distributions.py

Writes four charts to charts/ and prints the numbers behind them.

The point of this script is not the charts. It is the gap between the summary
statistics and the shape: three of the four columns here have a mean that
tells you something actively misleading, and you cannot see that from
describe().
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # write files; do not try to open a window

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "enrolments_clean.csv"
CHARTS = ROOT / "charts"


def load():
    """Read the cleaned data from Week 8."""
    if not DATA.exists():
        raise SystemExit(
            f"Cannot find {DATA}.\n"
            "Copy enrolments_clean.csv from your Week 8 repo, or run that "
            "repo's tools/make_messy_data.py and src/clean.py."
        )
    return pd.read_csv(DATA, parse_dates=["enrolled_on"])


def describe_shape(series, name):
    """The numbers that tell you the shape, not just the centre.

    mean vs median is the most useful comparison in descriptive statistics:
    when they disagree, the distribution is skewed and the mean is reporting
    the tail rather than the typical case.

    But the check that catches the worst error here is the cardinality one.
    A column with four distinct values is not a distribution with a centre at
    all, and its mean is a number no row contains.
    """
    missing = int(series.isna().sum())
    values = series.dropna()
    mean, median = values.mean(), values.median()
    distinct = values.nunique()

    if distinct <= 10:
        shape = f"multimodal - only {distinct} distinct values; the mean is not a real one"
    elif mean > median * 1.05:
        shape = "right-skewed (a long tail of high values pulls the mean up)"
    elif mean < median * 0.95:
        shape = "left-skewed (a long tail of low values pulls the mean down)"
    else:
        shape = "roughly symmetric - mean and median agree"

    return {
        "column": name,
        "n": len(values),
        "missing": missing,
        "distinct": distinct,
        "mean": round(mean, 2),
        "median": round(median, 2),
        "std": round(values.std(), 2),
        "p25": round(values.quantile(0.25), 2),
        "p75": round(values.quantile(0.75), 2),
        "min": round(values.min(), 2),
        "max": round(values.max(), 2),
        "shape": shape,
    }


def chart_grade_histogram(df):
    """Is the grade distribution normal, or does it have structure?"""
    fig, ax = plt.subplots(figsize=(7, 4))
    grades = df["final_grade"].dropna()
    ax.hist(grades, bins=20, edgecolor="white")
    ax.axvline(grades.mean(), linestyle="--", label=f"mean {grades.mean():.1f}")
    ax.axvline(grades.median(), linestyle=":", label=f"median {grades.median():.1f}")
    ax.set_title("Final grades")
    ax.set_xlabel("grade")
    ax.set_ylabel("students")
    ax.legend()
    fig.tight_layout()
    return fig, "grades-histogram.png"


def chart_age_distribution(df):
    """Ages are long-tailed: most students cluster, a few are much older."""
    fig, ax = plt.subplots(figsize=(7, 4))
    ages = df["age"].dropna()
    ax.hist(ages, bins=range(16, 50, 2), edgecolor="white")
    ax.set_title("Student ages")
    ax.set_xlabel("age")
    ax.set_ylabel("students")
    fig.tight_layout()
    return fig, "ages-histogram.png"


def chart_grade_by_course(df):
    """A boxplot, because comparing three means would hide the spread."""
    fig, ax = plt.subplots(figsize=(7, 4))
    courses = sorted(df["course"].dropna().unique())
    data = [df.loc[df["course"] == c, "final_grade"].dropna() for c in courses]
    ax.boxplot(data, tick_labels=courses)
    ax.set_title("Final grade by course")
    ax.set_ylabel("grade")
    fig.tight_layout()
    return fig, "grade-by-course.png"


def chart_enrolments_over_time(df):
    """Monthly enrolments - the chart most affected by the 70 ambiguous dates."""
    fig, ax = plt.subplots(figsize=(7, 4))
    monthly = df["enrolled_on"].dt.to_period("M").value_counts().sort_index()
    ax.bar([str(p) for p in monthly.index], monthly.values)
    ax.set_title("Enrolments by month (see the caveat in the README)")
    ax.set_ylabel("students")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig, "enrolments-by-month.png"


CHART_FUNCTIONS = [
    chart_grade_histogram,
    chart_age_distribution,
    chart_grade_by_course,
    chart_enrolments_over_time,
]


def main():
    df = load()
    CHARTS.mkdir(exist_ok=True)

    print(f"{len(df)} rows\n")
    print("DISTRIBUTIONAL SUMMARY")
    print("=" * 72)
    stats = [describe_shape(df[c], c) for c in ["final_grade", "age", "fee_paid"]]
    frame = pd.DataFrame(stats).set_index("column")
    print(frame.to_string())

    print("\nSHAPE")
    for row in stats:
        print(f"  {row['column']:<14} {row['shape']}")

    for function in CHART_FUNCTIONS:
        fig, name = function(df)
        fig.savefig(CHARTS / name, dpi=120)
        plt.close(fig)
        print(f"wrote charts/{name}")

    print(
        "\nNow answer the question in worksheets/distribution-notes.md: which "
        "of these means is misleading, and what would you report instead?"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
