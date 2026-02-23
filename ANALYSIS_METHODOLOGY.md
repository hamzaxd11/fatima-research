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
    1. Illiterate/Primary
    2. Middle
    3. Secondary
    4. Intermediate
    5. Higher

## 2. Scoring and Derived Variables

### Knowledge Score (0-9)
Calculated from Section III responses using questionnaire scoring rules. Missing responses are assigned a score of 0.

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
- **Knowledge Score**: Kruskal-Wallis H = 5.8669, p = 0.2093
- **Practice Score**: Kruskal-Wallis H = 10.1562, p = 0.0379

## 4. Effect Sizes

- **ANOVA**: Eta squared (eta^2)
- **Kruskal-Wallis**: Epsilon squared (epsilon^2)

### Results for this Dataset
- **Knowledge Score**: epsilon^2 = 0.0162
- **Practice Score**: epsilon^2 = 0.0535

## 5. Correlation Analysis

- **Method**: Pearson correlation with p-values (complete-case)
- **Key correlations**:
  - Knowledge Score vs Age: r = 0.307, p = 0.0007
  - Knowledge Score vs Practice Score: r = 0.335, p = 0.0002
- **Note**: Correlations with Total Score are expected because Total Score is derived from Knowledge + Practice.
- **Sensitivity Note**: Income is highly skewed with outliers; Pearson correlations may be sensitive. A Spearman or log-transform sensitivity check can be used if needed.

## 6. Data Quality and Missingness

- **Overall Missing Values**: 550 cells
- **Overall Data Quality**: 88.82%
- **Core Data Quality (excluding conditional/skip-logic columns)**: 99.85%

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
- **Age**: Moderately correlated with Knowledge Score (r = 0.307, p = 0.0007).
- **Income**: Not significantly correlated with knowledge or practice scores (p > 0.05).

### Modeling Scope
- Analyses are bivariate and unadjusted. Interpret differences as associations, not causal effects, unless covariates are modeled.

### Missing Data Assumption
Missing questionnaire responses are scored as 0. This may bias scores downward if non-response does not imply lack of knowledge/practice.
