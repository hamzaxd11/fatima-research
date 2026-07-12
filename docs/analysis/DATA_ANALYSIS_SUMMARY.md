# Data Analysis Summary

## 1. Study Overview
- **Total Participants**: 160 (original dataset)
- **Valid Participants**: 120 (40 empty rows excluded based on missing Maternal Education)
- **Objective**: Assess menstrual hygiene awareness and practice and determine the impact of Maternal Education.

## 2. Key Statistics

### Demographics
- **Average Age**: 14.47 years (Range: 12-18)
- **Average Monthly Income**: 48,833
- **Family Size**: 6.66 members (avg)
- **Maternal Education**:
  - Illiterate (Level 1): 71.7%
  - Primary (Level 2): 14.2%
  - Middle (Level 3): 6.7%
  - Secondary (Level 4): 6.7%
  - Intermediate and above (Level 5): 0.8%

### Score Summary
- **Knowledge Score** (0-9): Mean 6.65, Median 7.00, Max 9
- **Practice Score** (0-7): Mean 5.68, Median 6.00, Max 7

## 3. Hypothesis Testing Results

### Association of Maternal Education with **Practice**
- **Result**: **Nominal unadjusted association; exploratory after multiplicity correction**
- **Test Used**: Kruskal-Wallis
- **H Statistic**: 10.1562
- **P-Value**: 0.0379
- **Holm-Adjusted P-Value**: 0.0758 for the two principal outcomes
- **Effect Size**: epsilon^2 = 0.0853
- **Complete-Case Sensitivity**: H = 8.6488, p = 0.0705 (n = 115)
- **Conclusion**: The unadjusted omnibus p-value is below 0.05, but the result is not familywise-error robust.

### Association of Maternal Education with **Knowledge**
- **Result**: **Omnibus comparison not significant**
- **Test Used**: Kruskal-Wallis
- **H Statistic**: 8.0427
- **P-Value**: 0.0900
- **Effect Size**: epsilon^2 = 0.0676
- **Conclusion**: The selected omnibus test did not detect a distributional difference. An exploratory ordinal trend was nominally significant (rho = 0.2023, p = 0.0267).

## 4. Correlations
- **Age vs. Knowledge**: r = 0.314, p = 0.0005 (moderate positive)
- **Knowledge vs. Practice**: r = 0.317, p = 0.0004 (weak to moderate)
- **Income vs. Practice/Knowledge**: Pearson correlations were not significant. Spearman analysis found a weak positive association with knowledge (rho = 0.2160, p = 0.0178) but not practice.
- **Age vs. Practice**: r = 0.267, p = 0.0032; age also differed across maternal-education groups (H = 10.6913, p = 0.0303), so confounding is plausible.

## 5. Data Quality Notes
- **Overall Missing Values**: 550 cells
- **Invalid Values**: 6 out-of-label categorical responses across 3 variables
- **Overall Post-processing Cell Completeness**: 88.70%
- **Core Cell Completeness**: 99.70% (excluding conditional/skip-logic columns)
- **Metric Scope**: Calculated on the transformed 41-column dataset; this is not a validated global data-quality score.
- **Conditional Columns**: IfYesSourceOfInformationAboutMensturation, AnyOtherSpecify, AnyOtherPleaseSpecify, IfUseClothDoYouRegularyWashClothPadWithSoapAndWater, DoYouDryTheClothINSun, FaceAnyProblemDuringWashingandDryingClothUsedForMensturation, TypeOfProblemFaceWhileWashingAndDryingCloth, ReasonNotUsingSanitaryPads

## 6. Methodology Notes
- **Missing Responses**: Questionnaire items missing for valid students are scored as 0.
- **Assumption Checks**: Shapiro-Wilk and group-size checks triggered non-parametric testing.
- **Effect Sizes**: Effect sizes are small; interpret practical significance alongside p-values.
- **Correlations**: Calculated using complete-case data (rows with all continuous variables present).
- **Income Skew**: Income is highly skewed; Pearson correlations can be sensitive to outliers.
- **Modeling Scope**: Results are unadjusted (bivariate); interpret as associations rather than causal effects.
- **Multiplicity**: The practice result does not remain below 0.05 after Holm correction for the two principal outcomes.
