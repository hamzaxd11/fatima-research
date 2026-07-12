from __future__ import annotations

import json
import re
from urllib.parse import unquote
import zipfile
from pathlib import Path
from xml.etree import ElementTree


REPO = Path(__file__).resolve().parents[2]
WORKSPACE = REPO / "comparative_study"


def check(name: str, passed: bool, detail: str) -> dict:
    return {"check": name, "passed": passed, "detail": detail}


def validate_metadata() -> list[dict]:
    path = WORKSPACE / "metadata" / "included_studies.json"
    studies = json.loads(path.read_text(encoding="utf-8"))
    full_text = [item for item in studies if item.get("evidence_status") == "full_text_checked"]
    verified = [item for item in studies if item.get("handle_valid") and item.get("title_match")]
    evidence_paths = []
    for item in studies:
        evidence = item.get("evidence") or {}
        relative = evidence.get("text_path")
        normalized = relative.replace("\\", "/") if relative else None
        evidence_paths.append(bool(normalized and (WORKSPACE / normalized).exists()))
    return [
        check("included study count", len(studies) == 12, f"{len(studies)} studies"),
        check("DOI and title verification", len(verified) == 12, f"{len(verified)}/12 verified"),
        check("full-text evidence count", len(full_text) == 11, f"{len(full_text)}/12 full text; one abstract-level record expected"),
        check("local evidence paths", all(evidence_paths), f"{sum(evidence_paths)}/12 source texts exist"),
    ]


def validate_claim_sources() -> list[dict]:
    expected = {
        "wasan2022.txt": ["25%", "OR = 3.9", "61.9%"],
        "aziz2024.txt": ["69.8", "38.4", "71.1", "11.9"],
        "shah2023.txt": ["65.3%", "51.7%", "47.7%", "30.7%"],
        "michael2020.txt": ["67%", "77.7%", "68.7%"],
        "afzaal2024.txt": ["0.649", "p < 0.001"],
        "dasgupta2008.txt": ["48.75%", "11.25%"],
        "kansal2016.txt": ["literate (62%)", "illiterate (13%)"],
        "yadav2018.txt": ["67.4%", "26.4%", "56 (40%)"],
        "bhusal2020.txt": ["AOR = 0.52", "AOR = 2.61"],
        "haque2014.txt": ["51% vs 82.4%", "28.8% vs 88.9%"],
        "alam2017.txt": ["APD=−5.4", "APD=9.1"],
        "upashe2015.txt": ["AOR = 1.51", "AOR = 2.03"],
    }
    results = []
    for filename, markers in expected.items():
        text = (WORKSPACE / "paper_text" / filename).read_text(encoding="utf-8")
        missing = [marker for marker in markers if marker not in text]
        results.append(check(f"claim source: {filename}", not missing, "all markers found" if not missing else f"missing: {missing}"))
    return results


def validate_manuscript() -> list[dict]:
    markdown = (REPO / "RESEARCH_PAPER_RAW.md").read_text(encoding="utf-8")
    reference_numbers = [int(value) for value in re.findall(r"^(\d+)\. ", markdown, flags=re.MULTILINE)]
    reference_numbers = [number for number in reference_numbers if number <= 50][-21:]
    dois = re.findall(r"https://doi\.org/([^\s)]+)", markdown)
    expected_phrases = [
        "### 6.1 Comparative review methods",
        "### 6.2 Comparison with published studies",
        "Holm-adjusted p = 0.0758",
        "H = 8.0427",
        "rho = 0.3650, p < 0.001",
        "Contradicts the expected direction",
    ]
    protected = [
        REPO / "menstrual hygiene spss.sav fatima and ayesha (1).sav",
        REPO / "Synopsis - Menstrual hygiene..docx",
        REPO / "doc.md",
    ]
    return [
        check("reference numbering", reference_numbers == list(range(1, 22)), f"references: {reference_numbers}"),
        check("unique DOI count", len(set(dois)) == 18, f"{len(set(dois))} unique DOI links; 3 institutional references have no DOI"),
        check("comparative manuscript content", all(phrase in markdown for phrase in expected_phrases), "all required comparative and result phrases present"),
        check("protected root files", all(path.exists() for path in protected), ", ".join(path.name for path in protected)),
    ]


def validate_markdown_links() -> list[dict]:
    broken = []
    inspected = 0
    for markdown_path in REPO.rglob("*.md"):
        if ".git" in markdown_path.parts:
            continue
        text = markdown_path.read_text(encoding="utf-8", errors="ignore")
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            target = target.strip().split("#", 1)[0]
            if not target or re.match(r"^(?:https?://|mailto:)", target):
                continue
            inspected += 1
            resolved = (markdown_path.parent / unquote(target)).resolve()
            if not resolved.exists():
                broken.append(f"{markdown_path.relative_to(REPO)} -> {target}")
    return [check("local Markdown links", not broken, f"{inspected} inspected; broken: {broken}")]


def validate_docx() -> list[dict]:
    docx_path = REPO / "RESEARCH_PAPER.docx"
    if not docx_path.exists():
        return [check("DOCX exists", False, "RESEARCH_PAPER.docx missing")]
    with zipfile.ZipFile(docx_path) as archive:
        document_xml = archive.read("word/document.xml")
        root = ElementTree.fromstring(document_xml)
        text = " ".join(value for value in root.itertext() if value.strip())
        media = [name for name in archive.namelist() if name.startswith("word/media/")]
        tables = [element for element in root.iter() if element.tag.endswith("}tbl")]
    phrases = [
        "Comparative review methods",
        "Comparison with published studies",
        "Wasan et al., rural Sindh",
        "Upashe et al., Ethiopia",
        "10.1186/s12905-015-0245-7",
    ]
    return [
        check("DOCX exists", True, f"{docx_path.stat().st_size} bytes"),
        check("DOCX comparative content", all(phrase in text for phrase in phrases), "required comparison phrases present"),
        check("DOCX figures", len(media) == 4, f"{len(media)} embedded media files"),
        check("DOCX tables", len(tables) >= 8, f"{len(tables)} tables"),
    ]


def main() -> None:
    results = validate_metadata() + validate_claim_sources() + validate_manuscript() + validate_markdown_links() + validate_docx()
    output = {
        "passed": all(item["passed"] for item in results),
        "passed_count": sum(item["passed"] for item in results),
        "total_count": len(results),
        "checks": results,
    }
    audits = WORKSPACE / "audits"
    audits.mkdir(parents=True, exist_ok=True)
    (audits / "automated_validation.json").write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = [
        "# Automated Package Validation",
        "",
        f"Overall: {'PASS' if output['passed'] else 'FAIL'} ({output['passed_count']}/{output['total_count']})",
        "",
        "| Check | Status | Detail |",
        "| --- | --- | --- |",
    ]
    for item in results:
        detail = item["detail"].replace("|", "\\|")
        lines.append(f"| {item['check']} | {'PASS' if item['passed'] else 'FAIL'} | {detail} |")
    (audits / "automated_validation.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{'PASS' if output['passed'] else 'FAIL'}: {output['passed_count']}/{output['total_count']} checks")
    for item in results:
        if not item["passed"]:
            print(f"FAIL: {item['check']}: {item['detail']}")
    raise SystemExit(0 if output["passed"] else 1)


if __name__ == "__main__":
    main()
