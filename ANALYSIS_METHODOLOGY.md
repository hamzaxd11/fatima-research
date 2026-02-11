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
*   This is the "non-parametric" version of ANOVA, meaning it works well even with smaller sample sizes or skewed data, ensuring our results are robust.

## 3. Demographics and Per Capita Income
*   **Per Capita Income**: Calculated as `Monthly Income / Total Family Members`.
*   **Demographic Analysis**: Simple frequency distributions and descriptive statistics (mean, median) are used for demographic variables (Age, Income, Family Size) to provide a clear picture of the study population.
