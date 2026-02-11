# Requirements Document

## Introduction

This document specifies the requirements for a medical research data analysis system designed to analyze menstrual hygiene awareness among adolescent girls in sub-urban Lahore, Pakistan. The system will process survey data collected from adolescent girls to examine the relationship between maternal education and menstrual hygiene knowledge and practices. The analysis will support an MBBS student research project supervised by Dr. Naureen Omar, Dr. Ayesha Javed, and Dr. Fatima Sohail.

The system will read SPSS data files, calculate derived metrics, score questionnaire responses according to established guidelines, perform statistical analyses, and generate comprehensive reports with visualizations to support research findings.

## Glossary

- **System**: The data analysis software that processes survey data and generates research outputs
- **SPSS_File**: The .sav format file containing raw survey response data
- **Questionnaire**: The structured survey instrument with sections for demographics, menstrual history, knowledge, and practices
- **Knowledge_Score**: A calculated value (0-9) based on correct responses to Section III questions
- **Practice_Score**: A calculated value (0-7) based on responses to Section IV questions
- **Per_Capita_Income**: Monthly family income divided by total number of family members
- **Maternal_Education**: The education level of the respondent's mother (Illiterate, Primary, Middle, Secondary, Intermediate and above)
- **Output_Folder**: The directory where all analysis results, tables, charts, and reports are stored
- **Scored_Dataset**: The processed dataset with calculated scores and derived fields added

## Requirements

### Requirement 1: Data Import and Validation

**User Story:** As a researcher, I want to import SPSS data files into the system, so that I can analyze survey responses collected from adolescent girls.

#### Acceptance Criteria

1. WHEN a valid SPSS .sav file is provided, THE System SHALL read all variables and observations into memory
2. WHEN the SPSS file contains missing or invalid data, THE System SHALL identify and report these issues with row and column references
3. WHEN the data import is complete, THE System SHALL display a summary of imported records including total count and variable names
4. THE System SHALL preserve all original data types and values from the SPSS file
5. IF the SPSS file cannot be read, THEN THE System SHALL provide a descriptive error message indicating the file path and error type

### Requirement 2: Derived Field Calculation

**User Story:** As a researcher, I want the system to calculate per capita income automatically, so that I can analyze socioeconomic factors accurately.

#### Acceptance Criteria

1. WHEN income per month and number of family members are both present, THE System SHALL calculate per capita income as (Income Per Month / No of Family Members)
2. WHEN either income or family member count is missing or zero, THE System SHALL mark per capita income as null and log a warning
3. WHEN family member count is zero, THE System SHALL prevent division by zero and record an error for that observation
4. THE System SHALL add the calculated per capita income as a new column in the Scored_Dataset
5. THE System SHALL round per capita income to two decimal places

### Requirement 3: Knowledge Score Calculation

**User Story:** As a researcher, I want the system to calculate knowledge scores based on Section III responses, so that I can quantify menstrual hygiene awareness levels.

#### Acceptance Criteria

1. WHEN processing Section III responses, THE System SHALL assign scores according to the questionnaire scoring guidelines
2. THE System SHALL sum individual question scores to produce a total Knowledge_Score ranging from 0 to 9
3. WHEN a Section III question response is missing, THE System SHALL assign a score of 0 for that question
4. THE System SHALL validate that the final Knowledge_Score is within the valid range (0-9)
5. THE System SHALL add the Knowledge_Score as a new column in the Scored_Dataset

### Requirement 4: Practice Score Calculation

**User Story:** As a researcher, I want the system to calculate practice scores based on Section IV responses, so that I can evaluate actual menstrual hygiene behaviors.

#### Acceptance Criteria

1. WHEN processing Section IV responses, THE System SHALL assign scores according to the questionnaire scoring guidelines
2. THE System SHALL sum individual question scores to produce a total Practice_Score ranging from 0 to 7
3. WHEN a Section IV question response is missing, THE System SHALL assign a score of 0 for that question
4. THE System SHALL validate that the final Practice_Score is within the valid range (0-7)
5. THE System SHALL add the Practice_Score as a new column in the Scored_Dataset

### Requirement 5: Maternal Education Analysis

**User Story:** As a researcher, I want to analyze the relationship between maternal education and hygiene awareness scores, so that I can determine if maternal education influences adolescent girls' menstrual hygiene knowledge and practices.

#### Acceptance Criteria

1. WHEN performing maternal education analysis, THE System SHALL group data by Maternal_Education levels
2. THE System SHALL calculate mean Knowledge_Score and Practice_Score for each maternal education level
3. THE System SHALL calculate standard deviation for Knowledge_Score and Practice_Score within each education group
4. THE System SHALL perform statistical tests (ANOVA or Kruskal-Wallis) to determine if differences between education groups are statistically significant
5. THE System SHALL report p-values and confidence intervals for all statistical tests
6. THE System SHALL generate a summary table showing education level, sample size, mean scores, standard deviations, and statistical significance

