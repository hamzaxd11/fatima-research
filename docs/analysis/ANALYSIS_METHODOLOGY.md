# Statistical Analysis Methodology

This document explains the statistical methods chosen for the Menstrual Hygiene Awareness analysis, the variables involved, and the justification for these choices.

## 1. Variables and Data Types

### Dependent Variables (Outcomes)
- **Knowledge Score**
  - **Type**: Continuous / Interval (Range: 0-9)
  - **Description**: A calculated score representing menstrual hygiene awareness.
- **Practice Score**
  - **Type**: Continuous / Interval (Range: 0-7)
  - **Description**: A calculated score representing hygiene practices.

### Independent Variable (Predictor)
- **Maternal Education**
  - **Type**: Categorical / Ordinal (Multi-level)
  - **Levels**:
    1. Illiterate
    2. Primary
    3. Middle
    4. Secondary
    5. Intermediate and above

## 2. Scoring and Derived Variables

### Knowledge Score (0-9)
Calculated from Section III responses using the archived questionnaire scoring protocol, with one adjudicated correction. Missing responses are assigned a score of 0.

The archived key awarded the menstruation-process point to code 2 even though the SPSS metadata labels code 1 as physiological/natural and code 2 as pathological/disease. The corrected primary analysis awards the point to code 1 on biological grounds; the archived coding is retained as a sensitivity analysis. Four score items are nondiscriminating under the archived scoring protocol because every listed response option receives one point: the absorbent and change-frequency items in both the knowledge and practice sections. This limits score validity and must be considered when interpreting the results.

### Practice Score (0-7)
Calculated from Section IV responses using questionnaire scoring rules. Missing responses are assigned a score of 0.

### Per Capita Income
- **Formula**: `Monthly Income / Total Family Members`
- **Missing Data Handling**: If income or family size is missing/zero, per capita income is set to null and excluded from averages.

## 3. Statistical Test Selection

We use **ANOVA** when parametric assumptions are met and **Kruskal-Wallis** when they are not.

### Assumption Checks
- **Normality**: Shapiro-Wilk per group (only when group n >= 3)
- **Homogeneity of variance**: Levene's test (only when all groups n >= 2)
- **Minimum group size**: If any group has n < 3, parametric assumptions are considered insufficient for ANOVA
  - **Note**: Knowledge/practice scores are discrete and bounded, so non-normality is common even in valid data.

### Test Selection Logic
- If assumptions are satisfied, **ANOVA** is used.
- If assumptions are violated or not testable due to small group sizes, **Kruskal-Wallis** is used.

### Results for this Dataset
- **Knowledge Score**: Kruskal-Wallis H = 8.0427, p = 0.0900
- **Practice Score**: Kruskal-Wallis H = 10.1562, p = 0.0379
- **Multiplicity**: Unadjusted p-values are the principal comparisons. A conservative exploratory Holm sensitivity analysis gives practice p = 0.0758 and knowledge p = 0.0900.

## 4. Effect Sizes

- **ANOVA**: Eta squared (eta^2)
- **Kruskal-Wallis**: Epsilon squared (epsilon^2)

### Results for this Dataset
- **Knowledge Score**: epsilon^2 = H/(N-1) = 0.0676
- **Practice Score**: epsilon^2 = H/(N-1) = 0.0853

## 5. Correlation Analysis

- **Method**: Pearson correlation with p-values (complete-case)
- **Key correlations**:
  - Knowledge Score vs Age: r = 0.314, p = 0.0005
  - Knowledge Score vs Practice Score: r = 0.317, p = 0.0004
- **Note**: Correlations with Total Score are expected because Total Score is derived from Knowledge + Practice.
- **Sensitivity Note**: Income is highly skewed with outliers; Pearson correlations may be sensitive. A Spearman or log-transform sensitivity check can be used if needed.
- **Multiplicity Note**: Secondary correlations and ordinal trends are exploratory and unadjusted for multiple testing.

## 6. Data Quality and Missingness

- **Overall Missing Values**: 550 cells
- **Invalid Categorical Values**: 6 responses across 3 variables
- **Overall Issue-free Cell Rate**: 88.70%
- **Core Issue-free Cell Rate (excluding conditional/skip-logic columns)**: 99.70%
- **Metric Scope**: The denominator is the 41-column transformed dataset, including optional free-text and derived fields. The rate subtracts missing and out-of-domain cells; it is not literal non-missing completeness or a validated global quality score.

Conditional/skip-logic columns (expected missingness):
- IfYesSourceOfInformationAboutMensturation
- AnyOtherSpecify
- AnyOtherPleaseSpecify
- IfUseClothDoYouRegularyWashClothPadWithSoapAndWater
- DoYouDryTheClothINSun
- FaceAnyProblemDuringWashingandDryingClothUsedForMensturation
- TypeOfProblemFaceWhileWashingAndDryingCloth
- ReasonNotUsingSanitaryPads

## 7. Validity Checks and Limitations

### Group Size Imbalance
Maternal education groups are unbalanced:
- Level 1: n = 86
- Level 2: n = 17
- Level 3: n = 8
- Level 4: n = 8
- Level 5: n = 1

Small group sizes limit post-hoc testing and reduce confidence in the smallest group (Level 5).

### Consistency Checks
- **Family size check**: Total family members equals male + female for all 120 records.
- **Age range**: 12-18, within the adolescent range.

### Confounding Factors
- **Age**: Moderately correlated with Knowledge Score (r = 0.314, p = 0.0005).
- **Age and Practice**: Age correlated with practice (r = 0.267, p = 0.0032) and differed across maternal-education groups (H = 10.6913, p = 0.0303), so it may confound the unadjusted practice comparison.
- **Income**: Pearson correlations were not significant. The Spearman sensitivity analysis found a weak positive association with knowledge (rho = 0.2160, p = 0.0178) but not practice (rho = 0.0544, p = 0.5550).

### Modeling Scope
- Analyses are bivariate and unadjusted. Interpret differences as associations, not causal effects, unless covariates are modeled.

### Missing Data Assumption
Missing questionnaire responses are scored as 0. This may bias scores downward if non-response does not imply lack of knowledge/practice.

### Sensitivity analyses
- Excluding the single level-5 participant left the knowledge comparison non-significant and the unadjusted practice p-value below 0.05.
- Treating maternal education as ordinal produced nominal trends for knowledge (rho = 0.2023, p = 0.0267) and practice (rho = 0.2684, p = 0.0030).
- Reproducing the archived pathological-response key yielded mean knowledge 5.82 and H = 5.8669, p = 0.2093.

### Out-of-label responses
The SPSS value-label domains identified six out-of-label responses: three maternal-occupation codes of 3, two menstruation-process codes of 5, and one handwashing code of 3. The two questionnaire domains and handwashing domain were scored as incorrect because they did not match a valid answer code. The maternal-occupation values are retained as an unlabeled descriptive category.
