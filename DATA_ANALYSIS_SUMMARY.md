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
- **Knowledge Score** (0-9): Mean 5.82, Median 6.00, Max 8
- **Practice Score** (0-7): Mean 5.68, Median 6.00, Max 7

## 3. Hypothesis Testing Results

### Impact of Maternal Education on **Practice**
- **Result**: **Statistically Significant**
- **Test Used**: Kruskal-Wallis
- **H Statistic**: 10.1562
- **P-Value**: 0.0379
- **Effect Size**: epsilon^2 = 0.0535
- **Conclusion**: Practice scores differ across maternal education levels.

### Impact of Maternal Education on **Knowledge**
- **Result**: **Not Significant**
- **Test Used**: Kruskal-Wallis
- **H Statistic**: 5.8669
- **P-Value**: 0.2093
- **Effect Size**: epsilon^2 = 0.0162
- **Conclusion**: Knowledge scores do not significantly differ by maternal education level in this sample.

## 4. Correlations
- **Age vs. Knowledge**: r = 0.307, p = 0.0007 (moderate positive)
- **Knowledge vs. Practice**: r = 0.335, p = 0.0002 (weak to moderate)
- **Income vs. Practice/Knowledge**: Not significant (p > 0.05)

## 5. Data Quality Notes
- **Overall Missing Values**: 550 cells (overall quality 88.82%)
- **Core Data Quality**: 99.85% (excluding conditional/skip-logic columns)
- **Conditional Columns**: IfYesSourceOfInformationAboutMensturation, AnyOtherSpecify, AnyOtherPleaseSpecify, IfUseClothDoYouRegularyWashClothPadWithSoapAndWater, DoYouDryTheClothINSun, FaceAnyProblemDuringWashingandDryingClothUsedForMensturation, TypeOfProblemFaceWhileWashingAndDryingCloth, ReasonNotUsingSanitaryPads

## 6. Methodology Notes
- **Missing Responses**: Questionnaire items missing for valid students are scored as 0.
- **Assumption Checks**: Shapiro-Wilk and group-size checks triggered non-parametric testing.
- **Effect Sizes**: Effect sizes are small; interpret practical significance alongside p-values.
- **Correlations**: Calculated using complete-case data (rows with all continuous variables present).
- **Income Skew**: Income is highly skewed; Pearson correlations can be sensitive to outliers.
- **Modeling Scope**: Results are unadjusted (bivariate); interpret as associations rather than causal effects.
