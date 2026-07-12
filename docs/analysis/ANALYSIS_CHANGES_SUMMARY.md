# Analysis Changes Summary (High Level)

This note summarizes what changed in the overall analysis compared to the previous version, in plain language.

## What Changed
- The scoring key was reconciled with the SPSS metadata: the physiological/natural response to the menstruation-process item is code 1, not code 2.
- The analysis was re-run and the corrected output folder was generated as `output/analysis_20260712_224950`.
- Categorical responses are now validated against SPSS value-label domains; six out-of-label values were identified and reported.
- Maternal education labels in reports, visualizations, and statistical summary CSVs were corrected to match the source SPSS coding: Illiterate, Primary, Middle, Secondary, and Intermediate and above.
- The report now separates expected missing answers (skip-logic questions) from true missing data, so data quality is clearer and more fair.
- Results are labeled with clearer maternal education names (not just numeric codes) and include sample sizes next to each group.
- The report now includes the strength of the relationships (effect sizes) and clearer notes on which tests were used.
- Correlation results now include significance values, and the output includes a new file with correlation p-values.
- Filtering of empty rows is explicitly documented in the report header (raw vs. analyzed records).

## What Stayed the Same
- The statistically significant unadjusted practice p-value remains 0.0379. A conservative exploratory Holm sensitivity correction gives an adjusted p-value of 0.0758. The knowledge omnibus p-value is 0.0900.
- Sample size remained 120 after removing 40 empty rows from the raw dataset.
- Mean knowledge increased from 5.82 to 6.65 after correction; mean practice remained 5.68.

## Why This Matters
- The updated reporting makes the analysis easier to defend during review because it explains missing data and test selection more clearly.
- The new output files make it easier to verify significance without re-running the analysis.

## Where to Find the Latest Results
- Main report: `output/analysis_20260712_224950/analysis_report.md`
- Output inventory: `output/analysis_20260712_224950/FILE_INVENTORY.md`
- Correlation p-values: `output/analysis_20260712_224950/correlation_pvalues.csv`
- Sensitivity analyses: `output/analysis_20260712_224950/sensitivity_analyses.csv`
