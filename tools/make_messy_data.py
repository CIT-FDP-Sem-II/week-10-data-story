"""Generate the deliberately messy dataset. No API calls.

    python tools/make_messy_data.py

Writes data/enrolments_raw.csv - 300 rows of module enrolment records with
every data quality problem from the lecture deliberately planted in it:

    completeness   missing values, blank strings, "N/A" as text
    consistency    the same course written four ways; mixed date formats
    accuracy       ages of 0 and 150; a negative fee; a grade of 200
    uniqueness     exact duplicate rows, and near-duplicates
    types          numbers stored as text, with currency symbols and commas
    encoding       smart quotes and non-breaking spaces in names

The faults are seeded with a fixed random seed, so everyone in the cohort
gets the same dataset and can compare answers. The answer key is in
data/PLANTED_FAULTS.md - do not read it until you have done the audit.
"""

import csv
import random
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"
SEED = 20260224
ROWS = 300

FIRST = ["Aisha", "Ben", "Chen", "Divya", "Eli", "Fatima", "Grace", "Hassan",
         "Ingrid", "Jai", "Kemi", "Liam", "Mei", "Noor", "Omar", "Priya",
         "Quinn", "Ravi", "Sofia", "Tom"]
LAST = ["Ahmed", "Brown", "Chen", "Davies", "Evans", "Farah", "Garcia",
        "Hughes", "Iqbal", "Jones", "Khan", "Lewis", "Murphy", "Nkemdirim",
        "Okafor", "Patel", "Quinn", "Rossi", "Smith", "Tanaka"]

# The same three courses, written inconsistently. This is the single most
# common real-world data quality problem and the one students notice last.
COURSE_VARIANTS = {
    "Data Science": ["Data Science", "data science", "DATA SCIENCE", " Data Science "],
    "Computer Science": ["Computer Science", "Comp Sci", "computer science", "CS"],
    "Engineering": ["Engineering", "engineering", "Eng.", "ENGINEERING"],
}

CAMPUSES = ["Chennai", "Coimbatore", "Madurai"]

# Real structure, deliberately put in so that Weeks 9 and 10 have something
# true to find. None of this is a data quality fault - it is signal.
#
#   fee depends on COURSE   -> explains why fee_paid is multimodal
#   grade depends on CAMPUS -> the finding the Week 10 data story argues
#   missing grades cluster at one campus -> the caveat that makes the story
#                                           honest rather than just tidy
COURSE_FEES = {"Data Science": 55000, "Computer Science": 48000, "Engineering": 32000}
CAMPUS_GRADE_MEAN = {"Chennai": 72, "Coimbatore": 70, "Madurai": 62}
CAMPUS_MISSING_WEIGHT = {"Chennai": 1, "Coimbatore": 1, "Madurai": 4}


def messy_date(rng, year=2025):
    """Four date formats in one column. All four occur in real exports."""
    month, day = rng.randint(1, 12), rng.randint(1, 28)
    return rng.choice([
        f"{year}-{month:02d}-{day:02d}",      # ISO
        f"{day:02d}/{month:02d}/{year}",      # UK
        f"{month:02d}/{day:02d}/{year}",      # US - ambiguous against UK
        f"{day} {['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][month-1]} {year}",
    ])


def messy_fee(rng, amount):
    """Numbers stored as text, three ways."""
    return rng.choice([
        str(amount),
        f"Rs {amount:,}",
        f"{amount:,}",
    ])


def build_rows(rng):
    rows = []
    for student_id in range(1001, 1001 + ROWS):
        canonical = rng.choice(list(COURSE_VARIANTS))
        campus = rng.choice(CAMPUSES)
        first, last = rng.choice(FIRST), rng.choice(LAST)

        # Real signal: grade varies by campus, fee is set by course.
        grade = rng.gauss(CAMPUS_GRADE_MEAN[campus], 11)
        grade = round(min(99.0, max(31.0, grade)), 1)

        row = {
            "student_id": student_id,
            "first_name": first,
            "last_name": last,
            "course": rng.choice(COURSE_VARIANTS[canonical]),
            "campus": campus,
            "enrolled_on": messy_date(rng),
            "age": rng.randint(18, 45),
            "fee_paid": messy_fee(rng, COURSE_FEES[canonical]),
            "final_grade": grade,
            "email": f"{first.lower()}.{last.lower()}@example.edu",
        }
        rows.append(row)

    # --- plant the faults ------------------------------------------------

    # Completeness: missing values in three different disguises.
    #
    # Missing grades are NOT spread evenly - they cluster at Madurai, the
    # campus with the lowest mean. That makes the Week 10 data story honest:
    # the campus that looks worst is also the one we know least about, so the
    # true gap could be larger or smaller than the charts show. A dataset
    # where missingness is random would teach the opposite lesson.
    weights = [CAMPUS_MISSING_WEIGHT[rows[i]["campus"]] for i in range(ROWS)]
    blanked = set()
    while len(blanked) < 24:
        blanked.add(rng.choices(range(ROWS), weights=weights, k=1)[0])
    for index in blanked:
        rows[index]["final_grade"] = ""
    for index in rng.sample(range(ROWS), 12):
        rows[index]["campus"] = "N/A"          # text that looks like data
    for index in rng.sample(range(ROWS), 9):
        rows[index]["email"] = "   "           # whitespace that looks like data

    # Accuracy: impossible values that pass a type check.
    for index in rng.sample(range(ROWS), 5):
        rows[index]["age"] = rng.choice([0, 1, 150, 999])
    for index in rng.sample(range(ROWS), 3):
        rows[index]["final_grade"] = rng.choice([-10.0, 200.0, 150.5])
    rows[rng.randrange(ROWS)]["fee_paid"] = "-32000"

    # Encoding: smart quotes and non-breaking spaces in names.
    for index in rng.sample(range(ROWS), 7):
        rows[index]["last_name"] = "O’" + rows[index]["last_name"]
    for index in rng.sample(range(ROWS), 5):
        rows[index]["first_name"] = rows[index]["first_name"] + " "

    # Uniqueness: 10 exact duplicates and 6 near-duplicates. The near ones
    # are the interesting case - drop_duplicates() will not touch them.
    for index in rng.sample(range(ROWS), 10):
        rows.append(dict(rows[index]))
    for index in rng.sample(range(ROWS), 6):
        near = dict(rows[index])
        near["email"] = near["email"].upper()
        rows.append(near)

    rng.shuffle(rows)
    return rows


def main():
    rng = random.Random(SEED)
    rows = build_rows(rng)
    DATA.mkdir(exist_ok=True)
    target = DATA / "enrolments_raw.csv"

    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {target} - {len(rows)} rows, {len(rows[0])} columns")
    print("Audit it before you read data/PLANTED_FAULTS.md.")


if __name__ == "__main__":
    main()
