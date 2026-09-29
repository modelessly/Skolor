#!/usr/bin/env python3
"""Reproducible coverage audit for official Swedish school data.

Uses only the Python standard library. Source artifacts are cached locally and
identified by URL/query, retrieval timestamp, byte size, and SHA-256 digest.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import re
import ssl
import urllib.request
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET


REGISTER_URL = "https://api.skolverket.se/skolenhetsregistret/export/skolenhet/adressfil"
REGISTER_INDEX_URL = "https://api.skolverket.se/skolenhetsregistret/v2/school-units"
PXWEB_URL = (
    "https://statistikdatabasen.skolverket.se/PxWeb/api/v1/sv/"
    "Skolverkets_statistikdatabas/Underlag_for_analys_inom_det_nationella_"
    "kvalitetssystemet/Grundskola/Grundskola.px"
)
SURVEYS = {
    "grade_5": "https://www.skolinspektionen.se/globalassets/02-beslut-rapporter-stat/statistik/statistik-skolenkaten/2026/skolenkaten-elever-grundskola-ak-5-2026.xlsx",
    "grade_8": "https://www.skolinspektionen.se/globalassets/02-beslut-rapporter-stat/statistik/statistik-skolenkaten/2026/skolenkaten-elever-grundskola-ak-8-2026.xlsx",
    "guardians": "https://www.skolinspektionen.se/globalassets/02-beslut-rapporter-stat/statistik/statistik-skolenkaten/2026/skolenkaten-vardnadshavare-grundskola-ak-1-9-2026.xlsx",
    "teachers": "https://www.skolinspektionen.se/globalassets/02-beslut-rapporter-stat/statistik/statistik-skolenkaten/2026/skolenkaten-undervisande-larare-grundskola-ak-1-9-2026.xlsx",
}
METRICS = ["0", "2", "3", "10", "15", "26", "27", "28", "29", "30", "31", "32", "35", "36", "44"]
PXWEB_QUERY = {
    "query": [
        {"code": "variable", "selection": {"filter": "item", "values": METRICS}},
        {"code": "level", "selection": {"filter": "all", "values": ["*"]}},
        {"code": "time", "selection": {"filter": "all", "values": ["*"]}},
    ],
    "response": {"format": "json-stat2"},
}
DETAIL_URL = "https://api.skolverket.se/skolenhetsregistret/v2/school-units/{code}"
USER_AGENT = "Schools research audit/1.0 (public-data coverage study)"
NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_PACKAGE_REL = "http://schemas.openxmlformats.org/package/2006/relationships"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def request_bytes(url: str, payload: dict | None = None) -> bytes:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload else None
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json" if payload else "*/*"}
    if payload:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method="POST" if payload else "GET")
    context = ssl.create_default_context()
    with urllib.request.urlopen(request, context=context, timeout=90) as response:
        return response.read()


def fetch(path: Path, url: str, payload: dict | None, offline: bool) -> None:
    if path.exists():
        return
    if offline:
        raise FileNotFoundError(f"offline cache miss: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    body = request_bytes(url, payload)
    temporary = path.with_suffix(path.suffix + ".part")
    temporary.write_bytes(body)
    temporary.replace(path)


def column_index(reference: str) -> int:
    letters = re.match(r"[A-Z]+", reference).group(0)
    value = 0
    for character in letters:
        value = value * 26 + ord(character) - 64
    return value - 1


def xlsx_rows(path: Path, sheet_name: str | None = None):
    with zipfile.ZipFile(path) as archive:
        shared = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            for item in root.findall(f"{{{NS_MAIN}}}si"):
                shared.append("".join(node.text or "" for node in item.iter(f"{{{NS_MAIN}}}t")))

        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        targets = {
            rel.attrib["Id"]: rel.attrib["Target"]
            for rel in relationships.findall(f"{{{NS_PACKAGE_REL}}}Relationship")
        }
        sheets = workbook.find(f"{{{NS_MAIN}}}sheets")
        selected = None
        for sheet in sheets:
            if sheet_name is None or sheet.attrib["name"] == sheet_name:
                selected = targets[sheet.attrib[f"{{{NS_REL}}}id"]]
                break
        if selected is None:
            raise KeyError(f"sheet not found: {sheet_name}")
        xml_path = selected.lstrip("/")
        if not xml_path.startswith("xl/"):
            xml_path = "xl/" + xml_path
        root = ET.fromstring(archive.read(xml_path))
        sheet_data = root.find(f"{{{NS_MAIN}}}sheetData")
        for row in sheet_data.findall(f"{{{NS_MAIN}}}row"):
            values: dict[int, str] = {}
            for cell in row.findall(f"{{{NS_MAIN}}}c"):
                index = column_index(cell.attrib["r"])
                cell_type = cell.attrib.get("t")
                if cell_type == "inlineStr":
                    values[index] = "".join(node.text or "" for node in cell.iter(f"{{{NS_MAIN}}}t"))
                    continue
                value = cell.find(f"{{{NS_MAIN}}}v")
                if value is None or value.text is None:
                    values[index] = ""
                elif cell_type == "s":
                    values[index] = shared[int(value.text)]
                elif cell_type == "b":
                    values[index] = "true" if value.text == "1" else "false"
                else:
                    values[index] = value.text
            if values:
                width = max(values) + 1
                yield [values.get(index, "") for index in range(width)]


def normalize_code(value: str) -> str | None:
    value = str(value).strip()
    if re.fullmatch(r"\d{8}(?:\.0)?", value):
        return value[:8]
    return None


def parse_register(path: Path) -> dict[str, dict[str, str]]:
    rows = iter(xlsx_rows(path, "Grundskola"))
    headers = [value.strip() for value in next(rows)]
    records = {}
    for row in rows:
        padded = row + [""] * (len(headers) - len(row))
        record = dict(zip(headers, padded))
        code = normalize_code(record.get("SKOLENHETSKOD", ""))
        if code:
            records[code] = record
    return records


def parse_survey(path: Path) -> dict:
    codes: set[str] = set()
    suppression = Counter()
    group_sizes = {}
    duplicate_rows = 0
    for row in xlsx_rows(path):
        code = normalize_code(row[3] if len(row) > 3 else "")
        if not code:
            continue
        if code in codes:
            duplicate_rows += 1
        codes.add(code)
        if len(row) > 5 and re.fullmatch(r"\d+(?:\.0)?", row[5]):
            group_sizes[code] = int(float(row[5]))
        for value in row[6:]:
            if value in {"*", "***", "-"}:
                suppression[value] += 1
    return {
        "codes": codes,
        "group_sizes": group_sizes,
        "duplicate_rows": duplicate_rows,
        "suppression_markers": dict(suppression),
    }


def ordered_categories(dimension: dict, name: str) -> tuple[list[str], dict[str, str]]:
    category = dimension[name]["category"]
    index = category["index"]
    if isinstance(index, list):
        codes = index
    else:
        codes = [code for code, _ in sorted(index.items(), key=lambda pair: pair[1])]
    return codes, category.get("label", {})


def parse_pxweb(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    variables, variable_labels = ordered_categories(data["dimension"], "variable")
    levels, level_labels = ordered_categories(data["dimension"], "level")
    times, time_labels = ordered_categories(data["dimension"], "time")
    values = data["value"]
    n_levels, n_times = len(levels), len(times)
    school_levels = {}
    for level_index, level in enumerate(levels):
        match = re.search(r"-(\d{8})$", level)
        if match:
            school_levels[match.group(1)] = level_index

    observations = defaultdict(lambda: defaultdict(dict))
    for variable_index, variable in enumerate(variables):
        for code, level_index in school_levels.items():
            for time_index, period in enumerate(times):
                flat_index = (variable_index * n_levels + level_index) * n_times + time_index
                value = values[flat_index]
                if value is not None:
                    observations[variable][code][period] = value
    return {
        "updated": data.get("updated"),
        "period_labels": time_labels,
        "metric_labels": variable_labels,
        "school_level_count": len(school_levels),
        "observations": observations,
    }


def systematic_sample(items: list[str], count: int) -> list[str]:
    if count <= 0 or not items:
        return []
    count = min(count, len(items))
    return [items[(index * len(items)) // count] for index in range(count)]


def fetch_coordinate_sample(codes: list[str], directory: Path, count: int, offline: bool) -> dict:
    sample = systematic_sample(sorted(codes), count)
    directory.mkdir(parents=True, exist_ok=True)

    def load(code: str):
        path = directory / f"{code}.json"
        fetch(path, DETAIL_URL.format(code=code), None, offline)
        return code, json.loads(path.read_text(encoding="utf-8"))

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        for result in executor.map(load, sample):
            results.append(result)
    with_coordinates = 0
    with_visit_address = 0
    for _, payload in results:
        addresses = payload.get("data", {}).get("attributes", {}).get("addresses", [])
        visit = [address for address in addresses if address.get("type") == "BESOKSADRESS"]
        with_visit_address += bool(visit)
        with_coordinates += bool(visit and visit[0].get("geoCoordinates", {}).get("latitude") and visit[0].get("geoCoordinates", {}).get("longitude"))
    return {
        "method": "systematic sample of sorted active grundskola codes",
        "requested": count,
        "sampled": len(results),
        "with_visit_address": with_visit_address,
        "with_coordinates": with_coordinates,
        "coordinate_rate_pct": round(100 * with_coordinates / len(results), 1) if results else None,
    }


def fetch_detail_set(codes: set[str], directory: Path, offline: bool) -> dict[str, dict]:
    directory.mkdir(parents=True, exist_ok=True)

    def load(code: str):
        path = directory / f"{code}.json"
        fetch(path, DETAIL_URL.format(code=code), None, offline)
        payload = json.loads(path.read_text(encoding="utf-8"))
        return code, payload.get("data", {}).get("attributes", {})

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        return dict(executor.map(load, sorted(codes)))


def latest_available(observations: dict[str, dict[str, float]]) -> dict[str, tuple[str, float]]:
    latest = {}
    for code, periods in observations.items():
        if periods:
            period = sorted(periods)[-1]
            latest[code] = (period, periods[period])
    return latest


def pct(numerator: int, denominator: int) -> float | None:
    return round(100 * numerator / denominator, 1) if denominator else None


def build_report(register: dict, register_status: dict, surveys: dict, pxweb: dict, coordinates: dict, mismatch_details: dict, artifacts: list[dict]) -> dict:
    codes = set(register)
    grades = {grade: {code for code, record in register.items() if record.get(f"ÅR{grade}") == "J"} for grade in range(1, 10)}
    metric_coverage = {}
    latest_sets = {}
    for metric, by_school in pxweb["observations"].items():
        latest = latest_available(by_school)
        available = set(latest) & codes
        latest_sets[metric] = available
        periods = Counter(period for code, (period, _) in latest.items() if code in codes)
        if metric in {"27", "28"}:
            denominator_codes = grades[9]
        elif metric in {"26"}:
            denominator_codes = grades[6]
        elif metric in {"29", "31"}:
            denominator_codes = grades[5]
        elif metric in {"30", "32"}:
            denominator_codes = grades[8]
        else:
            denominator_codes = codes
        applicable_available = available & denominator_codes
        history3 = {code for code, periods_by_code in by_school.items() if len(periods_by_code) >= 3} & denominator_codes
        metric_coverage[metric] = {
            "label": pxweb["metric_labels"][metric],
            "applicable_schools": len(denominator_codes),
            "latest_available": len(applicable_available),
            "coverage_pct": pct(len(applicable_available), len(denominator_codes)),
            "latest_period_distribution": dict(sorted(periods.items())),
            "three_or_more_periods": len(history3),
            "three_period_coverage_pct": pct(len(history3), len(denominator_codes)),
        }

    grade9_outcomes = grades[9] & latest_sets.get("27", set()) & latest_sets.get("28", set())
    grade6_outcomes = grades[6] & latest_sets.get("26", set())
    teaching = codes & latest_sets.get("10", set()) & latest_sets.get("15", set())
    pupil_environment = (
        (grades[5] & latest_sets.get("29", set()) & latest_sets.get("31", set()))
        | (grades[8] & latest_sets.get("30", set()) & latest_sets.get("32", set()))
    )
    outcomes = grade9_outcomes | grade6_outcomes
    three_component_proxy = outcomes & teaching & pupil_environment

    survey_report = {}
    for name, survey in surveys.items():
        joined = survey["codes"] & codes
        unmatched = survey["codes"] - codes
        unmatched_status = Counter(register_status.get(code, "NOT_IN_REGISTER_INDEX") for code in unmatched)
        active_types = Counter(
            school_type
            for code in unmatched
            if register_status.get(code) == "AKTIV"
            for school_type in mismatch_details.get(code, {}).get("schoolTypes", [])
        )
        survey_report[name] = {
            "school_codes": len(survey["codes"]),
            "joined_active_register": len(joined),
            "join_rate_pct": pct(len(joined), len(survey["codes"])),
            "active_register_coverage_pct": pct(len(joined), len(codes)),
            "unmatched_codes": len(unmatched),
            "unmatched_sample": sorted(unmatched)[:10],
            "unmatched_status": dict(unmatched_status),
            "unmatched_active_school_types": dict(active_types),
            "duplicate_school_rows": survey["duplicate_rows"],
            "schools_with_group_size": len(survey["group_sizes"]),
            "suppression_markers": survey["suppression_markers"],
        }

    organizer_types = Counter(record.get("HUVUDMANNATYP") or "missing" for record in register.values())
    address_count = sum(bool(record.get("BESÖKSADRESS") and record.get("BESÖKSPOSTORT")) for record in register.values())
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "scope": "Active grundskola in daily register extract; selected PxWeb measures for 2022/23–2025/26; Skolenkäten 2026",
        "artifacts": artifacts,
        "register": {
            "active_grundskola": len(codes),
            "unique_school_unit_codes": len(codes),
            "organizer_types": dict(organizer_types),
            "complete_visit_address": address_count,
            "visit_address_coverage_pct": pct(address_count, len(codes)),
            "offered_grade_counts": {str(grade): len(grade_codes) for grade, grade_codes in grades.items()},
            "coordinate_sample": coordinates,
        },
        "pxweb": {
            "source_updated": pxweb["updated"],
            "school_levels_in_table": pxweb["school_level_count"],
            "metric_coverage": metric_coverage,
        },
        "surveys_2026": survey_report,
        "eligibility_proxies": {
            "grade_9_outcomes_both_measures": len(grade9_outcomes),
            "grade_6_attainment": len(grade6_outcomes),
            "teaching_both_measures": len(teaching),
            "pupil_environment_safety_and_study_pair": len(pupil_environment),
            "outcome_teaching_environment_intersection": len(three_component_proxy),
            "intersection_pct_all_active": pct(len(three_component_proxy), len(codes)),
            "note": "Proxy only: SALSA and full score anchor/recency/confidence rules are not applied.",
        },
        "known_gaps": [
            "No supported national bulk SALSA export was verified; only the public per-school SIRIS application and methodology were found.",
            "The daily register XLSX has complete visit addresses but no coordinates; coordinate coverage is estimated from a deterministic API detail sample.",
            "This audit profiles availability, not statistical validity, response bias, licence sufficiency, or parent comprehension.",
        ],
    }


def artifact_record(name: str, path: Path, url: str, query: dict | None = None) -> dict:
    record = {"name": name, "url": url, "bytes": path.stat().st_size, "sha256": sha256(path)}
    if query:
        record["query"] = query
    return record


def report_markdown(report: dict) -> str:
    register = report["register"]
    proxy = report["eligibility_proxies"]
    lines = [
        "# National Coverage Audit",
        "",
        f"Generated: {report['generated_at']}",
        "",
        "## Scope",
        "",
        report["scope"],
        "",
        "## Measured results",
        "",
        f"- Active grundskola units: **{register['active_grundskola']:,}** with {register['visit_address_coverage_pct']}% complete visiting addresses.",
        f"- Coordinate sample: **{register['coordinate_sample']['with_coordinates']}/{register['coordinate_sample']['sampled']}** ({register['coordinate_sample']['coordinate_rate_pct']}%).",
        f"- Outcome + teaching + pupil-environment proxy intersection: **{proxy['outcome_teaching_environment_intersection']:,}** ({proxy['intersection_pct_all_active']}% of active units).",
        "- This intersection is not score eligibility; SALSA, anchors, recency, confidence, and validation gates are not applied.",
        "",
        "### Selected metric coverage",
        "",
        "| Metric | Applicable | Latest available | Coverage | 3+ periods |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for metric in METRICS:
        item = report["pxweb"]["metric_coverage"][metric]
        lines.append(
            f"| {item['label']} | {item['applicable_schools']:,} | {item['latest_available']:,} | {item['coverage_pct']}% | {item['three_or_more_periods']:,} |"
        )
    lines.extend(["", "### Skolenkäten 2026 joins", "", "| Workbook | Unit codes | Joined active | Join rate | Active coverage | Unmatched | Unmatched current status |", "| --- | ---: | ---: | ---: | ---: | ---: | --- |"])
    for name, item in report["surveys_2026"].items():
        status = ", ".join(f"{key}: {value}" for key, value in sorted(item["unmatched_status"].items()))
        lines.append(
            f"| {name} | {item['school_codes']:,} | {item['joined_active_register']:,} | {item['join_rate_pct']}% | {item['active_register_coverage_pct']}% | {item['unmatched_codes']:,} | {status} |"
        )
    lines.extend(["", "## Known gaps", ""] + [f"- {gap}" for gap in report["known_gaps"]])
    lines.extend(["", "## Source artifact hashes", "", "| Artifact | Bytes | SHA-256 |", "| --- | ---: | --- |"])
    for item in report["artifacts"]:
        lines.append(f"| {item['name']} | {item['bytes']:,} | `{item['sha256']}` |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-dir", type=Path, default=Path(".cache/research/school-data-2026"))
    parser.add_argument("--output-dir", type=Path, default=Path("docs/research"))
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--coordinate-sample", type=int, default=120)
    args = parser.parse_args()
    args.cache_dir.mkdir(parents=True, exist_ok=True)

    register_path = args.cache_dir / "school-units.xlsx"
    register_index_path = args.cache_dir / "school-unit-index.json"
    metrics_path = args.cache_dir / "grundskola-metrics.json"
    fetch(register_path, REGISTER_URL, None, args.offline)
    fetch(register_index_path, REGISTER_INDEX_URL, None, args.offline)
    fetch(metrics_path, PXWEB_URL, PXWEB_QUERY, args.offline)
    survey_paths = {}
    for name, url in SURVEYS.items():
        path = args.cache_dir / f"survey-{name.replace('_', '-')}.xlsx"
        fetch(path, url, None, args.offline)
        survey_paths[name] = path

    register = parse_register(register_path)
    register_index_payload = json.loads(register_index_path.read_text(encoding="utf-8"))
    register_status = {
        item["schoolUnitCode"]: item.get("status", "UNKNOWN")
        for item in register_index_payload.get("data", {}).get("attributes", [])
    }
    surveys = {name: parse_survey(path) for name, path in survey_paths.items()}
    pxweb = parse_pxweb(metrics_path)
    coordinates = fetch_coordinate_sample(list(register), args.cache_dir / "school-details", args.coordinate_sample, args.offline)
    unmatched_active = {
        code
        for survey in surveys.values()
        for code in survey["codes"] - set(register)
        if register_status.get(code) == "AKTIV"
    }
    mismatch_details = fetch_detail_set(unmatched_active, args.cache_dir / "school-details", args.offline)
    artifacts = [
        artifact_record("school-units", register_path, REGISTER_URL),
        artifact_record("school-unit-index", register_index_path, REGISTER_INDEX_URL),
        artifact_record("grundskola-metrics", metrics_path, PXWEB_URL, PXWEB_QUERY),
    ] + [artifact_record(f"survey-{name}", path, SURVEYS[name]) for name, path in survey_paths.items()]
    report = build_report(register, register_status, surveys, pxweb, coordinates, mismatch_details, artifacts)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "coverage-audit-2026-09-29.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "coverage-audit-2026-09-29.md").write_text(report_markdown(report), encoding="utf-8")
    print(json.dumps({"active_grundskola": len(register), "output_dir": str(args.output_dir)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
