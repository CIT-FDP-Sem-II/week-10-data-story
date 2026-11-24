"""The four-chart data story. No API calls.

    python src/data_story.py

Question: do students at one campus do worse, and if so by how much?

Four charts, in the order an argument goes - not in the order the analysis
happened:

    1. CONTEXT   what the grades look like overall
    2. CLAIM     the gap, shown as plainly as possible
    3. EVIDENCE  is the gap real, or is it one or two outliers?
    4. CAVEAT    what we do not know, and why it matters

Chart 4 is the one most students leave out, and it is the one that makes the
other three trustworthy. A story with no caveat chart is a sales pitch.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "enrolments_clean.csv"
CHARTS = ROOT / "charts"

# One colour for the campus under discussion, one for everything else. Using
# a different colour per campus would be prettier and would say nothing - the
# reader should be able to see the point without reading the legend.
FOCUS = "#C44E52"
OTHER = "#B0B0B0"
FOCUS_CAMPUS = "Madurai"


def load():
    if not DATA.exists():
        raise SystemExit(
            f"Cannot find {DATA}. Copy enrolments_clean.csv from your Week 8 repo."
        )
    return pd.read_csv(DATA, parse_dates=["enrolled_on"])


def colours_for(campuses):
    return [FOCUS if c == FOCUS_CAMPUS else OTHER for c in campuses]


# --- 1. context ----------------------------------------------------------

def chart_1_context(df):
    """What do the grades look like at all? Orient the reader before arguing."""
    fig, ax = plt.subplots(figsize=(7, 4))
    grades = df["final_grade"].dropna()
    ax.hist(grades, bins=22, color=OTHER, edgecolor="white")
    ax.axvline(grades.mean(), color="black", linestyle="--",
               label=f"mean {grades.mean():.1f}")
    ax.set_title("1. Final grades across all campuses")
    ax.set_xlabel("final grade")
    ax.set_ylabel("students")
    ax.legend(frameon=False)
    fig.tight_layout()
    return fig, "01-context.png"


# --- 2. claim ------------------------------------------------------------

def chart_2_claim(df):
    """The gap. A bar chart because the reader needs to compare three numbers.

    The y-axis starts at zero. A truncated axis would make a 6-point gap look
    like a collapse, which is the most common way a chart lies while every
    number on it stays true.
    """
    fig, ax = plt.subplots(figsize=(7, 4))
    means = df.groupby("campus")["final_grade"].mean().sort_values()
    ax.bar(means.index, means.values, color=colours_for(means.index))
    ax.set_ylim(0, 100)                       # NOT truncated - see docstring
    ax.set_title("2. Mean final grade by campus")
    ax.set_ylabel("mean final grade")
    for name, value in means.items():
        ax.text(name, value + 2, f"{value:.1f}", ha="center")
    fig.tight_layout()
    return fig, "02-claim.png"


# --- 3. evidence ---------------------------------------------------------

def chart_3_evidence(df):
    """Is the gap real, or two outliers dragging a mean?

    A boxplot shows the whole distribution per campus. If the boxes overlap
    almost completely, the difference in means is not worth reporting however
    big the bars looked.
    """
    fig, ax = plt.subplots(figsize=(7, 4))
    campuses = sorted(df["campus"].dropna().unique())
    data = [df.loc[df["campus"] == c, "final_grade"].dropna() for c in campuses]
    boxes = ax.boxplot(data, tick_labels=campuses, patch_artist=True)
    for patch, colour in zip(boxes["boxes"], colours_for(campuses)):
        patch.set_facecolor(colour)
    ax.set_title("3. Spread of grades by campus - is the gap real?")
    ax.set_ylabel("final grade")
    fig.tight_layout()
    return fig, "03-evidence.png"


# --- 4. caveat -----------------------------------------------------------

def chart_4_caveat(df):
    """What we do not know. The chart that makes the other three honest.

    Missing grades are not spread evenly. The campus with the lowest mean is
    also the one with by far the most missing grades, so the gap we measured
    is computed from the students we happen to have.
    """
    fig, ax = plt.subplots(figsize=(7, 4))
    missing = df[df["final_grade"].isna()]["campus"].value_counts()
    total = df["campus"].value_counts()
    percent = (missing / total * 100).reindex(sorted(total.index)).fillna(0)

    ax.bar(percent.index, percent.values, color=colours_for(percent.index))
    ax.set_title("4. Percent of grades MISSING, by campus")
    ax.set_ylabel("% of students with no grade")
    for name, value in percent.items():
        ax.text(name, value + 0.4, f"{value:.0f}%", ha="center")
    fig.tight_layout()
    return fig, "04-caveat.png"


CHARTS_IN_ORDER = [chart_1_context, chart_2_claim, chart_3_evidence, chart_4_caveat]


def findings(df):
    """The numbers the brief has to quote. Computed, not remembered."""
    by_campus = df.groupby("campus")["final_grade"].agg(["count", "mean", "median", "std"])
    missing = df[df["final_grade"].isna()]["campus"].value_counts()
    total = df["campus"].value_counts()

    best = by_campus["mean"].idxmax()
    worst = by_campus["mean"].idxmin()

    return {
        "by_campus": by_campus.round(1),
        "gap": round(by_campus["mean"].max() - by_campus["mean"].min(), 1),
        "best": best,
        "worst": worst,
        "missing_pct": (missing / total * 100).round(1).to_dict(),
        "worst_missing_pct": round(missing.get(worst, 0) / total[worst] * 100, 1),
    }


def main():
    df = load()
    CHARTS.mkdir(exist_ok=True)

    result = findings(df)
    print("GRADES BY CAMPUS")
    print(result["by_campus"].to_string())
    print(f"\ngap between {result['best']} and {result['worst']}: "
          f"{result['gap']} points")
    print(f"missing grades (% of campus): {result['missing_pct']}")

    for function in CHARTS_IN_ORDER:
        fig, name = function(df)
        fig.savefig(CHARTS / name, dpi=120)
        plt.close(fig)
        print(f"wrote charts/{name}")

    print(
        f"\nThe caveat: {result['worst']} has the lowest mean AND "
        f"{result['worst_missing_pct']}% missing grades. The gap is measured "
        f"on the students we happen to have."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
