# Analysis Changes Summary (High Level)

This note summarizes what changed in the overall analysis compared to the previous version, in plain language.

## What Changed
- The analysis was re-run and a fresh output folder was generated (`output/analysis_20260223_220644`).
- The report now separates expected missing answers (skip-logic questions) from true missing data, so data quality is clearer and more fair.
- Results are labeled with clearer maternal education names (not just numeric codes) and include sample sizes next to each group.
- The report now includes the strength of the relationships (effect sizes) and clearer notes on which tests were used.
- Correlation results now include significance values, and the output includes a new file with correlation p-values.
- Filtering of empty rows is explicitly documented in the report header (raw vs. analyzed records).

## What Stayed the Same
- The key findings did not change: practice scores differ by maternal education (p = 0.0379), knowledge scores do not (p = 0.2093).
- Sample size remained 120 after removing 40 empty rows from the raw dataset.
- Mean knowledge and practice scores are unchanged.

## Why This Matters
- The updated reporting makes the analysis easier to defend during review because it explains missing data and test selection more clearly.
- The new output files make it easier to verify significance without re-running the analysis.

## Where to Find the Latest Results
- Main report: `output/analysis_20260223_220644/analysis_report.md`
- Output inventory: `output/analysis_20260223_220644/FILE_INVENTORY.md`
- Correlation p-values: `output/analysis_20260223_220644/correlation_pvalues.csv`
