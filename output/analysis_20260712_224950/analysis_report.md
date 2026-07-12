================================================================================
MENSTRUAL HYGIENE AWARENESS ANALYSIS REPORT
================================================================================

Report Generated: 2026-07-12 22:49:53

Source Data File: menstrual hygiene spss.sav fatima and ayesha (1).sav

Raw Records Loaded: 160
Fully Empty Records Removed: 40

Total Records Analyzed: 120

================================================================================

## 1. DEMOGRAPHIC SUMMARY

This section provides an overview of the study population characteristics.

### 1.1 Age Distribution

  Age 14.0: 29.0 (24.2%)
  Age 15.0: 28.0 (23.3%)
  Age 13.0: 27.0 (22.5%)
  Age 16.0: 20.0 (16.7%)
  Age 12.0: 7.0 (5.8%)
  Age 17.0: 7.0 (5.8%)
  Age 18.0: 2.0 (1.7%)

### 1.2 Maternal Education Distribution

  1 (Illiterate): 86 (71.7%)
  2 (Primary): 17 (14.2%)
  4 (Secondary): 8 (6.7%)
  3 (Middle): 8 (6.7%)
  5 (Intermediate and above): 1 (0.8%)

### 1.3 Continuous Variables Summary

**Age**
  Count: 120
  Mean: 14.47
  Median: 14.00
  Std Dev: 1.40
  Range: 12.00 - 18.00

**Income**
  Count: 120
  Mean: 48833.33
  Median: 45000.00
  Std Dev: 57440.99
  Range: 10000.00 - 600000.00

**Family Size**
  Count: 120
  Mean: 6.66
  Median: 6.00
  Std Dev: 2.38
  Range: 2.00 - 15.00

**Per Capita Income**
  Count: 120
  Mean: 8648.83
  Median: 6428.57
  Std Dev: 10763.62
  Range: 1111.11 - 100000.00


## 2. DATA QUALITY SUMMARY

This section summarizes missingness and data quality checks.

  Total Rows: 120
  Total Columns: 41
  Missing Values: 550
  Invalid Values: 6
  Data Quality: 88.7%
  Core Data Quality: 99.7%

Conditional/Skip-Logic Columns (missingness expected):
  - IfYesSourceOfInformationAboutMensturation
  - AnyOtherSpecify
  - AnyOtherPleaseSpecify
  - IfUseClothDoYouRegularyWashClothPadWithSoapAndWater
  - DoYouDryTheClothINSun
  - FaceAnyProblemDuringWashingandDryingClothUsedForMensturation
  - TypeOfProblemFaceWhileWashingAndDryingCloth
  - ReasonNotUsingSanitaryPads

Family Size Consistency Check:
  Checked Rows: 120, Mismatches: 0


## 3. KNOWLEDGE SCORES ANALYSIS

Knowledge scores range from 0 to 9, based on responses to Section III questions
about menstrual hygiene awareness. The adjudicated key scores menstruation as a
physiological/natural process; archived reverse coding is reported as a sensitivity analysis.
This is an instrument-specific composite rather than a validated unidimensional scale.

### 3.1 Overall Knowledge Score Statistics

  Total Respondents: 120
  Mean Score: 6.65
  Median Score: 7.00
  Standard Deviation: 1.22
  Minimum Score: 3
  Maximum Score: 9

### 3.2 Score Distribution

  Score 3: 2 respondents (1.7%)
  Score 4: 6 respondents (5.0%)
  Score 5: 11 respondents (9.2%)
  Score 6: 26 respondents (21.7%)
  Score 7: 45 respondents (37.5%)
  Score 8: 28 respondents (23.3%)
  Score 9: 2 respondents (1.7%)

**Visualization**: See 'score_distributions.png' for histogram


## 4. PRACTICE SCORES ANALYSIS

Practice scores range from 0 to 7, based on responses to Section IV questions
about actual menstrual hygiene practices. Missing item responses are scored zero under
the archived protocol; complete-case sensitivity results should accompany the primary result.

### 4.1 Overall Practice Score Statistics

  Total Respondents: 120
  Mean Score: 5.68
  Median Score: 6.00
  Standard Deviation: 0.58
  Minimum Score: 4
  Maximum Score: 7

### 4.2 Score Distribution

  Score 4: 6 respondents (5.0%)
  Score 5: 27 respondents (22.5%)
  Score 6: 86 respondents (71.7%)
  Score 7: 1 respondents (0.8%)

**Visualization**: See 'score_distributions.png' for histogram


## 5. MATERNAL EDUCATION IMPACT ANALYSIS

This section examines the relationship between maternal education level and
adolescent girls' menstrual hygiene knowledge and practices.

### 5.1 Scores by Maternal Education Level

**1 (Illiterate)** (n=86)
  Knowledge Score: 6.53 ± 1.27
  Practice Score: 5.59 ± 0.62

**2 (Primary)** (n=17)
  Knowledge Score: 6.53 ± 1.23
  Practice Score: 5.76 ± 0.44

**3 (Middle)** (n=8)
  Knowledge Score: 7.38 ± 0.52
  Practice Score: 6.00 ± 0.00

**4 (Secondary)** (n=8)
  Knowledge Score: 7.25 ± 0.71
  Practice Score: 6.12 ± 0.35

**5 (Intermediate and above)** (n=1)
  Knowledge Score: 8.00 ± N/A
  Practice Score: 6.00 ± N/A

### 5.2 Statistical Significance Testing

**Test Used**: Kruskal-Wallis (Robust)

**Knowledge Scores:**
  Test Type: Kruskal-Wallis
  Test Statistic: 8.0427
  P-value: 0.0900
  Effect Size (epsilon_squared): 0.0676
  Assumptions: Shapiro-Wilk min p=0.0001, Levene p=N/A
  Note: Small group sizes limit parametric assumptions
  Interpretation: The difference in knowledge scores across maternal
                  education levels is not statistically significant at the unadjusted 0.05 level.

