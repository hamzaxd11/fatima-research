# Statistical Analysis Methodology

This document explains the statistical methods chosen for the Menstrual Hygiene Awareness analysis, the variables involved, and the justification for these choices.

## 1. Variables and Data Types

### Dependent Variables (Outcomes)
These are the variables we are measuring and testing for differences.
*   **Knowledge Score**:
    *   **Type**: Continuous / Interval (Range: 0-9)
    *   **Description**: A calculated score representing the level of awareness.
*   **Practice Score**:
    *   **Type**: Continuous / Interval (Range: 0-7)
    *   **Description**: A calculated score representing the quality of hygiene practices.

### Independent Variable (Predictor)
This is the variable we are using to group the data to see if it causes a difference.
*   **Maternal Education**:
    *   **Type**: Categorical / Ordinal (Multi-level)
    *   **Levels**:
        1.  Illiterate/Primary (Level 1)
        2.  Middle (Level 2)
        3.  Secondary (Level 3)
        4.  Intermediate (Level 4)
        5.  Higher (Level 5)

## 2. Statistical Test Selection

We chose **ANOVA (Analysis of Variance)** as the primary statistical test.

### Why ANOVA?
*   **Reason**: ANOVA is specifically designed to compare the means of a continuous dependent variable (e.g., Knowledge Score) across **three or more** independent groups (e.g., the 5 levels of Maternal Education).
*   **Goal**: To determine if there is a statistically significant difference in the average scores between different education levels.

### Why Not T-Test?
*   **Limitation**: A T-test is used to compare means between **exactly two** groups (e.g., Male vs. Female).
*   **Problem**: Since we have 5 education levels, we would have to run many separate T-tests (Level 1 vs 2, Level 1 vs 3, Level 2 vs 3, etc.).
*   **Risk**: Running multiple tests drastically increases the "Type I Error" rate (the probability of finding a "significant" result purely by chance). ANOVA handles all groups at once to avoid this issue.

### Why Not Chi-Square?
*   **Limitation**: The Chi-Square test checks for a relationship between **two categorical** variables.
*   **Problem**: While Maternal Education is categorical, our outcomes (Knowledge/Practice Scores) are **continuous**.
*   **Mismatch**: To use Chi-Square, we would have to convert our precise scores into vague categories like "High Score" vs "Low Score". This would throw away valuable detailed data and make the analysis less accurate.

### Fallback: Kruskal-Wallis Test
*   The code includes an automatic check. If the data does not meet the strict requirements for ANOVA (e.g., not normally distributed or very unequal variances), it automatically switches to the **Kruskal-Wallis** test.
### Robustness Check (Addressing Normality Concerns)
*   **Issue**: In our verification, the Shapiro-Wilk test indicated that the data for Practice Scores was **not normally distributed** (p < 0.05).
*   **Resolution**: To Ensure "p-hacking" did not occur (using an invalid test to get a good result), we ran a **Kruskal-Wallis Test** (non-parametric) as a cross-check.
*   **Result**: The Kruskal-Wallis test also showed a **statistically significant difference** (p = 0.0379).
*   **Conclusion**: The finding that Maternal Education impacts Practice Scores is **robust** and not an artifact of test selection. It holds true even when we don't assume a normal distribution.


## 4. Derived Variables

### Per Capita Income
*   **Formula**: `Monthly Income / Total Family Members`
*   **Missing Data Handling**: If Income or Family Size is missing/zero, Per Capita Income is set to `null` (excluded from averages).

## 5. Missing Data Handling
*   **Empty Rows**: The original dataset contained **160 rows**, of which **40 were completely empty** (missing Age, Education, etc.). These rows were **filtered out** prior to analysis to prevent skewing of results (Sample Size = 120).
*   **Questionnaire Responses**: For the 120 valid participants, if a specific question response was missing, it was assigned a score of **0** (conservative approach).
*   **Demographics**: Records with missing demographic data (e.g., Mother's Education) are excluded pair-wise from specific analyses (like the ANOVA test) but included in general summaries if other data is present.
