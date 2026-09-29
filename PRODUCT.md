# Schools — Product Brief

## Product Name

Schools (working name)

## One-Sentence Description

A transparent decision-support service that helps parents in Sweden find, understand, and compare compulsory schools using authoritative public data.

## Vision

Turn fragmented Swedish school information into a trustworthy answer to: “Which schools are available to my child, and why might each be a good choice?” The product combines proximity, outcomes, context, teaching conditions, environment, and trends without hiding uncertainty or reducing a consequential family decision to a league table.

## Core User

A parent or guardian in Sweden choosing a grundskola or associated förskoleklass for a child and trying to understand credible differences among realistic nearby options.

## Core Moment

The parent has a home location and required grade, but public information is spread across agencies, spreadsheets, reports, and individual school websites.

## Problem

Discovering eligible nearby schools is cumbersome, comparisons are hard to reproduce, raw outcomes are socially confounded, and existing summaries often conceal missing data or methodology.

## Product Thesis

If authoritative school data is joined, dated, and explained in one location-first workflow, parents can make a more informed shortlist than they can from directories, anecdotes, or raw rankings alone.

## Evidence And Riskiest Assumption

- Evidence: multiple national authorities publish complementary school information through separate registers, databases, workbooks, and reports. User-demand evidence is not yet collected.
- Current alternative: municipality and school sites, Utbildningsguiden, recommendations, and manual comparisons.
- Riskiest assumption: parents will understand and trust a composite score when coverage, uncertainty, source values, and limitations are prominent.
- Smallest experiment: 5–8 moderated parent sessions using a real municipality and grade; each builds a shortlist, explains two score differences, and identifies uncertain evidence.
- Decision threshold: continue if 6/8 correctly explain the main score drivers and coverage warning and 5/8 prefer it to their current process; revise or remove the composite score if users over-trust it.
- Result and next decision: not tested.

## Emotional Goals

The product should feel trustworthy, calm, clear without being simplistic, and respectful of the decision. It should not feel like a black-box ranking, a cluttered government database, or a childish/gamified sales product.

## What This Product Is

- A location-first school discovery and comparison tool.
- A transparent interpretation layer over authoritative public data.
- A decision aid that keeps common quality and personal fit separate.

## What This Product Is Not

- A guarantee that one school is universally “best.”
- An admissions, catchment, queue, or placement calculator.
- An AI-generated evaluator or substitute for visiting a school.

## V1 User Promise

Given a Swedish address and required grade, a parent can find plausible nearby active schools, inspect dated evidence and transparent quality components, and compare up to four schools without missing data being presented as poor performance.

## V1 Scope

### Included

- All active Swedish grundskolor, including associated förskoleklass, municipal and independent, with actual offered grades.
- Address-based map/list discovery, radius and core filters, school summaries, profiles, and straight-line distance.
- Versioned common score only where evidence meets published eligibility rules; component detail, coverage, dates, caveats, and sources everywhere.
- Comparison for up to four schools and locally stored weighting preferences shown separately as “My Fit.”
- Municipality/city pages that disclose how many schools are eligible to rank.
- Swedish and English string architecture; Swedish becomes the default before public launch.

### Explicitly Excluded

- Förskola, gymnasium, university, admissions probability, catchments, queue availability, and municipality placement rules.
- Accounts, permanent address storage, travel-time calculation, AI-generated facts or scores, and live agency queries on page load.
- Inspection findings in `score_v1` until structure, comparability, and reuse terms are validated.

## Core Workflows

### Discover nearby schools

1. Enter an address and choose the required grade.
2. Inspect active matching schools on a synchronized map/list; change bounds, radius, filters, or sorting.
3. Open a summary showing distance, grades, type, score or “not enough data,” and key evidence.

### Understand a school

1. Open a stable school profile.
2. Inspect components, actual metrics, periods, sample/coverage information, comparisons, and deterministic insights.
3. Follow source/method links and distinguish unavailable data from poor performance.

### Compare and personalize

1. Select two to four schools.
2. Compare scores and underlying measures.
3. Adjust local fit weights while the unchanged common score stays visible.

## Success Criteria

- Address → grade → shortlist → evidence works on desktop/mobile, including empty and partial-data states.
- Every evaluative value has a source, period, methodology version, and reproducible transformation.
- Missing/suppressed values never become zero; ineligible schools remain discoverable but unranked.
- The parent comprehension experiment meets its threshold.
- Import, identity, score, missingness, ranking, geography, grade, comparison, and deterministic-insight tests pass on representative fixtures.

## Open Questions

- Which geocoder/tile provider best satisfies Swedish address quality, privacy, attribution, reliability, and budget?
- Can every intended Skolverket bulk output and Skolenkäten workbook be reused in a public commercial derivative under confirmed terms?
- How should cohorts/eligibility change after the audit found only 43.6% complete cases and sharp size/type differences?
- Should an overall score exist at all after independent statistical and parent-comprehension review of the measured sensitivity?
