#!/usr/bin/env python3
"""Analyze provisional score sensitivity and fairness without publishing a score.

The analysis uses the pinned/cacheable official extract produced by
``audit_school_data.py``. Outputs are research artifacts, not product scores.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path

try:
    from scripts.audit_school_data import latest_available, parse_pxweb, parse_register, sha256
except ModuleNotFoundError:  # Direct execution adds scripts/, not the repository root.
    from audit_school_data import latest_available, parse_pxweb, parse_register, sha256


WEIGHT_SCHEMES = {
    "baseline": {"academic": 0.40, "teaching": 0.27, "environment": 0.33},
    "academic_heavy": {"academic": 0.60, "teaching": 0.20, "environment": 0.20},
    "teaching_heavy": {"academic": 0.25, "teaching": 0.50, "environment": 0.25},
    "environment_heavy": {"academic": 0.25, "teaching": 0.25, "environment": 0.50},
    "near_equal": {"academic": 0.33, "teaching": 0.33, "environment": 0.34},
}


def percentile_midrank(values: dict[str, float], higher_is_better: bool = True) -> dict[str, float]:
    """Return 0–100 empirical mid-rank percentiles, preserving ties."""
    if not values:
        return {}
    ordered = sorted(values.items(), key=lambda item: item[1], reverse=not higher_is_better)
    result: dict[str, float] = {}
    index = 0
    total = len(ordered)
    while index < total:
        end = index + 1
        while end < total and ordered[end][1] == ordered[index][1]:
            end += 1
        rank_mid = ((index + 1) + end) / 2
        percentile = 100 * (rank_mid - 0.5) / total
        for code, _ in ordered[index:end]:
            result[code] = percentile
        index = end
    return result


def pearson(left: list[float], right: list[float]) -> float | None:
    if len(left) < 2 or len(left) != len(right):
        return None
    left_mean = statistics.fmean(left)
    right_mean = statistics.fmean(right)
    numerator = sum((a - left_mean) * (b - right_mean) for a, b in zip(left, right))
    left_ss = sum((a - left_mean) ** 2 for a in left)
    right_ss = sum((b - right_mean) ** 2 for b in right)
    denominator = math.sqrt(left_ss * right_ss)
    return numerator / denominator if denominator else None


def rank_values(values: dict[str, float], descending: bool = True) -> dict[str, float]:
    if not values:
        return {}
    ordered = sorted(values.items(), key=lambda item: item[1], reverse=descending)
    ranks: dict[str, float] = {}
    index = 0
    while index < len(ordered):
        end = index + 1
        while end < len(ordered) and ordered[end][1] == ordered[index][1]:
            end += 1
        rank = ((index + 1) + end) / 2
        for code, _ in ordered[index:end]:
            ranks[code] = rank
        index = end
    return ranks


def spearman(left: dict[str, float], right: dict[str, float]) -> float | None:
    codes = sorted(set(left) & set(right))
    left_ranks = rank_values({code: left[code] for code in codes})
    right_ranks = rank_values({code: right[code] for code in codes})
    return pearson([left_ranks[code] for code in codes], [right_ranks[code] for code in codes])


def quantile(values: list[float], proportion: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * proportion
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def rounded(value: float | None, digits: int = 3) -> float | None:
    return round(value, digits) if value is not None else None


def latest_values(pxweb: dict, metric: str) -> dict[str, float]:
    return {code: value for code, (_, value) in latest_available(pxweb["observations"][metric]).items()}


def grade_configuration(record: dict[str, str]) -> str:
    grades = [grade for grade in range(1, 10) if record.get(f"ÅR{grade}") == "J"]
    if not grades:
        return "unknown"
    if max(grades) <= 6:
        return "grades 1–6"
    if min(grades) >= 7:
        return "grades 7–9"
    if min(grades) == 1 and max(grades) == 9:
        return "grades 1–9"
    return "mixed/other"


def component_scores(register: dict[str, dict[str, str]], pxweb: dict) -> tuple[dict[str, dict[str, float]], dict[str, dict[str, float]]]:
    raw = {metric: latest_values(pxweb, metric) for metric in ["0", "2", "3", "10", "15", "26", "27", "28", "29", "30", "31", "32"]}
    percentiles = {
        metric: percentile_midrank(values, higher_is_better=metric != "15")
        for metric, values in raw.items()
        if metric not in {"0", "2", "3"}
    }
    components: dict[str, dict[str, float]] = defaultdict(dict)
    for code, record in register.items():
        if record.get("ÅR9") == "J" and code in percentiles["27"] and code in percentiles["28"]:
            components[code]["academic"] = statistics.fmean([percentiles["27"][code], percentiles["28"][code]])
        elif record.get("ÅR9") != "J" and record.get("ÅR6") == "J" and code in percentiles["26"]:
            components[code]["academic"] = percentiles["26"][code]

        if code in percentiles["10"] and code in percentiles["15"]:
            components[code]["teaching"] = statistics.fmean([percentiles["10"][code], percentiles["15"][code]])

        environment_pairs = []
        if record.get("ÅR5") == "J" and code in percentiles["29"] and code in percentiles["31"]:
            environment_pairs.append(statistics.fmean([percentiles["29"][code], percentiles["31"][code]]))
        if record.get("ÅR8") == "J" and code in percentiles["30"] and code in percentiles["32"]:
            environment_pairs.append(statistics.fmean([percentiles["30"][code], percentiles["32"][code]]))
        if environment_pairs:
            components[code]["environment"] = statistics.fmean(environment_pairs)
    return dict(components), raw


def aggregate(components: dict[str, dict[str, float]], weights: dict[str, float], minimum_components: int) -> dict[str, float]:
    scores = {}
    for code, values in components.items():
        available = set(values) & set(weights)
        if len(available) < minimum_components:
            continue
        denominator = sum(weights[name] for name in available)
        scores[code] = sum(weights[name] * values[name] for name in available) / denominator
    return scores


def top_quartile(scores: dict[str, float]) -> set[str]:
    cutoff = quantile(list(scores.values()), 0.75)
    return {code for code, score in scores.items() if score >= cutoff} if cutoff is not None else set()


def compare_scores(baseline: dict[str, float], alternative: dict[str, float]) -> dict:
    codes = sorted(set(baseline) & set(alternative))
    base_ranks = rank_values({code: baseline[code] for code in codes})
    alt_ranks = rank_values({code: alternative[code] for code in codes})
    movements = [abs(base_ranks[code] - alt_ranks[code]) for code in codes]
    base_top = top_quartile({code: baseline[code] for code in codes})
    alt_top = top_quartile({code: alternative[code] for code in codes})
    return {
        "schools": len(codes),
        "spearman": rounded(spearman(baseline, alternative)),
        "median_absolute_rank_movement": rounded(statistics.median(movements), 1) if movements else None,
        "p95_absolute_rank_movement": rounded(quantile(movements, 0.95), 1),
        "maximum_absolute_rank_movement": rounded(max(movements), 1) if movements else None,
        "top_quartile_overlap_pct": rounded(100 * len(base_top & alt_top) / len(base_top), 1) if base_top else None,
    }


def quartile_labels(values: dict[str, float]) -> tuple[dict[str, str], list[float]]:
    cuts = [quantile(list(values.values()), point) for point in (0.25, 0.50, 0.75)]
    labels = {}
    for code, value in values.items():
        if value <= cuts[0]:
            labels[code] = "Q1 (lowest)"
        elif value <= cuts[1]:
            labels[code] = "Q2"
        elif value <= cuts[2]:
            labels[code] = "Q3"
        else:
            labels[code] = "Q4 (highest)"
    return labels, [round(cut, 2) for cut in cuts]


def grouped_summary(all_codes: set[str], scores: dict[str, float], groups: dict[str, str]) -> dict[str, dict]:
    top = top_quartile(scores)
    result = {}
    for group in sorted(set(groups.values())):
        universe = {code for code in all_codes if groups.get(code) == group}
        eligible = universe & set(scores)
        score_values = [scores[code] for code in eligible]
        top_count = len(eligible & top)
        result[group] = {
            "active_schools": len(universe),
            "complete_case_schools": len(eligible),
            "complete_case_rate_pct": rounded(100 * len(eligible) / len(universe), 1) if universe else None,
            "median_score": rounded(statistics.median(score_values), 1) if score_values else None,
            "top_quartile_share_pct": rounded(100 * top_count / len(eligible), 1) if eligible else None,
        }
    return result


def analyze(register: dict[str, dict[str, str]], pxweb: dict) -> dict:
    components, raw = component_scores(register, pxweb)
    schemes = {name: aggregate(components, weights, 3) for name, weights in WEIGHT_SCHEMES.items()}
    baseline = schemes["baseline"]
    two_of_three = aggregate(components, WEIGHT_SCHEMES["baseline"], 2)
    baseline_ranks = rank_values(baseline)
    academic = {code: values["academic"] for code, values in components.items() if code in baseline and "academic" in values}
    academic_ranks = rank_values(academic)

    context = {}
    for metric, label in [("3", "parents_postsecondary_education"), ("2", "foreign_background")]:
        codes = sorted(set(baseline) & set(raw[metric]))
        context[label] = {
            "metric": metric,
            "schools": len(codes),
            "score_pearson": rounded(pearson([baseline[code] for code in codes], [raw[metric][code] for code in codes])),
            "score_spearman": rounded(spearman({code: baseline[code] for code in codes}, {code: raw[metric][code] for code in codes})),
            "academic_spearman": rounded(spearman({code: academic[code] for code in codes}, {code: raw[metric][code] for code in codes})),
        }

    parent_population = set(register) & set(raw["3"])
    parent_groups, parent_cuts = quartile_labels({code: raw["3"][code] for code in parent_population})
    shifts = defaultdict(list)
    for code in set(baseline) & parent_population:
        shifts[parent_groups[code]].append(baseline_ranks[code] - academic_ranks[code])
    parent_movement = {
        group: {
            "schools": len(values),
            "median_baseline_minus_academic_rank": rounded(statistics.median(values), 1),
        }
        for group, values in sorted(shifts.items())
    }

    sizes = {code: value for code, value in raw["0"].items() if code in register}
    size_groups, size_cuts = quartile_labels(sizes)
    organizer_groups = {code: record.get("HUVUDMANNATYP") or "missing" for code, record in register.items()}
    grade_groups = {code: grade_configuration(record) for code, record in register.items()}
    component_counts = Counter(len(values) for values in components.values())

    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "status": "research diagnostic only; not a production score or ranking",
        "population": {
            "active_grundskola": len(register),
            "complete_case_schools": len(baseline),
            "complete_case_pct": rounded(100 * len(baseline) / len(register), 1),
            "two_of_three_schools": len(two_of_three),
            "two_of_three_pct": rounded(100 * len(two_of_three) / len(register), 1),
            "component_count_distribution": dict(sorted(component_counts.items())),
        },
        "definitions": {
            "academic": "Grade-9 schools require both grade-9 outcome measures; other grade-6 schools use grade-6 all-subject attainment.",
            "teaching": "Mean percentile of qualified-teacher share and inverse pupils-per-teacher.",
            "environment": "Mean of complete safety/study-environment pairs for applicable grades 5 and/or 8.",
            "normalization": "Latest available value; empirical mid-rank percentile within each metric's observed population.",
            "missingness": "Complete-case requires all three components; the two-of-three scenario visibly renormalizes only for sensitivity testing.",
        },
        "weight_sensitivity": {
            name: {"weights": WEIGHT_SCHEMES[name], **compare_scores(baseline, scores)}
            for name, scores in schemes.items()
            if name != "baseline"
        },
        "missingness_sensitivity": {
            "complete_case": len(baseline),
            "two_of_three": len(two_of_three),
            "additional_schools": len(set(two_of_three) - set(baseline)),
            "comparison_on_complete_cases": compare_scores(baseline, two_of_three),
            "warning": "The additional schools are not directly comparable to complete cases; this scenario is not a publication recommendation.",
        },
        "context_correlations": context,
        "parent_education_quartiles": {
            "cut_points_pct": parent_cuts,
            "groups": grouped_summary(set(register), baseline, parent_groups),
            "rank_movement": parent_movement,
            "rank_movement_sign": "Negative means the baseline three-component rank is better than the academic-only rank.",
        },
        "school_size": {
            "cut_points_pupils": size_cuts,
            "groups": grouped_summary(set(register), baseline, size_groups),
        },
        "organizer_type": grouped_summary(set(register), baseline, organizer_groups),
        "grade_configuration": grouped_summary(set(register), baseline, grade_groups),
        "limitations": [
            "This is an observational sensitivity diagnostic using latest available values, not the proposed multi-year score implementation.",
            "No SALSA bulk series was available, so with/without-SALSA sensitivity remains unresolved.",
            "Correlations do not establish causality or fairness; they flag where deeper review is required.",
            "Current offered grades may differ from the grades offered in an observation year.",
            "Suppression, response selection, cohort size, and uncertainty require further model-specific review.",
        ],
    }


def markdown(report: dict) -> str:
    population = report["population"]
    lines = [
        "# Provisional Score Sensitivity and Fairness Diagnostic",
        "",
        f"Generated: {report['generated_at']}",
        "",
        "> Research diagnostic only. These calculations are not a production score or publishable ranking.",
        "",
        "## Population and missingness",
        "",
        f"- Complete-case three-component population: **{population['complete_case_schools']:,}** schools ({population['complete_case_pct']}% of {population['active_grundskola']:,} active units).",
        f"- Allowing any two components raises the population to **{population['two_of_three_schools']:,}** ({population['two_of_three_pct']}%), adding {report['missingness_sensitivity']['additional_schools']:,} schools that are not directly comparable to complete cases.",
        "- The two-of-three rule is a stress test, not a recommendation.",
        "",
        "## Weight sensitivity",
        "",
        "| Scheme | Academic / teaching / environment | Spearman vs baseline | Median rank move | P95 rank move | Top-quartile overlap |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for name, item in report["weight_sensitivity"].items():
        weights = item["weights"]
        label = f"{weights['academic']:.0%} / {weights['teaching']:.0%} / {weights['environment']:.0%}"
        lines.append(f"| {name.replace('_', ' ')} | {label} | {item['spearman']:.3f} | {item['median_absolute_rank_movement']:.1f} | {item['p95_absolute_rank_movement']:.1f} | {item['top_quartile_overlap_pct']:.1f}% |")

    lines.extend([
        "",
        "Material rank movement under plausible weights means a precise national ordinal ranking would overstate robustness even when broad ordering is correlated.",
        "",
        "## Socioeconomic diagnostic",
        "",
        "Context variables are **not** score inputs. They are used to test whether the provisional raw-evidence score remains associated with pupil context.",
        "",
        "| Context measure | Schools | Score Pearson | Score Spearman | Academic Spearman |",
        "| --- | ---: | ---: | ---: | ---: |",
    ])
    for label, item in report["context_correlations"].items():
        lines.append(f"| {label.replace('_', ' ')} | {item['schools']:,} | {item['score_pearson']:.3f} | {item['score_spearman']:.3f} | {item['academic_spearman']:.3f} |")

    lines.extend(["", "### Parent-education quartiles", "", "| Group | Complete cases | Eligibility | Median score | Top-quartile share | Academic → baseline median rank shift |", "| --- | ---: | ---: | ---: | ---: | ---: |"])
    parent_groups = report["parent_education_quartiles"]["groups"]
    movements = report["parent_education_quartiles"]["rank_movement"]
    for group, item in parent_groups.items():
        shift = movements.get(group, {}).get("median_baseline_minus_academic_rank")
        lines.append(f"| {group} | {item['complete_case_schools']:,} | {item['complete_case_rate_pct']:.1f}% | {item['median_score']:.1f} | {item['top_quartile_share_pct']:.1f}% | {shift:.1f} |")
    lines.extend(["", "Negative rank shift means the combined score ranks a school better than academic-only evidence.", "", "## School-size diagnostic", "", "| Pupil-count quartile | Active schools | Complete cases | Eligibility | Median score | Top-quartile share |", "| --- | ---: | ---: | ---: | ---: | ---: |"])
    for group, item in report["school_size"]["groups"].items():
        lines.append(f"| {group} | {item['active_schools']:,} | {item['complete_case_schools']:,} | {item['complete_case_rate_pct']:.1f}% | {item['median_score']:.1f} | {item['top_quartile_share_pct']:.1f}% |")

    for section, title in [("organizer_type", "Organizer type"), ("grade_configuration", "Grade configuration")]:
        lines.extend(["", f"## {title}", "", "| Group | Active schools | Complete cases | Eligibility | Median score | Top-quartile share |", "| --- | ---: | ---: | ---: | ---: | ---: |"])
        for group, item in report[section].items():
            median = "—" if item["median_score"] is None else f"{item['median_score']:.1f}"
            top_share = "—" if item["top_quartile_share_pct"] is None else f"{item['top_quartile_share_pct']:.1f}%"
            eligibility = "—" if item["complete_case_rate_pct"] is None else f"{item['complete_case_rate_pct']:.1f}%"
            lines.append(f"| {group} | {item['active_schools']:,} | {item['complete_case_schools']:,} | {eligibility} | {median} | {top_share} |")

    lines.extend(["", "## Interpretation", "", "The diagnostic does not clear a composite score for publication. It demonstrates sensitivity to weighting and missingness and measures socioeconomic, size, organizer, and grade-configuration differences that require statistician review. SALSA sensitivity and parent comprehension remain open gates.", "", "## Limitations", ""])
    lines.extend(f"- {item}" for item in report["limitations"])
    lines.extend(["", "## Input artifact hashes", "", "| Artifact | SHA-256 |", "| --- | --- |"])
    for item in report["inputs"]:
        lines.append(f"| {item['name']} | `{item['sha256']}` |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-dir", type=Path, default=Path(".cache/research/school-data-2026"))
    parser.add_argument("--output-dir", type=Path, default=Path("docs/research"))
    args = parser.parse_args()
    register_path = args.cache_dir / "school-units.xlsx"
    metrics_path = args.cache_dir / "grundskola-metrics.json"
    register = parse_register(register_path)
    pxweb = parse_pxweb(metrics_path)
    report = analyze(register, pxweb)
    report["inputs"] = [
        {"name": "school-units.xlsx", "sha256": sha256(register_path)},
        {"name": "grundskola-metrics.json", "sha256": sha256(metrics_path)},
    ]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "score-sensitivity-2026-09-29.json"
    markdown_path = args.output_dir / "score-sensitivity-2026-09-29.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(markdown(report), encoding="utf-8")
    print(json.dumps(report["population"], ensure_ascii=False))


if __name__ == "__main__":
    main()
