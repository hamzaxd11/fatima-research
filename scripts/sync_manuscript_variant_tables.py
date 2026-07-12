"""Copy verified Markdown tables into each prose-only manuscript variant."""

from pathlib import Path

from validate_manuscript_variants import ROOT, STEMS, extract_tables


def replace_tables(text: str, replacements: list[str]) -> str:
    lines = text.splitlines()
    output = []
    table_index = 0
    index = 0
    while index < len(lines):
        if not lines[index].startswith("|"):
            output.append(lines[index])
            index += 1
            continue
        while index < len(lines) and lines[index].startswith("|"):
            index += 1
        output.extend(replacements[table_index].splitlines())
        table_index += 1
    assert table_index == len(replacements)
    return "\n".join(output) + "\n"


def main() -> None:
    source = (ROOT / "RESEARCH_PAPER_RAW.md").read_text(encoding="utf-8")
    source_tables = extract_tables(source)
    for stem in STEMS:
        path = ROOT / f"{stem}.md"
        text = path.read_text(encoding="utf-8")
        assert len(extract_tables(text)) == len(source_tables)
        path.write_text(replace_tables(text, source_tables), encoding="utf-8")
        print(f"Synchronized {len(source_tables)} tables: {path.name}")


if __name__ == "__main__":
    main()
