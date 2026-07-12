"""Verify manuscript reference links and DOI metadata against live sources."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import quote

import requests


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "RESEARCH_PAPER_RAW.md"
REPORT_JSON = ROOT / "docs" / "verification" / "citation_verification.json"
REPORT_MD = ROOT / "docs" / "verification" / "CITATION_VERIFICATION.md"
HEADERS = {"User-Agent": "MenstrualHygieneCitationVerifier/1.0 (research use)"}


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def fetch_json(url: str) -> dict:
    response = requests.get(url, headers=HEADERS, timeout=45)
    response.raise_for_status()
    return response.json()


def verify_doi(number: int, reference: str, doi: str) -> dict:
    handle = fetch_json(f"https://doi.org/api/handles/{quote(doi, safe='')}")
    metadata = fetch_json(f"https://api.crossref.org/works/{quote(doi, safe='')}")["message"]
    title = " ".join(metadata.get("title") or [])
    year = ((metadata.get("published") or {}).get("date-parts") or [[None]])[0][0]
    authors = [
        " ".join(part for part in (author.get("given"), author.get("family")) if part)
        for author in metadata.get("author") or []
    ]
    return {
        "number": number,
        "doi": doi,
        "resolver_valid": handle.get("responseCode") == 1,
        "title": title,
        "title_match": normalize(title) in normalize(reference),
        "authors": authors,
        "journal": " ".join(metadata.get("container-title") or []),
        "year": year,
        "year_match": year is None or re.search(rf"\b{year}\b", reference) is not None,
        "volume": metadata.get("volume"),
        "issue": metadata.get("issue"),
        "pages": metadata.get("page") or metadata.get("article-number"),
        "crossref_url": metadata.get("URL"),
        "reference": reference,
    }


def verify_url(number: int, reference: str, url: str) -> dict:
    response = requests.get(url, headers=HEADERS, timeout=45, allow_redirects=True, stream=True)
    return {
        "number": number,
        "url": url,
        "status_code": response.status_code,
        "resolves": response.status_code < 400,
        "final_url": response.url,
        "reference": reference,
    }


def main() -> None:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    references = []
    current_number = None
    current_lines: list[str] = []
    for line in lines:
        match = re.match(r"^(\d+)\. ", line)
        if match and 1 <= int(match.group(1)) <= 21:
            if current_number is not None:
                references.append((current_number, " ".join(current_lines)))
            current_number = int(match.group(1))
            current_lines = [line]
        elif current_number is not None:
            if line.startswith("## "):
                references.append((current_number, " ".join(current_lines)))
                current_number = None
                current_lines = []
                break
            if line.strip():
                current_lines.append(line.strip())
    if current_number is not None:
        references.append((current_number, " ".join(current_lines)))
    if len(references) != 21:
        raise ValueError(f"Expected 21 references, found {len(references)}")

    results = []
    for number, reference in references:
        doi_match = re.search(r"https://doi\.org/([^\s)]+)", reference)
        url_match = re.search(r"https?://[^\s)]+", reference)
        try:
            if doi_match:
                results.append(verify_doi(number, reference, doi_match.group(1)))
            elif url_match:
                results.append(verify_url(number, reference, url_match.group(0)))
            else:
                results.append({"number": number, "reference": reference, "error": "No URL or DOI"})
        except Exception as exc:  # noqa: BLE001
            results.append({"number": number, "reference": reference, "error": str(exc)})

    payload = {"verified_on": date.today().isoformat(), "references": results}
    REPORT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# Citation Verification",
        "",
        f"Live verification date: {payload['verified_on']}",
        "",
        "| Ref | Identifier | Resolves | Title match | Year match | Crossref metadata |",
        "| ---: | --- | :---: | :---: | :---: | --- |",
    ]
    for item in results:
        if "doi" in item:
            metadata = "; ".join(
                filter(
                    None,
                    [
                        item["title"],
                        ", ".join(item["authors"]),
                        item["journal"],
                        str(item["year"] or ""),
                        str(item["volume"] or ""),
                        str(item["issue"] or ""),
                        str(item["pages"] or ""),
                    ],
                )
            )
            lines.append(
                f"| {item['number']} | `{item['doi']}` | "
                f"{'PASS' if item['resolver_valid'] else 'FAIL'} | "
                f"{'PASS' if item['title_match'] else 'FAIL'} | "
                f"{'PASS' if item['year_match'] else 'FAIL'} | {metadata} |"
            )
        elif "url" in item:
            lines.append(
                f"| {item['number']} | {item['url']} | "
                f"{'PASS' if item['resolves'] else 'FAIL'} | N/A | N/A | HTTP {item['status_code']} |"
            )
        else:
            lines.append(f"| {item['number']} | None | FAIL | N/A | N/A | {item['error']} |")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    failures = [
        item
        for item in results
        if item.get("error")
        or not item.get("resolver_valid", item.get("resolves", False))
        or item.get("title_match") is False
        or item.get("year_match") is False
    ]
    print(f"Verified references: {len(results) - len(failures)}/{len(results)}")
    for item in failures:
        print(f"Reference {item['number']}: verification mismatch")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
