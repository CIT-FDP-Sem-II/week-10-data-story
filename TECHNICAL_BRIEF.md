# Technical Brief — Grade Gap Between Campuses

**To:** Director of Studies · **From:** Data Analysis · **Length:** 400 words

> The worked example. Structure: **claim → evidence → implication.** Write
> your own for your own question.

---

## Claim

Madurai students average **6.6 grade points below** the other two campuses —
64.0 against 70.6 at Chennai and 70.5 at Coimbatore. The gap is consistent
across the whole distribution, not the product of a few low scores. However,
**one in five Madurai grades is missing**, against roughly one in twenty
elsewhere, so the true size of the gap is not known and could be larger.

## Evidence

Across 306 cleaned records, mean final grades by campus are Chennai 70.6
(n=80), Coimbatore 70.5 (n=102) and Madurai 64.0 (n=84). Standard deviations
are near-identical — 11.3, 11.9 and 11.2 — so the three campuses have
similarly spread outcomes around different centres.

The boxplot (chart 3) rules out the obvious alternative explanation. If the
gap were caused by a handful of very low scores, Madurai's median would sit
close to the others with a long lower tail. It does not: the median is 62.8
against 69.6 and 71.1, and the whole box is shifted down. The gap is in the
typical student, not the worst ones.

Chart 2 uses a y-axis from 0 to 100. On a truncated axis the same 6.6-point
difference would look like a collapse rather than a difference of about nine
percent.

**The limitation is the important part of this brief.** Chart 4 shows missing
grades by campus: 20.0% at Madurai, 3.6% at Chennai, 3.8% at Coimbatore.
Those 21 Madurai students are not a random sample of the campus. If a grade is
missing because a student withdrew, the recorded mean of 64.0 already excludes
the weakest performers and the real gap is **wider**. If grades are missing
for an administrative reason unrelated to performance, 64.0 is a fair estimate.
Nothing in this dataset distinguishes the two.

A second limitation: 57 of 306 enrolment dates are ambiguous between UK and
US ordering, so no claim here involves timing.

## Implication

Two actions, in order.

**First, find out why the grades are missing at Madurai.** Until that is
known, the size of the gap cannot be stated and any intervention is being
designed against a number that may be wrong. This is a records question, not
an analysis question, and it is cheap.

**Second, treat 6.6 points as a lower bound**, not an estimate. Every
mechanism that plausibly explains missing grades at a single campus — more
withdrawals, weaker administration, a different cohort — would make the true
gap larger rather than smaller.

Do not act on the ranking of Chennai against Coimbatore. The difference is
0.1 points on samples of 80 and 102, which is noise.

*(≈400 words)*

---

## What makes this a brief and not a report

| | |
|---|---|
| **Claim first** | The reader knows the finding in sentence one. If they stop reading there, they still have it |
| **The limitation is in the claim** | Not buried in a footnote. It changes what the reader should do |
| **Numbers are specific** | "6.6 points", "20.0%", "n=80" — not "significantly lower" |
| **The alternative explanation is tested** | And named, so the reader can see it was considered |
| **Implications are actions** | "Find out why grades are missing", not "further research is warranted" |
| **It says what NOT to act on** | The 0.1-point difference is explicitly called noise |

## The sentence that earns the most marks

> *"If a grade is missing because a student withdrew, the recorded mean
> already excludes the weakest performers and the real gap is wider. If
> grades are missing for an administrative reason, 64.0 is a fair estimate.
> Nothing in this dataset distinguishes the two."*

It states both possibilities, says which way each one pushes the answer, and
admits the data cannot choose. That is what honest analysis reads like.
