# Data Source Audit

Research snapshot: 2026-09-29. This is a source-level audit, not yet a national coverage audit. URLs are primary sources unless noted.

The technical national coverage audit is now available in [`research/coverage-audit-2026-09-29.md`](research/coverage-audit-2026-09-29.md), with machine-readable results beside it. It measures 4,624 active grundskola units, selected four-year PxWeb measures, and four 2026 survey workbooks. Source-rights verification remains incomplete.

## Decision summary

| Source | Intended use | School-unit data | Join | Status |
| --- | --- | --- | --- | --- |
| Skolverket Skolenhetsregistret v2 | canonical identity, status, organizer, grades, address/coordinates | Yes | 8-digit `schoolUnitCode` | Adopt |
| Skolverket statistics / PxWeb / downloads | results, staffing, pupils, multi-year evidence | Yes for many outputs | school-unit code where exported | Adopt after file audit |
| Skolverket SALSA | grade-9 context-adjusted residuals/background | Yes, eligibility-limited | school-unit code | Conditional component only |
| Skolinspektionen Skolenkäten | perceived environment/teaching by respondent/cycle | Yes in annual workbooks | verify school-unit code and changes per workbook | Adopt after schema/license audit |
| SCB PxWeb | municipality/context benchmarks | Mostly aggregate for this use | municipality code; never infer a school join | Context only |
| Kolada API v3 | candidate unique municipality/unit KPIs | Some, via V15 units | separate V-ID crosswalk | Secondary/conditional |
| Geoapify Geocoding API | transient parent-address lookup | Yes, address → coordinate | user submit only | Initial provider; free plan/attribution limits |
| Lantmäteriet open geodata | address/geographic reference data | Not a school metric source | coordinates/address | Candidate for future Swedish address index |
| Skolinspektionen decisions | regulatory events | Search/document oriented | unit/name/date resolution | Research later; exclude score_v1 |

## Skolverket: Skolenhetsregistret v2

