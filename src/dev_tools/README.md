# Developer Helper Scripts

These scripts are optional utilities for developers and reviewers. They are not part of the main pipeline (`analyze.py`).

## How to Run
Run from the repository root (recommended):

```bash
python src/dev_tools/<script_name>.py
```

## Scripts
- `analyze_columns.py`: Prints SPSS column inventory and candidates for knowledge/practice questions.
- `check_validity.py`: Runs consistency checks, outlier detection, and basic confounder checks on the latest output.
- `convert_spss_data.py`: Converts SPSS data into multiple review-friendly formats (CSV, optional Excel).
- `repro_issue.py`: Reproduces mean-skew issue by comparing raw vs. filtered records.
- `test_data_analysis.py`: Inspects SPSS structure, missingness, and scoring behavior.
- `verify_data.py`: Verifies data integrity between raw SPSS and latest scored dataset.
- `verify_stats.py`: Runs additional statistical checks (ANOVA assumptions, effect size, post-hoc, Kruskal-Wallis).

## Notes
- Excel export in `convert_spss_data.py` requires `openpyxl`. If it is not installed, the script skips Excel output.
- These scripts assume the SPSS file is located at repo root and look for the latest `output/analysis_*` folder.
