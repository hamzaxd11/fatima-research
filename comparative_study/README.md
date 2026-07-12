# Comparative Study Workspace

This folder contains the evidence used to compare the present Lahore study with other menstrual-hygiene studies.

## Contents

- `papers/`: downloaded open-access papers.
- `paper_text/`: searchable text extracted from each paper.
- `article_pages/`: full-text XML saved from trusted repositories.
- `metadata/`: search results, included-study records, and verification reports.
- `outputs/`: the evidence matrix and comparative analysis.
- `audits/`: independent review and integrity reports.
- `scripts/`: reproducible acquisition and verification tools.

## Reproduce the Evidence Download

From the repository root:

```bash
pip install -r comparative_study/requirements.txt
python comparative_study/scripts/acquire_and_verify.py
```

The final manuscript uses only claims documented in the evidence matrix. Different studies use different definitions and scoring systems, so their percentages and scores are not pooled as a meta-analysis.
