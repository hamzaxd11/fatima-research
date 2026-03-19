# Menstrual Hygiene Awareness in Adolescent Girls: Exploring the Influence of Maternal Education on Knowledge and Practices in a Sub-Urban Area of Pakistan

**Supervisor:** Dr Naureen Omar

**Investigators:** Dr Ayesha Javed, Dr Fatima Sohail

## Abstract

Menstrual hygiene management remains a major adolescent health challenge in low-resource settings where stigma, inadequate menstrual health literacy, and limited access to safe hygiene materials can compromise health, dignity, and school participation [1-3]. Maternal education is frequently viewed as an important determinant of adolescent health behavior, but local evidence from sub-urban Pakistan is limited. This study examined menstrual hygiene knowledge and practices among adolescent girls and assessed whether these outcomes differed across maternal education categories. The manuscript is based on a finalized school-based survey dataset from a sub-urban area of Lahore, Pakistan. Of 160 raw records loaded from the SPSS source file, 40 records with missing maternal education were excluded according to the predefined analytic pipeline, leaving 120 analyzable participants. Knowledge scores ranged from 0 to 9 and practice scores ranged from 0 to 7, both generated from prespecified questionnaire scoring rules in which missing questionnaire responses were assigned a score of zero. Descriptive statistics, data quality checks, group comparisons, and correlation analyses were performed. Because score distributions were bounded and discrete, and because maternal education groups were imbalanced, Kruskal-Wallis tests were used for the primary group comparisons. Mean age was 14.47 years (range 12-18 years). The mean knowledge score was 5.82/9 (SD 1.08), and the mean practice score was 5.68/7 (SD 0.58). Maternal education was significantly associated with practice scores (Kruskal-Wallis H = 10.1562, p = 0.0379, epsilon-squared = 0.0535), but not with knowledge scores (H = 5.8669, p = 0.2093, epsilon-squared = 0.0162). Age correlated positively with knowledge (r = 0.307, p = 0.0007), and knowledge correlated positively with practice (r = 0.335, p = 0.0002). Overall data quality was 88.82%, while core data quality excluding conditional or skip-logic variables was 99.85%. In this sample, maternal education was more strongly related to menstrual hygiene practice than to menstrual hygiene knowledge. The findings support behavior-focused menstrual hygiene interventions, but they should be interpreted as associative rather than causal because the analysis is cross-sectional and unadjusted.

**Keywords:** menstrual hygiene; adolescent girls; maternal education; Pakistan; school health; cross-sectional study

## 1. Introduction

Adolescence is a critical developmental period in which health-related attitudes and behaviors become established and often persist into adulthood. Menstrual health is a central component of adolescent well-being, particularly for girls who must navigate menarche, cycle management, personal hygiene, and social stigma within environments that may not provide adequate information or material support. International guidance from the World Health Organization and UNESCO frames menstrual health as a health, education, rights, and gender-equity issue that depends not only on hygiene materials but also on knowledge, supportive social norms, and safe sanitation environments [1-3].

In low- and middle-income settings, menstrual hygiene management is often constrained by silence around menstruation, cultural taboos, limited privacy, and restricted access to appropriate absorbents and disposal facilities. Adolescent girls may begin menstruation without prior preparation and may rely on informal or incomplete sources of information. These barriers can impair hygienic practice, contribute to discomfort and embarrassment, and interfere with schooling and social participation. Evidence from Ghana, Ethiopia, Nepal, India, and related settings suggests that menstrual knowledge and practice are shaped by parental education, access to information, and broader socioeconomic conditions [4-10].

Within Pakistan, the interaction between family environment, maternal education, and menstrual hygiene behavior remains highly relevant, especially in sub-urban communities where educational attainment, household resources, and social norms are heterogeneous. Maternal education may influence daughters' menstrual hygiene through communication, monitoring, modeling of hygienic routines, and facilitation of access to menstrual products. At the same time, greater maternal education may not necessarily translate into large measurable differences in formal menstrual knowledge if girls also receive information from peers, media, or school environments. The present study therefore examined menstrual hygiene knowledge and menstrual hygiene practices among adolescent girls in a sub-urban area of Lahore, Pakistan, with specific attention to differences across maternal education categories.

## 2. Rationale and Objectives