**Practice Scores:**
  Test Type: Kruskal-Wallis
  Test Statistic: 10.1562
  P-value: 0.0379
  Effect Size (epsilon_squared): 0.0853
  Assumptions: Shapiro-Wilk min p=0.0000, Levene p=N/A
  Note: Small group sizes limit parametric assumptions
  Interpretation: The difference in practice scores across maternal
                  education levels is statistically significant in the primary unadjusted analysis.
  Sensitivity note: A conservative exploratory Holm correction across knowledge and
                    practice is reported separately to assess multiplicity sensitivity.

**Visualizations**:
  - See 'scores_by_maternal_education.png' for bar chart with error bars
  - See 'score_boxplots.png' for box plots by education level


## 6. CORRELATION ANALYSIS

Pearson correlation coefficients between continuous variables (complete-case).

### 6.1 Correlation Matrix

**Key Findings:**

  Knowledge Score <-> Age: r=0.314, p=0.0005
  Knowledge Score <-> Income Per Month: r=-0.042, p=0.6501
  Knowledge Score <-> Total Family Members: r=-0.201, p=0.0279
  Knowledge Score <-> Per Capita Income: r=0.040, p=0.6637
  Knowledge Score <-> Practice Score: r=0.317, p=0.0004
  Practice Score <-> Age: r=0.267, p=0.0032
  Practice Score <-> Income Per Month: r=-0.122, p=0.1834
  Practice Score <-> Total Family Members: r=-0.165, p=0.0725
  Practice Score <-> Per Capita Income: r=-0.077, p=0.4040

**Visualization**: See 'scatter_matrix.png' for scatter plots

### 6.2 Sensitivity Analyses

  Holm-adjusted primary outcome (knowledge_score): statistic=8.0427, p=0.0900, n=120
  Holm-adjusted primary outcome (practice_score): statistic=10.1562, p=0.0758, n=120
  Complete-case practice responses (practice_score): statistic=8.6488, p=0.0705, effect size=0.0759, n=115
  Kruskal-Wallis excluding MotherEducation=5 (knowledge_score): statistic=6.3719, p=0.0949, effect size=0.0540, n=119
  Kruskal-Wallis excluding MotherEducation=5 (practice_score): statistic=9.7515, p=0.0208, effect size=0.0826, n=119
  Archived pathological-response scoring key (knowledge_score): statistic=5.8669, p=0.2093, effect size=0.0493, n=120
  Spearman ordinal trend (MotherEducation vs knowledge_score): statistic=0.2023, p=0.0267, n=120
  Spearman ordinal trend (MotherEducation vs practice_score): statistic=0.2684, p=0.0030, n=120
  Kruskal-Wallis confounder check (Age by MotherEducation): statistic=10.6913, p=0.0303, effect size=0.0898, n=120
  Spearman correlation (Age vs knowledge_score): statistic=0.3710, p=0.0000, n=120
  Spearman correlation (Age vs practice_score): statistic=0.2233, p=0.0142, n=120
  Spearman correlation (knowledge_score vs practice_score): statistic=0.3650, p=0.0000, n=120
  Spearman correlation (IncomePerMonth vs knowledge_score): statistic=0.2160, p=0.0178, n=120
  Spearman correlation (IncomePerMonth vs practice_score): statistic=0.0544, p=0.5550, n=120


## 7. GENERATED OUTPUT FILES

All analysis outputs have been saved to the output folder:
output\analysis_20260712_224950

### 7.1 Data Files

  - **scored_dataset.csv**: Local participant-level dataset; excluded from public version control
  - **maternal_education_summary.csv**: Summary statistics by maternal education level
  - **demographic_age_freq.csv**: Frequency distribution for age
  - **demographic_maternal_education_freq.csv**: Frequency distribution for maternal education
  - **demographic_paternal_education_freq.csv**: Frequency distribution for paternal education
  - **demographic_maternal_occupation_freq.csv**: Frequency distribution for maternal occupation
  - **demographic_paternal_occupation_freq.csv**: Frequency distribution for paternal occupation
  - **demographic_continuous_stats.csv**: Descriptive statistics for continuous variables
  - **correlation_matrix.csv**: Correlation coefficients between continuous variables
  - **correlation_pvalues.csv**: P-values for Pearson correlations
  - **sensitivity_analyses.csv**: Rank-based, ordinal-trend, and confounder sensitivity checks
  - **data_quality_summary.txt**: Data quality assessment summary
  - **data_quality_missing_values.csv**: Missing value details
  - **data_quality_invalid_values.csv**: Invalid value details (if any)

### 7.2 Visualization Files

  - **scores_by_maternal_education.png**: Bar chart showing mean scores by education level
  - **score_distributions.png**: Histograms of knowledge and practice score distributions
  - **score_boxplots.png**: Box plots comparing scores across education groups
  - **scatter_matrix.png**: Scatter plot matrix for continuous variables

### 7.3 Report Files

  - **analysis_report.txt**: This report in plain text format
  - **analysis_report.md**: This report in Markdown format
  - **FILE_INVENTORY.md**: Complete inventory of all output files

================================================================================

## NOTES

- All statistical tests use α = 0.05 significance level
- Missing values were handled according to predefined rules (0 for scores, null for calculations)
- Conditional/skip-logic columns are reported separately in data quality summaries
- Group sizes may be imbalanced; interpret small-n groups with caution
- All visualizations are saved at 300 DPI resolution in PNG format
- For detailed methodology, refer to the analysis documentation

================================================================================

END OF REPORT
