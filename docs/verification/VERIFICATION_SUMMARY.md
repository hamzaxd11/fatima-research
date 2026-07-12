# Verification Summary

This document outlines the verification steps taken to ensure the accuracy, reliability, and validity of the analysis results.

## 1. Data Integrity Checks
- **Empty Row Filtration (CRITICAL)**: Identified and removed 40 rows that were empty across every source variable.
  - **Result**: Corrected Knowledge Mean = 6.65, Practice Mean = 5.68. Sample size confirmed as N = 120.
- **Scoring-Key Check**: Reconciled the menstruation-process item with SPSS metadata. Code 1 is physiological/natural and receives the point; code 2 is pathological/disease and does not.
- **Categorical Domain Check**: Identified 6 out-of-label values across maternal occupation, the menstruation-process item, and handwashing.
- **Logic Consistency**: Verified that `Total Family Members` equals `Male Members + Female Members` for all 120 records. **(Status: PASSED)**
- **Demographic Ranges**: Verified all Age values fall within the adolescent range (12-18). **(Status: PASSED)**

## 2. Statistical Rigor
- **Test Selection**: Assumption checks (Shapiro-Wilk, group-size constraints) indicated non-normality and small groups.
- **Result**: Kruskal-Wallis used for both outcomes.
  - Knowledge: H = 8.0427, p = 0.0900, epsilon^2 = 0.0676 (not significant)
  - Practice: H = 10.1562, unadjusted p = 0.0379, epsilon^2 = 0.0853 (Holm-adjusted p = 0.0758)
  - Complete-case practice sensitivity: H = 8.6488, p = 0.0705, n = 115
- **Effect Size Note**: Observed effect sizes are small; interpret practical importance alongside statistical significance.

## 3. Confounder Analysis
- **Age**: Correlated with knowledge (r = 0.314, p = 0.0005) and practice (r = 0.267, p = 0.0032). Age also differed across maternal-education groups (H = 10.6913, p = 0.0303), so it may confound the practice result.
- **Income**: Pearson correlations were not significant. The Spearman sensitivity analysis found a weak association with knowledge (rho = 0.2160, p = 0.0178), which should be treated as exploratory.

## 4. Limitations Identified
- **Small Group Sizes**: The "Intermediate and above" group has n = 1; Levels 3 and 4 have n = 8.
  - **Implication**: Conclusions about the smallest groups should be interpreted cautiously.
- **Score Discrimination**: Four items award a point to every listed response option and therefore cannot distinguish stronger from weaker knowledge or practice.
- **Ethics Archive**: The consent text appended to `doc.md` concerns bullying rather than menstrual hygiene. The correct consent and ethics approval record must be confirmed before submission.

## 5. Final Verdict
The corrected calculations and reproducibility artifacts have been verified. Practice scores differed significantly across maternal-education groups in the primary unadjusted comparison; a conservative exploratory Holm sensitivity correction attenuated this evidence. The knowledge omnibus comparison is not significant, although an exploratory ordinal trend is statistically significant. Neither result establishes causation or an independent maternal-education effect.
