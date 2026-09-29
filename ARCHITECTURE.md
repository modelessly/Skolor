# Architecture

## Platform And Stack

- Responsive, server-rendered web app; Node.js 24+ and evergreen browsers.
- Next.js App Router, React, TypeScript, Material UI v9, and Emotion (see `docs/design.md`).
- PostgreSQL/PostGIS; immutable raw artifacts in object storage.
- MapLibre GL JS behind tile adapters; Geoapify is the initial server-side geocoder behind a replaceable adapter.
- TypeScript ingestion by default; Python only when statistical work is materially clearer.
- Unit, integration, and browser tests.

These are reversible Phase 1 choices. Phase 0 provisions no cloud resources.

## Reproducible Development

- Node.js 24+ and pnpm 12.8.1; exact application dependencies and `pnpm-lock.yaml` are pinned.
- Add `.env.example` with the first integration; never include secrets.
- Exact commands belong in `README.md`.

## Initial Structure

- `src/app`: routes, server metadata, composition.
- `src/features`: discovery, profiles, comparison, rankings, fit.
- `src/theme`: Material tokens and product-owned component overrides.
- `src/domain`: identity, metrics, scores, eligibility, deterministic insights.
- `src/data`: connectors, raw schemas, normalization, import runs.
- `src/db`: schema, migrations, repositories.
- `src/i18n`: Swedish/English messages.
- `tests/fixtures`: complete, incomplete, small, renamed, closed, and unusual-grade schools.

Create folders only with their first behavior.

## Data Layers

1. Raw: immutable artifact/record, retrieval metadata, checksum.
2. Normalized: schools, organizers, identifiers, grades, definitions, observations.
3. Derived: cohorts, normalized values, coverage, confidence, deterministic insights.
4. Published: immutable methodology-versioned score snapshots and ranking eligibility.

See `docs/data-model.md`.

## State Ownership

- Viewport, filters, and selection are URL-addressable screen state.
- Home coordinates stay in session/client state and out of application storage/logs.
- Comparison IDs and fit weights persist locally; no account.
- Evidence and common scores are server-owned and immutable per methodology version.
- Loading, empty, partial, stale, and source-failure states are explicit.

## Integration Boundaries

- Skolenhetsregistret v2: canonical current/historical unit identity and coordinates; daily incremental import.
- Skolverket statistics/PxWeb: outcomes, staffing, SALSA.
- Skolinspektionen workbooks: survey observations by respondent and cycle.
- Kolada v3: secondary only for unique validated indicators; retain V-unit crosswalk.
- SCB PxWeb: context benchmarks only unless a defensible unit key exists.
- Geoapify geocoder: server-side submit-only address lookup, `GEOAPIFY_API_KEY`, no address persistence/logging, required attribution, and a replaceable adapter.
- Map: tile provider unresolved; accessible list fallback when tiles/WebGL fail.

## Reliability And Privacy

- Imports are idempotent, schema-validated, checksum-aware, auditable, and fail closed on incompatible change.
- Each run records received/created/updated/rejected counts, missing IDs, schema changes, and failures.
- Suppressed stays suppressed; null never becomes zero. Serve last successful dated data on upstream failure.
- Send an address only to the selected geocoder and retain it only for the session absent future consent.
