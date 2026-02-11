# Data Analysis Summary

## 1. Study Overview
*   **Total Participants**: 160 (Original Dataset)
*   **Valid Participants**: 120 (40 empty rows excluded)
*   **Objective**: To assess Menstrual Hygiene Awareness and Practice among adolescent girls and determine the impact of Maternal Education.

## 2. Key Statistics

### Demographics
*   **Average Age**: 14.5 years (Range: 12-18)
*   **Average Monthly Income**: 48,833
*   **Family Size**: 6.7 members (avg)
*   **Maternal Education**:
    *   Illiterate/Primary (Level 1): 71.7%
    *   Middle (Level 2): 14.2%
    *   Secondary (Level 3): 6.7%
    *   Intermediate (Level 4): 6.7%
    *   Higher (Level 5): 0.8%

### Score Summary (Corrected)
*   **Knowledge Score** (0-9):
    *   **Mean**: 5.82
    *   **Median**: 6.00
    *   **Max**: 8
*   **Practice Score** (0-7):
    *   **Mean**: 5.68
    *   **Median**: 6.00
    *   **Max**: 7

## 3. Hypothesis Testing Results

### Impact of Maternal Education on **Practice**
*   **Result**: **Statistically Significant**
*   **Test Used**: ANOVA
*   **P-Value**: **0.0417** (p < 0.05)
*   **Robustness Check**: Confirmed by Kruskal-Wallis test (p = 0.0379).
*   **Conclusion**: There is a significant difference in hygiene *practices* based on the mother's education level.

### Impact of Maternal Education on **Knowledge**
*   **Result**: **Not Significant**
*   **Test Used**: ANOVA
*   **P-Value**: 0.2610 (p > 0.05)
*   **Conclusion**: Maternal education level did not significantly predict the *knowledge* scores in this sample.

## 4. Correlations
*   **Age vs. Knowledge**: Moderate positive correlation (r = 0.307, p < 0.01). Older girls tend to have higher knowledge scores.
*   **Knowledge vs. Practice**: Weak-Moderate correlation (r = 0.335). Knowing more is somewhat associated with better practice, but they are not identical.
*   **Income vs. Practice**: No significant correlation.

## 5. Methodology Notes
*   **Missing Values**: 40 empty rows were filtered out. Missing questionnaire answers for valid students were scored as 0.
*   **Statistical Tests**: ANOVA was used as the primary test. Normality checks were performed, and non-parametric tests (Kruskal-Wallis) were used to confirm results where assumptions were violated.
