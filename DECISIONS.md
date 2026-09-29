# Decisions

Append-only. Supersede accepted decisions with a new entry.

## Inherited harness

Harness revision: `2026-09-23`

Standing constraints live in `AGENTS.md`. Product decisions start below.

---

## 2026-09-29: Treat provenance as a product boundary

Decision: Use Skolverket school-unit code as canonical external identity, retain source identifiers/raw artifacts, and separate raw, normalized, derived, and published layers.

Reasoning: Skolenhetsregistret v2 is authoritative and daily updated; explanations must remain reproducible across interpretation changes.

Tradeoffs: more storage/import discipline, but corrections and methodology revisions stay auditable.

Status: Accepted

---

## 2026-09-29: Gate composite scoring

Decision: Do not publish a composite until a national coverage audit, sensitivity/fairness analysis, and parent comprehension test pass. SALSA is only a separately explained grade-9 contextual signal, never a standalone rank.

Reasoning: sources differ in cycle, suppression, and population; Skolverket says SALSA alone cannot determine quality or rank schools.

Tradeoffs: the first public experience may be evidence-led comparison without an overall score.

Status: Accepted

---

## 2026-09-29: Use a replaceable web/data stack

Decision: Target Next.js/React/TypeScript, PostgreSQL/PostGIS, MapLibre adapters, Tailwind, and shadcn/ui/Radix. Provision no infrastructure in Phase 0.

Reasoning: supports indexable routes, geospatial search, accessible composition, and one deployable app while keeping providers replaceable.

Tradeoffs: PostGIS/mapping add operations; exact vendors remain open.

Status: Accepted

---

## 2026-09-29: Use Google Material Design with Material UI

Decision: Supersede the shadcn/ui, Radix, and Tailwind UI-foundation portion of “Use a replaceable web/data stack.” Use Google Material Design with Material UI v9 and Emotion.

Reasoning: The user selected Material Design. Material UI is actively supported, production-ready, and integrates with Next.js. Google’s Material Web library is in maintenance mode. Material UI currently implements Material Design 2, so Material 3 guidance informs product tokens and adaptive behavior without claiming full M3 component parity.

Tradeoffs: Material UI adds Emotion and a recognizable default language that needs careful theming. It offers broader maintained React coverage than official Material Web, while latest Material 3 components may need product-owned adaptations.

Status: Accepted; supersedes the UI-library portion of the earlier web-stack decision.

---

## 2026-09-29: Continue withholding an overall score after quantitative diagnostics

Decision: Keep the Common School Score and ordinal rankings disabled. Continue with evidence profiles and comparisons while the remaining validation gates are resolved.

Reasoning: The first reproducible diagnostic found only 43.6% complete-case coverage, material rank movement under plausible weights, socioeconomic association, and strongly uneven eligibility by school size and organizer. These are research warnings, not parameters to tune away.

Tradeoffs: V1 may be less superficially simple and cannot promise a universal league table. It avoids presenting unstable or selectively available evidence as precise comparative quality.

Status: Accepted

---

## 2026-09-29: Pin the initial web scaffold dependencies

Decision: Pin Next.js 16.3.7, React/React DOM 19.3.0, Material UI and its Next.js integration 9.4.0, Emotion 11.14.x, TypeScript 6.0.3, ESLint 9.39.5, and eslint-config-next 16.3.7 with pnpm 12.8.1.

Reasoning: Next.js/React provide the server-rendered application foundation; Material UI/Emotion implement the selected design system and SSR style cache; TypeScript and the Next ESLint configuration provide static and framework checks. TypeScript 7 and ESLint 10 were not retained because the current typescript-eslint/react lint plugins reject those APIs.

Tradeoffs: exact pins improve reproducibility but require deliberate upgrades. ESLint 9 is a compatibility pin until the Next.js plugin chain supports ESLint 10.

Status: Accepted

---

## 2026-09-29: Use Geoapify for initial address geocoding

Decision: Use Geoapify’s server-side forward-geocoding API for the early public/test product, behind a replaceable adapter and with its API key kept server-side.

Reasoning: Its current free plan permits limited commercial use, provides 3,000 credits per day, and requires no card to begin. It enables an address-submit search without using the public Nominatim service, which is unsuitable for this product’s launch infrastructure.

Tradeoffs: Geoapify attribution is required and the free quota/rate limits need monitoring. We must not persist or log home addresses, must reassess DPA/privacy and Swedish quality before launch, and should retain a path to Lantmäteriet or another provider.

Status: Accepted