- Owner/docs: [Skolverket API page](https://www.skolverket.se/om-skolverket/oppna-data/api-for-skolenhetsregistret), [Swagger](https://api.skolverket.se/skolenhetsregistret/swagger-ui/index.html).
- Endpoint: `GET https://api.skolverket.se/skolenhetsregistret/v2/school-units` and `/{schoolUnitCode}`; JSON/XML through `Accept`.
- Tested: live detail request for unit `59900714` returned code, active status, school types, actual grades, organizer relationship links, municipality, address, WGS84/SWEREF coordinates, contact fields, and start date. OpenAPI also documents `search_date`, active/ceased status filters, and `meta_modified_after` for increments.
- Cadence/history: daily; v2 active since 2024-12-13 and exposes ceased units. `search_date` supports dated detail, but this is not a substitute for storing snapshots.
- Identity: eight-digit random school-unit code. Treat as the canonical external key, not as a meaningful number. Preserve aliases/relationships for reorganizations rather than assuming a code is a permanent physical campus.
- Geography: unit-level visiting address and coordinates are present when reported. Profile national absence/quality before relying on them.
- Missingness/caveats: organizer-reported current organization; null fields are omitted from responses; one “school” concept may not equal one campus or historical organization.
- Reuse: Skolverket describes open data as free to reuse and links a Creative Commons source licence. Record attribution and archive the exact licence text/version with each connector before commercial release.
- Ingestion: daily idempotent full bootstrap; incremental fetch by modification timestamp; immutable raw JSON, checksum, schema version; normalize only validated grundskola/förskoleklass units.
- Measured 2026-09-29: daily XLSX contained 4,624 unique active grundskola units and a complete visiting address for all 4,624. All 120 units in a deterministic API-detail sample had WGS84 coordinates; this is a sample, not a national completeness claim.

## Skolverket: statistics, national quality-system PxWeb, and downloads

- Discovery: [statistics search](https://www.skolverket.se/statistik-och-utvarderingar/statistik-om-forskola-skola-och-vuxenutbildning), [grundskola PxWeb table](https://statistikdatabasen.skolverket.se/PxWeb/pxweb/sv/Skolverkets_statistikdatabas/Skolverkets_statistikdatabas__Underlag_for_analys_inom_det_nationella_kvalitetssystemet__Grundskola/Grundskola.px/).
- Level/fields: school-unit outputs include selected grade results, national tests, merit value, eligibility/knowledge requirements, pupils, staffing/qualified teachers, and selected survey measures. Exact availability depends on grade, measure, period, and disclosure rules.
- Formats/access: bulk “all schools” downloads and PxWeb exports/API-compatible JSON/CSV/XLSX. Do not scrape visual school pages when a file/table exists.
- History: graph pages demonstrate up to ten years for some measures; the national quality-system table currently exposes a much shorter window. Audit each canonical bulk series rather than claiming a uniform range.
- Identifier: exported school-unit code is the expected join; verify type/leading zero preservation for every file.
- Missingness/caveats: small cohorts are suppressed; definitions and maximum merit value changed historically; school forms/grade configurations limit applicability; current PxWeb quality-system table is labelled not official statistics and is updated continuously.
- Reuse: Skolverket open-data statement is favorable, but the exact terms attached to every bulk/statistical output must be recorded before publication.
- Ingestion: pin URL, retrieval time, checksum, period and definition; keep suppression markers; schema-contract test headers and value domains; never parse display HTML as canonical data.
- Measured selected metrics: pupil count 97.5%, qualified-teacher share 94.0%, and pupils/teacher 96.9% of active units had a latest value. Grade-6 all-subject attainment covered 52.3% of grade-6-offering units; grade-9 all-subject attainment 71.7%; grade-9 gymnasium eligibility 64.6%. Applicability denominators use current offered grades and should be sensitivity-tested against the observation-year configuration.

## Skolverket: SALSA

- Owner/method: [SALSA methodology](https://www.skolverket.se/statistik-och-utvarderingar/statistik-om-forskola-och-skola/sok-statistik-om-forskola-skola-och-vuxenutbildning/salsa-en-statistisk-modell).
- Level/coverage: school unit, only pupils finishing grade 9; at least 15 pupils and background data for at least 75%.
- Fields: actual and model-estimated merit value and share passing all subjects; context uses parental education, share boys, and new/unknown-background pupils.
- History: current and historical outputs appear in Skolverket statistics/SIRIS; exact machine-readable range must be measured.
- Caveat with product consequence: Skolverket says SALSA cannot alone answer which school is better and must not be used to rank schools. It omits other influences and is not a causal value-added estimate.
- Use: show actual/model/residual and official caveat; only a capped contextual component for eligible grade-9 schools after sensitivity review. Never impute it for F–6 schools.
- Access finding: the public SIRIS application exposes per-school selection/reports, but no supported national machine-readable bulk export was verified. Do not automate the interactive APEX application as a production connector without written support/permission.

## Skolinspektionen: Skolenkäten

- Owner/results: [Skolinspektionen results](https://www.skolinspektionen.se/skolenkaten/resultat-fran-skolenkaten/), with annual school-level XLSX files by respondent group and historic 2015–2020/2021 onward pages.
- Current structure: grade 5 pupils, grade 8 pupils, guardians (förskoleklass/grundskola), and teaching staff; themes include teaching/learning, safety/study environment, and pedagogical leadership.
- Cadence: annual since spring 2021, half of schools each year; a two-year cycle covers all schools. Store survey year and respondent group, never label the latest calendar year as universal.
- Fields: published workbooks include question/index values and may include counts/response information and suppression. Exact 2026 schemas must be profiled separately for each workbook.
- Identity: Skolinspektionen states its school list comes from Skolverket’s register, but the actual code column, formatting, duplicates, and changed units must be verified.
- Missingness/caveats: perception survey, nonresponse, respondent/grade differences, anonymity/quality suppression, and incompatible questionnaire changes can limit trend comparison.
- Reuse: public download is technically accessible; explicit commercial/derivative licence was not located in this pass. Confirm with the authority or a source-specific notice before production reuse.
- Ingestion: one connector/schema per respondent/version; preserve item text, scale, index method, respondent, year, sample/response fields, suppression, and workbook checksum.
- Measured 2026 workbook joins: grade 5 had 1,640 unit codes (98.3% joined the current active grundskola extract); grade 8 864 (96.9%); guardians 2,256 (97.7%); teachers 2,258 (97.6%). Non-joins were explained by ceased, dormant, or currently non-GR units in the register rather than fuzzy name matching. Current-year active-register coverage is 18.1–47.7% depending on respondent/grade, consistent with the two-year cycle and grade applicability.

## SCB

- Owner/API: [SCB API](https://www.scb.se/en/services/open-data-api/), PxWeb statistical tables.
- Appropriate use: municipality/county/national demographic and socioeconomic context or benchmark denominators.
- Joining: municipality/region code at its published aggregation only. Do not attach area averages to a school as if they describe enrolled pupils, and do not assume SCB public tables expose unit-level pupil context.
- History/cadence: table-specific; metadata must be captured per query.
- Reuse: verify the table/API terms and attribution at implementation; avoid personal/microdata entirely.
- Ingestion: store full PxWeb query JSON, response, table metadata, unit, adjustment status, and period.

## Kolada API v3

- Owner/docs/terms: [Kolada API](https://www.kolada.se/om-oss/api/), [v3 Swagger](https://api.kolada.se/v3/docs).
- Tested: `GET /v3/kpi?title=grundskola` returned metadata including source, perspective, publication dates and `has_ou_data`; `GET /v3/ou?title=Väsby%20skola` returned V15 unit IDs and municipality codes.
- Level: municipality KPIs and selected operating-unit data. V15 means grundskola F–9 but is Kolada’s identifier, not the Skolverket code.
- Cadence/history: rolling publication; data can be revised or KPIs removed without notice.
- Reuse: free/no agreement, commercial use allowed, “Källa: Kolada” required for unmodified data; do not call transformed output “Källa: Kolada” and do not imply partnership.
- Decision: do not duplicate Skolverket measures. Consider only a unique KPI after definition/source comparison and a measured V15↔school-unit crosswalk.

## Geography, mapping, and geocoding

- Skolenhetsregistret already supplies reported WGS84 coordinates and addresses for many units.
- [Lantmäteriet open data](https://www.lantmateriet.se/oppnadata) is CC0 and commercial reuse is permitted; address/geographic products are candidates for validation or a geocoder index.
- Initial geocoder: Geoapify’s server-side forward-geocoding API. The free plan currently permits commercial use within a 3,000-credit/day allowance and requires Geoapify/underlying-source attribution. Send a user address only after explicit submit, keep the key server-side, do not log or persist the address/coordinates, and show a provider disclosure. Re-evaluate service terms, Swedish address quality, rate limits, DPA/privacy, caching/storage rights, attribution, and cost before public launch.
- Lantmäteriet remains the preferred authoritative Swedish-address candidate for a later owned address index. Do not use public OSM/Nominatim endpoints as commercial infrastructure.

## Inspections and other sources

Skolinspektionen publishes searchable decisions, but event types, severity, closure/remediation, document parsing, historical identity, and commercial reuse require a separate audit. Showing decisions as sourced events may be useful; a score penalty would imply comparability not yet established. Municipality/school websites are not national canonical metric sources and should not be scraped for scoring.

## Required next audit

RESEARCH-02 has quantified current units, grades/addresses, sampled coordinates, selected PxWeb coverage/history, survey joins, suppression markers, and a three-component availability proxy. Remaining: exact Skolenkäten commercial reuse confirmation, supported SALSA bulk access or an exclusion decision, observation-year grade history, and full `score_v1` eligibility after confidence/anchor rules.
