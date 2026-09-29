# Data Model And Identity

## Identity rules

`school` is the durable product entity; `school_unit_identifier` records time-bounded source identities. The Skolverket eight-digit school-unit code is canonical for import/joining, but a changed code is never merged solely by similar name/address. Automatic links require an explicit authority relationship or exact high-confidence evidence; ambiguous reorganizations enter a review queue. A school unit is not assumed to equal a physical campus.

## Core tables

- `source`: owner, dataset, documentation/licence URLs, attribution, connector/schema versions.
- `source_artifact`: source, URL/query, retrieved/published periods, checksum, media type, storage key, licence snapshot, status.
- `import_run`: connector/version, start/end, artifact, received/created/updated/rejected/missing-ID counts, schema diff, error summary.
- `raw_record`: artifact, source locator/row, raw payload, raw identifier, validation status/errors.
- `school`: internal UUID, preferred name/slug, active state, school form, municipality/county, created/updated.
- `school_unit_identifier`: school, source, identifier, valid-from/to, relationship type, confidence, evidence, reviewed-by.
- `school_name_history`: school, name, valid-from/to, source record.
- `organizer` and `school_organizer_period`: organization number, type/name/contact and dated relationship.
- `school_address`: type, address fields, WGS84/PostGIS point, coordinate source/precision, validity.
- `school_grade_period`: grade (`F`, `1`…`9`), valid-from/to, source.
- `metric_definition`: stable code, localized label/explanation, category, unit, direction, applicable grades/respondents, source definition, transformation version, caveats.
- `metric_observation`: school, definition, period/start/end, value and text value, source artifact/raw record, retrieved date, sample/denominator/response rate, suppressed/missing reason, quality flags.
- `benchmark_observation`: definition, cohort type/key, period, value/distribution, eligible count.
- `survey_observation`: either specialized fields or metric observations plus instrument/version, item/index, respondent group and grade; never flatten incompatible instruments.
- `regulatory_event`: authority, type, decision/event dates, status/severity only when sourced, URL, school identity evidence; excluded from score_v1.
- `methodology_version`: immutable ID (`score_v1`), documentation hash, effective/published date, status.
- `score_snapshot`: school, methodology, evidence cutoff/period, overall nullable, components JSON plus normalized contribution records, coverage/confidence, eligibility and reasons.
- `ranking_snapshot`: geography/category/grade filter, methodology, eligible/total counts and ordered eligible score references.
- `deterministic_insight`: rule/version, school, evidence references, localized parameters/text key, period.
- `identity_review`: proposed source→school link, evidence, status and audit trail.

## Invariants

- Raw records/artifacts are append-only; normalized corrections point to new evidence.
- Observation uniqueness includes school, metric, period, respondent/grade where relevant, and source version.
- `0`, `null`, `suppressed`, `not applicable`, and `not collected` are distinct.
- Every score contribution traces to observation(s), benchmark, transformation, weight, and methodology.
- Published snapshots are immutable; a new formula creates a new version.
- User address is not a domain entity. Comparison and fit preferences are client-local in V1.

## Import contract

Fetch → checksum/archive → validate schema → parse raw records → resolve identifiers → normalize/upsert dated facts → derive benchmarks/scores in a separate job → reconcile counts. A schema change or unexpectedly large rejection rate stops publication while preserving the last successful snapshot.