This analysis addresses a practical public health question: whether maternal education is linked more strongly to what adolescent girls know about menstruation or to what they actually do during menstruation. Distinguishing between knowledge and practice is important because interventions that improve awareness alone may not be sufficient if behavior is constrained by household context, product access, or sanitation conditions. The study therefore aimed to assess menstrual hygiene knowledge and practice scores among adolescent girls and to determine whether these scores differed by maternal education level. Secondary objectives were to describe the demographic profile of the sample, summarize household economic indicators, and examine correlations among age, income, family size, and menstrual hygiene scores.

## 3. Methods

### 3.1 Study design, setting, and source protocol

This manuscript reports a structured secondary analysis of the finalized survey dataset contained in the project workspace. According to the source protocol in `doc.md`, the study was planned as a school-based questionnaire study over nine months from March to December 2024 at Reach School on Sau Asal Road, Lahore. The protocol described a structured questionnaire, school-based participant recruitment, interviewer-led administration by the primary investigators, and an expected interview duration of approximately 15 to 20 minutes per participant.

### 3.2 Participant selection and analytic sample

The source protocol stated that eligible adolescent girls with parental consent would be included and that students without parental consent or unwilling to participate would be excluded. The protocol also described simple random sampling by lottery from a prepared list of eligible female students. The finalized analytic workflow loaded 160 raw records from the SPSS source file. In keeping with the predefined pipeline rule, 40 records with missing maternal education were excluded because they were treated as empty or non-analyzable rows, leaving 120 valid records for analysis.

### 3.3 Study variables

The two principal outcomes were menstrual hygiene knowledge score and menstrual hygiene practice score. Knowledge score was treated as a bounded discrete score ranging from 0 to 9, and practice score was treated as a bounded discrete score ranging from 0 to 7. The primary explanatory variable was maternal education, coded from the SPSS metadata as 1 = Illiterate, 2 = Primary, 3 = Middle, 4 = Secondary, and 5 = Intermediate and above. Additional descriptive and exploratory variables included age, paternal education, maternal occupation, paternal occupation, monthly household income, family size, and per-capita income.

### 3.4 Scoring rules and derived variables

Knowledge score was calculated from the Section III questionnaire items using the predefined scoring rules implemented in the analysis pipeline. Practice score was calculated from the Section IV questionnaire items using a parallel prespecified scoring scheme. Under the implemented analysis rules, missing questionnaire responses were assigned a score of zero. Per-capita income was calculated as monthly household income divided by total family members. When either income or family size was missing, or family size was zero, per-capita income was set to null rather than imputed.

### 3.5 Data quality procedures

The pipeline generated a dedicated data quality report that quantified missingness, invalid values, and the proportion of affected rows and columns. Because several questionnaire items were conditional follow-up questions, the workflow explicitly distinguished overall data quality from core data quality. This prevented expected skip-pattern missingness from being misclassified as evidence of poor data capture. In addition, a family-size consistency check compared the reported total family size with the sum of male and female family members.

### 3.6 Statistical analysis

All analyses used a two-sided significance threshold of 0.05. Descriptive statistics were reported as counts and percentages for categorical variables and as mean, median, standard deviation, minimum, maximum, and quartiles for continuous variables. The main inferential question was whether knowledge and practice scores differed across maternal education categories. Before choosing a group comparison test, the pipeline assessed normality within groups using Shapiro-Wilk tests when the group size permitted, assessed variance homogeneity using Levene's test when feasible, and screened for small group sizes that would undermine parametric assumptions. Because the score variables were bounded and discrete and the education groups were markedly imbalanced, Kruskal-Wallis tests were used for the primary comparisons. Epsilon-squared was reported as the effect size for these non-parametric tests.

Pearson complete-case correlations were used to assess linear relationships among age, income, family size, per-capita income, knowledge score, practice score, and total score. Because income was strongly right-skewed and outlier-prone, rank-based Spearman correlations were also calculated as sensitivity checks for the most important relationships. A second sensitivity analysis repeated the Kruskal-Wallis tests after excluding the highest maternal education category, which contained only one participant.

### 3.7 Ethical considerations

The source protocol specified parental consent procedures, confidentiality protections, anonymity of participant information, school permission, and institutional review processes. However, the analysis bundle available for manuscript preparation did not include a reportable ethics approval identifier. Accordingly, this manuscript reports the ethical framework documented in the source protocol without fabricating an approval number that was not available in the archived materials.

