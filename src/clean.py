"""The cleaning pipeline. One function per step of CLEANING_PLAN.md.

    python src/clean.py

No API calls. Reads data/enrolments_raw.csv, writes data/enrolments_clean.csv
and prints the before/after data quality summary.

Every function below carries the decision from the plan in its docstring.
That is not decoration: in six weeks the question will be "why does this
lowercase the email but not the name?", and the answer needs to be next to
the code that does it.

Order matters and is fixed by the plan:
    strip -> nulls -> types -> categories -> dates -> duplicates -> impossible
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent.parent
RAW = ROOT / "data" / "enrolments_raw.csv"
CLEAN = ROOT / "data" / "enrolments_clean.csv"

# Text that means "missing" but is stored as data.
MISSING_DISGUISES = ["", "   ", "N/A", "n/a", "NA", "na", "-", "null", "NULL"]

# Step 4: explicit, not a lowercase(). "CS" does not lowercase into
# "computer science", and a map fails loudly on a spelling nobody expected.
COURSE_MAP = {
    "data science": "Data Science",
    "computer science": "Computer Science",
    "comp sci": "Computer Science",
    "cs": "Computer Science",
    "engineering": "Engineering",
    "eng.": "Engineering",
}

VALID_AGE = (16, 80)
VALID_GRADE = (0.0, 100.0)

TEXT_COLUMNS = ["first_name", "last_name", "course", "campus", "email"]


# --- step 1 --------------------------------------------------------------

def strip_and_fix_encoding(df):
    """Strip whitespace; replace non-breaking spaces and smart apostrophes.

    First, because everything downstream compares strings. Deduplicating or
    grouping before this treats " Data Science " and "Data Science" as two
    different things.
    """
    for column in TEXT_COLUMNS:
        df[column] = (
            df[column]
            .astype("string")
            .str.replace(" ", " ", regex=False)   # non-breaking space
            .str.replace("’", "'", regex=False)   # smart apostrophe
            .str.strip()
        )
    return df


# --- step 2 --------------------------------------------------------------

def convert_missing_disguises(df):
    """Turn "N/A", "", "   " and friends into real nulls.

    DECISION: mark, do not impute. Filling 18 missing grades with the mean
    would invent those students' performance, and Week 9's distribution work
    would then be measuring our arithmetic rather than the cohort.
    """
    for column in TEXT_COLUMNS:
        df[column] = df[column].replace(MISSING_DISGUISES, pd.NA)
    return df


# --- step 3 --------------------------------------------------------------

def fix_types(df):
    """fee_paid is text with currency symbols and commas. Make it an integer.

    "Rs 48,000", "48,000" and "48000" are one fee written three ways, and
    none of them can be compared or summed while they are strings.
    """
    df["fee_paid"] = (
        df["fee_paid"]
        .astype("string")
        .str.replace("Rs", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df["fee_paid"] = pd.to_numeric(df["fee_paid"], errors="coerce").astype("Int64")
    df["final_grade"] = pd.to_numeric(df["final_grade"], errors="coerce")
    df["age"] = pd.to_numeric(df["age"], errors="coerce").astype("Int64")
    return df


# --- step 4 --------------------------------------------------------------

def standardise_courses(df):
    """Map every spelling of a course to one canonical value.

    DECISION: an explicit map, not .str.lower(). Lowercasing turns "CS" into
    "cs", not into "computer science". The map is longer and is the only
    version that is right - and it leaves an unrecognised spelling as null
    rather than silently creating a thirteenth category.
    """
    df["course"] = df["course"].str.lower().str.strip().map(COURSE_MAP).astype("string")
    return df


# --- step 5 --------------------------------------------------------------

def parse_dates(df):
    """Parse enrolled_on, day-first, and count what stays ambiguous.

    DECISION: the UK/US ambiguity is NOT solvable. 03/04/2025 is 3 April or
    4 March and nothing in the data says which. We parse day-first, count the
    rows where both readings are possible, and report that number. The number
    is the finding - anyone doing monthly analysis on this column needs it.
    """
    raw = df["enrolled_on"].astype("string")

    slash = raw.str.match(r"^\s*\d{1,2}/\d{1,2}/\d{4}\s*$", na=False)
    first = pd.to_numeric(raw.str.split("/").str[0], errors="coerce")
    second = pd.to_numeric(raw.str.split("/").str[1], errors="coerce")
    ambiguous = int((slash & (first <= 12) & (second <= 12)).sum())

    df["enrolled_on"] = pd.to_datetime(raw, dayfirst=True, format="mixed", errors="coerce")
    return df, ambiguous


# --- step 6 --------------------------------------------------------------

def remove_duplicates(df):
    """Drop exact duplicates. Report near-duplicates; do not drop them.

    DECISION: near-duplicates (same row, email differing only by case) are
    reported, not removed. We do not know whether they are a broken export or
    two real records. A cleaning step that silently deletes real data is
    worse than the duplicate it removed.
    """
    exact = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()

    lowered = df.assign(email=df["email"].str.lower())
    near = int(lowered.duplicated().sum())

    return df, exact, near


# --- step 7 --------------------------------------------------------------

def null_impossible_values(df):
    """Flag impossible values by nulling the VALUE, not dropping the ROW.

    These pass every type check: age 999 is a valid integer. Only domain
    knowledge catches them, which is why this step cannot be automated away.

    DECISION: null the cell, keep the row. A student with an impossible age
    still has a valid grade and fee. Dropping the row throws away four good
    values to remove one bad one.
    """
    counts = {}

    bad_age = ~df["age"].between(*VALID_AGE) & df["age"].notna()
    counts["age"] = int(bad_age.sum())
    df.loc[bad_age, "age"] = pd.NA

    bad_grade = ~df["final_grade"].between(*VALID_GRADE) & df["final_grade"].notna()
    counts["final_grade"] = int(bad_grade.sum())
    df.loc[bad_grade, "final_grade"] = pd.NA

    bad_fee = (df["fee_paid"] < 0) & df["fee_paid"].notna()
    counts["fee_paid"] = int(bad_fee.sum())
    df.loc[bad_fee, "fee_paid"] = pd.NA

    return df, counts


# --- the pipeline --------------------------------------------------------

def clean(df):
    """Run every step in the order the plan fixes. Returns (df, report)."""
    report = {"rows_in": len(df), "nulls_before": df.isna().sum().to_dict()}
    report["courses_before"] = int(df["course"].nunique())

    df = strip_and_fix_encoding(df)
    df = convert_missing_disguises(df)
    df = fix_types(df)
    df = standardise_courses(df)
    df, report["ambiguous_dates"] = parse_dates(df)
    df, report["exact_duplicates"], report["near_duplicates"] = remove_duplicates(df)
    df, report["impossible"] = null_impossible_values(df)

    report["rows_out"] = len(df)
    report["nulls_after"] = df.isna().sum().to_dict()
    report["courses_after"] = int(df["course"].nunique())
    return df, report


def summary_table(report):
    """The before/after data quality summary the assessment asks for."""
    lines = [
        "DATA QUALITY SUMMARY",
        "=" * 56,
        f"{'rows in':<34}{report['rows_in']:>10}",
        f"{'rows out':<34}{report['rows_out']:>10}",
        f"{'exact duplicates removed':<34}{report['exact_duplicates']:>10}",
        f"{'near-duplicates (reported only)':<34}{report['near_duplicates']:>10}",
        f"{'distinct courses before':<34}{report['courses_before']:>10}",
        f"{'distinct courses after':<34}{report['courses_after']:>10}",
        f"{'ambiguous dates (UK/US unresolvable)':<34}{report['ambiguous_dates']:>10}",
        "",
        f"{'impossible values nulled':<34}",
    ]
    for column, count in report["impossible"].items():
        lines.append(f"  {column:<32}{count:>10}")

    lines += ["", f"{'nulls per column':<34}{'before':>10}{'after':>10}"]
    for column in report["nulls_before"]:
        before = report["nulls_before"][column]
        after = report["nulls_after"][column]
        lines.append(f"  {column:<32}{before:>10}{after:>10}")

    return "\n".join(lines)


def main():
    if not RAW.exists():
        print(f"Cannot find {RAW}. Run: python tools/make_messy_data.py")
        return 1

    df = pd.read_csv(RAW, dtype=str, keep_default_na=False)
    cleaned, report = clean(df)
    cleaned.to_csv(CLEAN, index=False)

    print(summary_table(report))
    print(f"\nWritten to {CLEAN}")
    print("\nNote: rows out < rows in only by the exact duplicates. Cleaning")
    print("removes errors, not data - impossible values were nulled, not dropped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