### Requirement 6: Demographic Summary Statistics

**User Story:** As a researcher, I want comprehensive demographic summaries, so that I can describe the study population characteristics.

#### Acceptance Criteria

1. THE System SHALL calculate frequency distributions for all categorical demographic variables (age, maternal education, paternal education, maternal occupation, paternal occupation)
2. THE System SHALL calculate descriptive statistics (mean, median, standard deviation, min, max) for all continuous demographic variables (age, income, family size, per capita income)
3. THE System SHALL generate cross-tabulation tables for key demographic combinations
4. THE System SHALL calculate percentages and proportions for all frequency distributions
5. THE System SHALL save all demographic summary tables to the Output_Folder in CSV format

### Requirement 7: Data Visualization

**User Story:** As a researcher, I want visual charts and graphs, so that I can present findings clearly in research publications.

#### Acceptance Criteria

1. THE System SHALL generate bar charts showing mean Knowledge_Score and Practice_Score by maternal education level
2. THE System SHALL generate histograms showing the distribution of Knowledge_Score and Practice_Score across all respondents
3. THE System SHALL generate box plots comparing score distributions across maternal education groups
4. THE System SHALL generate scatter plots showing relationships between continuous variables (income, age, scores)
5. THE System SHALL save all visualizations to the Output_Folder in PNG format with minimum 300 DPI resolution
6. THE System SHALL include axis labels, titles, and legends on all charts

### Requirement 8: Output File Management

**User Story:** As a researcher, I want all analysis outputs organized in a dedicated folder, so that I can easily access and share results.

#### Acceptance Criteria

1. THE System SHALL create an Output_Folder directory if it does not exist
2. THE System SHALL save the Scored_Dataset with all calculated fields to the Output_Folder in CSV format
3. THE System SHALL save all statistical analysis tables to the Output_Folder with descriptive filenames
4. THE System SHALL save all visualization files to the Output_Folder with descriptive filenames
5. THE System SHALL generate a summary report document listing all output files with descriptions
6. WHEN output files already exist, THE System SHALL append timestamps to filenames to prevent overwriting

### Requirement 9: Analysis Report Generation

**User Story:** As a researcher, I want an automated analysis report, so that I can quickly review key findings and share results with supervisors.

#### Acceptance Criteria

1. THE System SHALL generate a text-based analysis report summarizing all key findings
2. THE System SHALL include sections for demographics, knowledge scores, practice scores, and maternal education analysis in the report
3. THE System SHALL include statistical test results with interpretations in the report
4. THE System SHALL reference all generated tables and charts in the report
5. THE System SHALL save the analysis report to the Output_Folder in both TXT and Markdown formats

### Requirement 10: Single Entry Point Execution

**User Story:** As a researcher with limited programming experience, I want to run the entire analysis with a single command, so that I can reproduce results easily.

#### Acceptance Criteria

1. THE System SHALL provide a single Python script as the entry point for all analysis operations
2. WHEN the entry point script is executed, THE System SHALL perform all data processing, scoring, analysis, and output generation steps in sequence
3. THE System SHALL display progress messages during execution indicating which step is currently running
4. WHEN any step fails, THE System SHALL display a clear error message and stop execution
5. WHEN execution completes successfully, THE System SHALL display a summary message indicating where outputs are located

### Requirement 11: Documentation and Reproducibility

**User Story:** As a researcher, I want complete documentation of the analysis process, so that I can reproduce the analysis and explain methodology in my research paper.

#### Acceptance Criteria

1. THE System SHALL include a README file documenting installation requirements, execution instructions, and output descriptions
2. THE System SHALL include inline code comments explaining all calculation logic and statistical methods
3. THE System SHALL log all analysis parameters (file paths, statistical test choices, significance levels) to a log file
4. THE System SHALL document all Python library dependencies with version numbers
5. THE System SHALL include example commands for running the analysis in the README

### Requirement 12: Error Handling and Data Quality

**User Story:** As a researcher, I want the system to handle data quality issues gracefully, so that I can identify and address problems in the survey data.

#### Acceptance Criteria

1. WHEN the System encounters missing values, THE System SHALL handle them according to predefined rules (assign 0 for scores, null for calculations)
2. WHEN the System encounters invalid values (negative numbers, out-of-range responses), THE System SHALL flag these records in a data quality report
3. THE System SHALL generate a data quality report listing all issues found with row numbers and variable names
4. THE System SHALL continue processing valid records even when some records contain errors
5. THE System SHALL save the data quality report to the Output_Folder