## 4. Results

### 4.1 Participant flow

The finalized SPSS file yielded 160 raw records. After applying the prespecified exclusion rule for records missing maternal education, 120 records remained in the analytic sample. Table 1 summarizes the participant flow used in the statistical analysis.

| Stage | n |
| --- | ---: |
| Raw records loaded | 160 |
| Excluded (missing maternal education) | 40 |
| Final records analyzed | 120 |

### 4.2 Demographic and household characteristics

The average age of the participants was 14.47 years (SD 1.40), and ages ranged from 12 to 18 years. Household income showed wide dispersion, with a mean monthly income of 48,833.33 and a maximum reported value of 600,000, indicating substantial right-skewness. Average family size was 6.66 members, and the mean per-capita income was 8,648.83. Maternal education was concentrated in the lower categories, with 71.7% of participants in the illiterate category and 14.2% in the primary category. Only one participant belonged to the highest category, Intermediate and above. Table 2 provides the full demographic summary.

| Variable | Category/Statistic | Value |
| --- | --- | --- |
| Age (years) | Mean +/- SD | 14.47 +/- 1.40 |
| Age (years) | Median (IQR) | 14.0 (13.0-15.0) |
| Age (years) | Range | 12-18 |
| Monthly income | Mean +/- SD | 48,833.33 +/- 57,440.99 |
| Monthly income | Median (IQR) | 45,000 (30,000-50,000) |
| Family size | Mean +/- SD | 6.66 +/- 2.38 |
| Family size | Median (IQR) | 6 (5-8) |
| Per-capita income | Mean +/- SD | 8,648.83 +/- 10,763.62 |
| Per-capita income | Median (IQR) | 6,428.57 (4,285.71-10,000) |
| Maternal education | Illiterate | 86 (71.7%) |
| Maternal education | Primary | 17 (14.2%) |
| Maternal education | Middle | 8 (6.7%) |
| Maternal education | Secondary | 8 (6.7%) |
| Maternal education | Intermediate and above | 1 (0.8%) |
| Maternal occupation | Non-working | 103 (85.8%) |
| Maternal occupation | Working | 14 (11.7%) |
| Maternal occupation | Other/unlabeled code | 3 (2.5%) |
| Paternal education | Primary | 35 (29.2%) |
| Paternal education | Middle | 28 (23.3%) |
| Paternal education | Secondary | 24 (20.0%) |
| Paternal education | Illiterate | 24 (20.0%) |
| Paternal education | Intermediate and above | 9 (7.5%) |

### 4.3 Knowledge and practice score distributions

Knowledge scores ranged from 3 to 8, with a mean of 5.82 and a median of 6.00. Practice scores ranged from 4 to 7, with a mean of 5.68 and a median of 6.00. The score distributions indicated that practice scores were more tightly clustered than knowledge scores. The most common knowledge score was 6 (40.0%), whereas the most common practice score was also 6 but with much greater concentration (71.7%). Table 3 summarizes the overall score distributions.

| Score domain | Summary |
| --- | --- |
| Knowledge score (0-9) | Mean 5.82, Median 6.00, SD 1.08, Min 3, Max 8 |
| Practice score (0-7) | Mean 5.68, Median 6.00, SD 0.58, Min 4, Max 7 |

Figure 1 displays the overall score distributions graphically.

### 4.4 Scores by maternal education

Groupwise descriptive statistics showed modest increases in mean scores with increasing maternal education, although the extreme imbalance of the groups, especially the single participant in the highest education category, limited direct interpretation of the upper end of the distribution. The mean knowledge score ranged from 5.71 in the primary category to 7.00 in the Intermediate and above category, while the mean practice score ranged from 5.59 in the illiterate category to 6.12 in the secondary category. Table 4 presents the score summary by maternal education.

