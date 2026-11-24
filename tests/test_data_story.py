"""Tests for the data story. No API calls."""

import json
import sys
from pathlib import Path

import matplotlib
import pandas as pd
import pytest

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from data_story import CHARTS_IN_ORDER, FOCUS, FOCUS_CAMPUS, OTHER, colours_for, findings, load


@pytest.fixture(scope="module")
def df():
    try:
        return load()
    except SystemExit:
        pytest.skip("data/enrolments_clean.csv not present")


# --- the story -----------------------------------------------------------

def test_there_are_four_charts_in_argument_order():
    """Context, claim, evidence, caveat - the order an argument goes in,
    not the order the analysis happened in."""
    assert [f.__name__ for f in CHARTS_IN_ORDER] == [
        "chart_1_context",
        "chart_2_claim",
        "chart_3_evidence",
        "chart_4_caveat",
    ]


def test_all_four_charts_build_and_are_not_empty(df, tmp_path):
    for function in CHARTS_IN_ORDER:
        figure, name = function(df)
        figure.savefig(tmp_path / name)
        plt.close(figure)
        assert (tmp_path / name).stat().st_size > 1000, f"{name} looks empty"


def test_the_claim_chart_axis_is_not_truncated(df):
    """A truncated y-axis turns a 6-point gap into an apparent collapse,
    with every number on the chart still true. It is the commonest
    honest-looking lie in data communication, so it gets a test."""
    from data_story import chart_2_claim

    figure, _ = chart_2_claim(df)
    bottom, _top = figure.axes[0].get_ylim()
    plt.close(figure)
    assert bottom == 0, "y-axis must start at zero on a comparison chart"


def test_colour_marks_the_campus_under_discussion(df):
    campuses = ["Chennai", "Coimbatore", FOCUS_CAMPUS]
    colours = colours_for(campuses)
    assert colours.count(FOCUS) == 1
    assert colours.count(OTHER) == 2


# --- the findings the brief quotes ---------------------------------------

def test_findings_reports_a_real_gap(df):
    result = findings(df)
    assert result["gap"] > 0
    assert result["best"] != result["worst"]


def test_the_caveat_is_real_missing_data_is_not_evenly_spread(df):
    """The whole point of chart 4. If missingness were even, there would be
    no caveat and the story would be a much easier one to tell."""
    result = findings(df)
    percentages = result["missing_pct"]
    assert max(percentages.values()) > 3 * min(percentages.values())


def test_the_worst_campus_is_also_the_least_complete(df):
    """The finding that makes the brief honest rather than just tidy."""
    result = findings(df)
    worst_missing = result["missing_pct"][result["worst"]]
    others = [v for k, v in result["missing_pct"].items() if k != result["worst"]]
    assert worst_missing > max(others)


def test_findings_are_computed_not_hardcoded(df):
    """Run it on half the data: the numbers must move."""
    half = df.iloc[: len(df) // 2]
    assert findings(half)["by_campus"]["count"].sum() < findings(df)["by_campus"]["count"].sum()


# --- the notebook --------------------------------------------------------

def test_notebook_is_valid_json_with_three_components():
    notebook = json.loads((ROOT / "analysis.ipynb").read_text(encoding="utf-8"))
    assert notebook["nbformat"] == 4
    text = json.dumps(notebook)
    for heading in ["1. Cleaning Pipeline", "2. Distributional Analysis", "3. Data Story"]:
        assert heading in text, f"notebook is missing: {heading}"


def test_every_notebook_code_cell_is_well_formed():
    notebook = json.loads((ROOT / "analysis.ipynb").read_text(encoding="utf-8"))
    for index, cell in enumerate(notebook["cells"]):
        assert cell["cell_type"] in ("markdown", "code"), index
        assert isinstance(cell["source"], list), index
        if cell["cell_type"] == "code":
            assert "outputs" in cell and "execution_count" in cell, index


def test_the_brief_is_about_400_words():
    brief = (ROOT / "TECHNICAL_BRIEF.md").read_text(encoding="utf-8")
    body = brief.split("## Claim", 1)[1].split("*(≈400 words)*", 1)[0]
    words = len(body.split())
    assert 330 <= words <= 470, f"brief body is {words} words, target 400"


def test_the_brief_follows_claim_evidence_implication():
    brief = (ROOT / "TECHNICAL_BRIEF.md").read_text(encoding="utf-8")
    positions = [brief.index(h) for h in ["## Claim", "## Evidence", "## Implication"]]
    assert positions == sorted(positions)
