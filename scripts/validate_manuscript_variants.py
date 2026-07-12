"""Validate humanized manuscript variants against the corrected source paper."""

import hashlib
import re
from pathlib import Path

from docx import Document


ROOT = Path(__file__).resolve().parents[1]
STEMS = (
    "RESEARCH_PAPER - PLAIN SCHOLARLY",
    "RESEARCH_PAPER - NATURAL ACADEMIC",
    "RESEARCH_PAPER - CONCISE JOURNAL",
)
CRITICAL_TEXT = (
    "H = 8.0427",
    "p = 0.0900",
    "H = 10.1562",
    "p = 0.0379",
    "0.0758",
    "p = 0.0705",
    "0.0676",
    "0.0853",
)
CRITICAL_PATTERNS = (
    r"(?:40|Forty) fully blank trailing (?:records|rows)",
    r"550 (?:missing cells|cells were missing)",
    r"six (?:out-of-label|categorical responses (?:were outside|fell outside))",
    r"Ethics approval and parental consent documentation could not be verified",
    r"Practice(?: scores)? differed significantly across maternal education groups",
    r"conservative exploratory Holm",
)
FORBIDDEN_FRAMING = (
    "nominally significant",
    "did not survive Holm",
    "confirmatory result",
    "not familywise-error robust",
)
FORBIDDEN_INTERNAL_LANGUAGE = (
    "doc.md",
    "source protocol",
    "project workspace",
    "output/analysis_",
    "local analysis workflow",
    "reproducible pipeline",
    "timestamped outputs",
    "archived bundle",
    "appended consent text",
)


def extract_tables(text: str) -> list[str]:
    lines = text.splitlines()
    tables = []
    index = 0
    while index < len(lines):
        if not lines[index].startswith("|"):
            index += 1
            continue
        block = []
        while index < len(lines) and lines[index].startswith("|"):
            block.append(lines[index])
            index += 1
        tables.append("\n".join(block))
    return tables


def main() -> None:
    source = (ROOT / "RESEARCH_PAPER_RAW.md").read_text(encoding="utf-8")
    source_tables = extract_tables(source)
    source_dois = set(re.findall(r"https://doi.org/[^\s)]+", source))
    hashes = set()

    for stem in STEMS:
        markdown_path = ROOT / f"{stem}.md"
        docx_path = ROOT / f"{stem}.docx"
        text = markdown_path.read_text(encoding="utf-8")
        document = Document(docx_path)
        docx_text = "\n".join(paragraph.text for paragraph in document.paragraphs)
        flat_text = " ".join(text.split())
        flat_docx_text = " ".join(docx_text.split())

        references = re.findall(r"^(?:[1-9]|1[0-9]|2[01])\. ", text, re.MULTILINE)
        figures = re.findall(r"^!\[Figure [1-4]\.", text, re.MULTILINE)
        missing = [value for value in CRITICAL_TEXT if value not in text]
        missing_docx = [value for value in CRITICAL_TEXT if value not in docx_text]

        assert not missing, f"{stem}: missing critical Markdown text: {missing}"
        assert not missing_docx, f"{stem}: missing critical DOCX text: {missing_docx}"
        for pattern in CRITICAL_PATTERNS:
            assert re.search(pattern, flat_text, re.IGNORECASE), f"{stem}: missing Markdown pattern: {pattern}"
            assert re.search(pattern, flat_docx_text, re.IGNORECASE), f"{stem}: missing DOCX pattern: {pattern}"
        assert len(references) == 21, f"{stem}: expected 21 references"
        assert len(figures) == 4, f"{stem}: expected 4 figure links"
        assert extract_tables(text) == source_tables, f"{stem}: source tables changed"
        assert source_dois.issubset(set(re.findall(r"https://doi.org/[^\s)]+", text)))
        assert "Excluded (missing maternal education)" not in text
        for phrase in FORBIDDEN_FRAMING:
            assert phrase not in text, f"{stem}: deprecated framing in Markdown: {phrase}"
            assert phrase not in docx_text, f"{stem}: deprecated framing in DOCX: {phrase}"
        for phrase in FORBIDDEN_INTERNAL_LANGUAGE:
            assert phrase not in text, f"{stem}: internal language in Markdown: {phrase}"
            assert phrase not in docx_text, f"{stem}: internal language in DOCX: {phrase}"
        assert "| Study | Main comparable finding |" not in text
        assert "### 6.2 Comparison with published studies" not in text
        assert "TODO" not in text and "[PLACEHOLDER]" not in text
        assert len(source_tables) == 6, "source manuscript should contain six result tables"
        assert len(document.tables) == 6, f"{stem}: expected 6 DOCX tables"
        assert len(document.inline_shapes) == 4, f"{stem}: expected 4 DOCX figures"

        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        hashes.add(digest)
        print(
            f"{stem}: {len(text.split())} words, 21 references, "
            f"6 tables, 4 figures, sha256={digest[:12]}"
        )

    assert len(hashes) == len(STEMS), "Variants are not textually distinct"
    print("ALL_VARIANTS_VERIFIED")


if __name__ == "__main__":
    main()