| Maternal education level | n | Knowledge mean +/- SD | Knowledge median (IQR) | Practice mean +/- SD | Practice median (IQR) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Illiterate | 86 | 5.73 +/- 1.16 | 6.0 (5.0-7.0) | 5.59 +/- 0.62 | 6.0 (5.0-6.0) |
| Primary | 17 | 5.71 +/- 0.92 | 6.0 (6.0-6.0) | 5.76 +/- 0.44 | 6.0 (6.0-6.0) |
| Middle | 8 | 6.38 +/- 0.52 | 6.0 (6.0-7.0) | 6.00 +/- 0.00 | 6.0 (6.0-6.0) |
| Secondary | 8 | 6.25 +/- 0.71 | 6.0 (6.0-7.0) | 6.12 +/- 0.35 | 6.0 (6.0-6.0) |
| Intermediate and above | 1 | 7.00 | 7.0 (7.0-7.0) | 6.00 | 6.0 (6.0-6.0) |

Figures 2 and 3 show these groupwise patterns using bar plots with error bars and box plots, respectively.

### 4.5 Inferential analysis for maternal education

Assumption checks indicated that parametric group-comparison methods were not appropriate for the primary analysis. Accordingly, Kruskal-Wallis tests were used for both outcomes. Knowledge score did not differ significantly across maternal education levels (H = 5.8669, p = 0.2093, epsilon-squared = 0.0162), indicating a small effect and no statistically significant between-group difference in this sample. In contrast, practice score differed significantly across maternal education levels (H = 10.1562, p = 0.0379, epsilon-squared = 0.0535), indicating a statistically significant but still modest effect size. These results suggest that maternal education in this dataset is more strongly related to menstrual hygiene behavior than to formal knowledge score. Table 5 summarizes the inferential results.

| Outcome | Test | Statistic | p-value | Effect size (epsilon-squared) | Interpretation |
| --- | --- | ---: | ---: | ---: | --- |
| Knowledge score | Kruskal-Wallis | H = 5.8669 | 0.2093 | 0.0162 | Not statistically significant |
| Practice score | Kruskal-Wallis | H = 10.1562 | 0.0379 | 0.0535 | Statistically significant |

### 4.6 Correlation analysis

Pearson complete-case analysis showed that older participants tended to have higher knowledge scores (r = 0.307, p = 0.0007). Knowledge and practice scores were also positively correlated (r = 0.335, p = 0.0002), suggesting that better menstrual hygiene knowledge tended to coexist with better reported menstrual hygiene practices. Household income showed no statistically significant relationship with either knowledge or practice score in the Pearson analysis. Because total score is mathematically derived from knowledge and practice scores, correlations involving total score were not emphasized as substantive findings. Table 6 presents the key correlations used in the manuscript.

| Variable pair | r | p-value | Interpretation |
| --- | ---: | ---: | --- |
| Age vs Knowledge score | 0.307 | 0.0007 | Moderate positive association |
| Knowledge score vs Practice score | 0.335 | 0.0002 | Weak-to-moderate positive association |
| Income vs Knowledge score | -0.014 | 0.8830 | Not significant |
| Income vs Practice score | -0.122 | 0.1834 | Not significant |

Figure 4 provides a scatter-matrix view of the continuous-variable relationships.

### 4.7 Data quality and sensitivity analyses

The data quality report identified 550 missing cells and no invalid values across 4,920 total cells, corresponding to an overall data quality of 88.82%. After excluding conditional and skip-logic variables, the core data quality rose to 99.85%, indicating that most missingness occurred in expected follow-up fields rather than in the core analytic variables. The family-size consistency check identified no mismatches between reported total family size and the sum of male and female family members.

Sensitivity analyses supported the stability of the primary conclusions. When the single participant in the highest maternal education category was excluded, knowledge score remained non-significant (H = 4.3048, p = 0.2304, epsilon-squared = 0.0113), whereas practice score remained significant (H = 9.7515, p = 0.0208, epsilon-squared = 0.0587). Rank-based Spearman correlations also preserved the key direction of association for age versus knowledge (rho = 0.3585, p < 0.001) and knowledge versus practice (rho = 0.3738, p < 0.001), while income remained non-significant. Table 7 summarizes these sensitivity results.

| Sensitivity analysis | Knowledge result | Practice result | Interpretation |
| --- | --- | --- | --- |
| Excluding maternal education level 5 (n = 1) | H = 4.3048, p = 0.2304, epsilon-squared = 0.0113 | H = 9.7515, p = 0.0208, epsilon-squared = 0.0587 | Practice association remains significant; knowledge remains non-significant |
| Spearman rank correlation (age-knowledge) | rho = 0.3585, p < 0.001 | - | Positive association remains |
| Spearman rank correlation (knowledge-practice) | rho = 0.3738, p < 0.001 | - | Positive association remains |
| Spearman rank correlation (income-knowledge / income-practice) | rho = 0.1574, p = 0.0860 | rho = 0.0544, p = 0.5550 | Income association remains non-significant |

