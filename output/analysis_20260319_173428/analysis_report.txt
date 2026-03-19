================================================================================
MENSTRUAL HYGIENE AWARENESS ANALYSIS REPORT
================================================================================

Report Generated: 2026-03-19 17:34:32

Source Data File: menstrual hygiene spss.sav fatima and ayesha (1).sav

Raw Records Loaded: 160
Records Excluded (missing MotherEducation): 40

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
  Invalid Values: 0
  Data Quality: 88.82%
  Core Data Quality: 99.85%

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
about menstrual hygiene awareness.

### 3.1 Overall Knowledge Score Statistics

  Total Respondents: 120
  Mean Score: 5.82
  Median Score: 6.00
  Standard Deviation: 1.08
  Minimum Score: 3
  Maximum Score: 8

### 3.2 Score Distribution

  Score 3: 3 respondents (2.5%)
  Score 4: 13 respondents (10.8%)
  Score 5: 23 respondents (19.2%)
  Score 6: 48 respondents (40.0%)
  Score 7: 30 respondents (25.0%)
  Score 8: 3 respondents (2.5%)

**Visualization**: See 'score_distributions.png' for histogram


## 4. PRACTICE SCORES ANALYSIS

Practice scores range from 0 to 7, based on responses to Section IV questions
about actual menstrual hygiene practices.

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
  Knowledge Score: 5.73 ± 1.16
  Practice Score: 5.59 ± 0.62

**2 (Primary)** (n=17)
  Knowledge Score: 5.71 ± 0.92
  Practice Score: 5.76 ± 0.44

**3 (Middle)** (n=8)
  Knowledge Score: 6.38 ± 0.52
  Practice Score: 6.00 ± 0.00

**4 (Secondary)** (n=8)
  Knowledge Score: 6.25 ± 0.71
  Practice Score: 6.12 ± 0.35

**5 (Intermediate and above)** (n=1)
  Knowledge Score: 7.00 ± N/A
  Practice Score: 6.00 ± N/A

### 5.2 Statistical Significance Testing

**Test Used**: Kruskal-Wallis (Robust)

**Knowledge Scores:**
  Test Type: Kruskal-Wallis
  Test Statistic: 5.8669
  P-value: 0.2093
  Effect Size (epsilon_squared): 0.0162
  Assumptions: Shapiro-Wilk min p=0.0001, Levene p=N/A
  Note: Small group sizes limit parametric assumptions
  Interpretation: The difference in knowledge scores across maternal
                  education levels is not significant (p ≥ 0.05).

**Practice Scores:**
  Test Type: Kruskal-Wallis
  Test Statistic: 10.1562
  P-value: 0.0379
  Effect Size (epsilon_squared): 0.0535
  Assumptions: Shapiro-Wilk min p=0.0000, Levene p=N/A
  Note: Small group sizes limit parametric assumptions
  Interpretation: The difference in practice scores across maternal
                  education levels is significant (p < 0.05).

**Visualizations**:
  - See 'scores_by_maternal_education.png' for bar chart with error bars
  - See 'score_boxplots.png' for box plots by education level


## 6. CORRELATION ANALYSIS

Pearson correlation coefficients between continuous variables (complete-case).

### 6.1 Correlation Matrix

**Key Findings:**

  Knowledge Score ↔ Age: r=0.307, p=0.0007
  Knowledge Score ↔ Practice Score: r=0.335, p=0.0002

**Visualization**: See 'scatter_matrix.png' for scatter plots


## 7. GENERATED OUTPUT FILES

All analysis outputs have been saved to the output folder:
output\analysis_20260319_173428

### 7.1 Data Files

  - **scored_dataset.csv**: Complete dataset with all calculated scores and derived fields
  - **maternal_education_summary.csv**: Summary statistics by maternal education level
  - **demographic_age_freq.csv**: Frequency distribution for age
  - **demographic_maternal_education_freq.csv**: Frequency distribution for maternal education
  - **demographic_paternal_education_freq.csv**: Frequency distribution for paternal education
  - **demographic_maternal_occupation_freq.csv**: Frequency distribution for maternal occupation
  - **demographic_paternal_occupation_freq.csv**: Frequency distribution for paternal occupation
  - **demographic_continuous_stats.csv**: Descriptive statistics for continuous variables
  - **correlation_matrix.csv**: Correlation coefficients between continuous variables
  - **correlation_pvalues.csv**: P-values for Pearson correlations
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