## 5. Figures

### Figure 1. Distribution of knowledge and practice scores
![Figure 1. Knowledge and practice score distributions.](figures/manuscript_score_distributions.png)

### Figure 2. Mean knowledge and practice scores by maternal education level
![Figure 2. Mean knowledge and practice scores by maternal education level.](figures/manuscript_scores_by_maternal_education.png)

### Figure 3. Boxplots of knowledge and practice scores by maternal education level
![Figure 3. Boxplot comparison by maternal education level.](figures/manuscript_score_boxplots.png)

### Figure 4. Scatter matrix of continuous variables
![Figure 4. Scatter matrix for age, income, family size, per-capita income, knowledge, practice, and total score.](figures/manuscript_scatter_matrix.png)

## 6. Discussion

The principal finding of this study is that maternal education showed a statistically significant association with menstrual hygiene practice score, whereas its association with knowledge score was not statistically significant. This pattern matters because it suggests that maternal education in this setting may be more influential in shaping household and behavioral routines than in producing large measurable differences in questionnaire-based menstrual knowledge. In other words, the pathway from maternal education to better menstrual hygiene may operate through supervision, household norms, product access, or reinforcement of routine behavior rather than through markedly higher formal knowledge scores alone.

The positive correlation between age and knowledge score is also consistent with a developmental explanation. Older adolescent girls have had more time to experience menstruation, receive information from family or peers, and refine their understanding of cycle management. The positive correlation between knowledge and practice further indicates that better understanding is linked to better behavior, although the relationship is not so strong that knowledge can be assumed to translate automatically into practice. This is important in menstrual hygiene research, where structural barriers, stigma, and access limitations often moderate the effects of knowledge.

The results are broadly compatible with prior work from Ghana, Ethiopia, Nepal, and India showing that parental education, social context, and access to enabling resources are all relevant to menstrual hygiene management [4-10]. At the same time, the present findings reinforce the idea that knowledge and practice should not be treated as interchangeable. A girl may know correct hygiene principles but still face difficulty implementing them because of product cost, privacy constraints, limited water access, or social restrictions. Conversely, some hygienic practices may be maintained through routine socialization even when formal menstrual knowledge is incomplete.

The study has several strengths. The analysis was performed using a reproducible pipeline with preserved timestamped outputs, explicit data quality reporting, documented assumption checks, and effect-size reporting in addition to p-values. The workflow also included a family-size consistency check and targeted sensitivity analyses that showed the main conclusions were robust to the exclusion of the single-participant highest education stratum and to rank-based correlation methods.

The study also has important limitations. First, the design is cross-sectional, so the findings should be interpreted as associations rather than causal effects. Second, the analysis is unadjusted and bivariate; residual confounding by age, school context, access to menstrual products, or other family-level variables cannot be excluded. Third, maternal education groups are severely imbalanced, especially in the highest category, limiting precision and making fine-grained comparisons unstable. Fourth, the implemented rule of assigning zero to missing questionnaire responses may have biased scores downward if non-response did not represent lack of knowledge or poor practice. Fifth, the income distribution was highly skewed, which is why rank-based sensitivity analyses were important. Finally, the study is based on a single school setting and therefore may not generalize to all adolescents in Lahore or to rural and urban populations elsewhere in Pakistan.

Taken together, the findings support interventions that do more than provide factual menstrual health information. Programs in similar settings should likely include behavior-focused support, caregiver engagement, and practical measures that improve product access, privacy, and safe disposal. Future work would be strengthened by larger and more balanced samples, explicitly adjusted multivariable models, and prospective or mixed-methods designs that can clarify how maternal education influences menstrual hygiene behavior in real-world settings.

## 7. Conclusion

In this sub-urban Lahore sample of adolescent girls, maternal education was significantly associated with menstrual hygiene practice but not with menstrual hygiene knowledge. Older age was associated with higher knowledge, and better knowledge was associated with better reported practice. These findings suggest that maternal education may matter most for the enactment of hygienic behavior rather than for formal knowledge alone. Because the study is cross-sectional and analytically unadjusted, the results should be interpreted cautiously as associative evidence. Even so, they provide a practical basis for designing school and household interventions that address both menstrual health literacy and the behavioral conditions required for safe menstrual hygiene management.

## 8. Declarations

### Ethics statement

The source protocol specified parental consent procedures, confidentiality protections, anonymity of participant data, school permission, and institutional review processes. A reportable ethics approval identifier was not available in the archived analysis bundle used for manuscript preparation and should be inserted before journal submission if required by the target journal.

### Funding

No external funding information was provided in the analysis bundle.

### Competing interests

No competing interests were declared in the available source materials.

### Data and materials availability

The manuscript was prepared from the final refreshed analysis outputs stored in `output/analysis_20260319_173428/`. Public repository information was not included in the archived materials and should be added if required by the target journal.

### Author contributions

Supervisor and investigator roles are reported on the title page. Statistical processing and manuscript assembly were conducted using the documented local analysis workflow.

## 9. References

1. World Health Organization. *Strengthening the health sector response to adolescent health and development.* Geneva: WHO; 2010. Available from: https://apps.who.int/iris/bitstream/handle/10665/340531/WHO-FCH-CAH-10-01-eng.pdf?sequence=1&isAllowed=y (No DOI; accessed 2026-03-19).
2. World Health Organization. *WHO statement on menstrual health and rights.* 22 June 2022. Available from: https://www.who.int/news/item/22-06-2022-who-statement-on-menstrual-health-and-rights (No DOI; accessed 2026-03-19).
3. UNESCO. *Puberty and menstrual hygiene management.* Available from: https://www.unesco.org/en/health-education/puberty (No DOI; accessed 2026-03-19).
4. Kumbeni MT, Otupiri E, Ziba FA. Menstrual hygiene among adolescent girls in junior high schools in rural Northern Ghana. *Pan Afr Med J.* 2020;37:190. https://doi.org/10.11604/pamj.2020.37.190.19015
5. Sahiledengle B, Atlaw D, Kumie A, Tekalegn Y, Woldeyohannes D, Agho KE. Menstrual hygiene practice among adolescent girls in Ethiopia: a systematic review and meta-analysis. *PLoS One.* 2022;17(1):e0262295. https://doi.org/10.1371/journal.pone.0262295
6. Belayneh Z, Mekuriaw B. Knowledge and menstrual hygiene practice among adolescent schoolgirls in southern Ethiopia: a cross-sectional study. *BMC Public Health.* 2019;19(1):1595. https://doi.org/10.1186/s12889-019-7973-9
7. Bhusal CK. Practice of menstrual hygiene and associated factors among adolescent school girls in Dang District, Nepal. *Adv Prev Med.* 2020;2020:1292070. https://doi.org/10.1155/2020/1292070
8. Bhusal CK, Bhattarai S, Kafle R, Shrestha R, Chhetri P, Adhikari K. Level and associated factors of knowledge regarding menstrual hygiene among school-going adolescent girls in Dang District, Nepal. *Adv Prev Med.* 2020;2020:8872119. https://doi.org/10.1155/2020/8872119
9. Sonowal P, Talukdar K, Saikia H. Sociodemographic factors and their association with menstrual hygiene practices among adolescent girls in urban slums of Dibrugarh town, Assam. *J Family Med Prim Care.* 2021;10(12):4446-4451. https://doi.org/10.4103/jfmpc.jfmpc_703_21
10. Srivastava U, Singh KK. Exploring knowledge and perceptions of school adolescents regarding pubertal changes and reproductive health. *Indian J Youth Adolesc Health.* 2017;4(1):26-35. https://doi.org/10.24321/2349.2880.201705

## 10. Appendix: Statistical notes

The primary inferential analyses were non-parametric because the score outcomes were bounded and discrete, the education groups were highly imbalanced, and normality assumptions were not adequately satisfied across groups. The effect sizes were small, with epsilon-squared values of 0.0162 for knowledge score and 0.0535 for practice score, indicating that the statistically significant practice finding should still be interpreted as modest in practical magnitude. Post-hoc pairwise comparisons were not emphasized because the sparsity of the upper education strata, particularly the single participant in the highest category, would have made such comparisons unstable and potentially misleading.
