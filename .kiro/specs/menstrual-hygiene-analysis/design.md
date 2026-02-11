# Design Document

## Overview

This system is a Python-based data analysis pipeline for medical research that processes SPSS survey data, calculates derived metrics and scores, performs statistical analyses, and generates comprehensive reports with visualizations. The design follows a modular architecture with clear separation between data processing, analysis, and output generation components.

The system will use standard Python scientific computing libraries (pandas, numpy, scipy, matplotlib) to ensure reliability and maintainability. The architecture emphasizes simplicity and reproducibility, with a single entry point script that orchestrates all analysis steps.

## Architecture

The system follows a pipeline architecture with four main stages:

1. **Data Ingestion Stage**: Reads SPSS files and validates data structure
2. **Data Processing Stage**: Calculates derived fields and scores
3. **Analysis Stage**: Performs statistical analyses and generates summaries
4. **Output Stage**: Creates visualizations and reports

```
[SPSS File] → [Data Ingestion] → [Data Processing] → [Analysis] → [Output Generation]
                     ↓                  ↓                ↓              ↓
                [Validation]      [Scoring]      [Statistics]    [Files/Reports]
```

The pipeline is orchestrated by a main entry point script (`analyze.py`) that calls each stage in sequence, handles errors, and manages output directories.

## Components and Interfaces

### 1. Data Ingestion Module (`data_loader.py`)

**Responsibilities:**
- Read SPSS .sav files using pyreadstat library
- Validate data structure and types
- Report data quality issues

**Key Functions:**
- `load_spss_file(file_path: str) -> tuple[pd.DataFrame, dict]`
  - Returns: DataFrame with data, dictionary with metadata
  - Raises: FileNotFoundError, SPSSReadError

- `validate_required_columns(df: pd.DataFrame, required_cols: list) -> list`
  - Returns: List of missing column names
  
- `generate_data_summary(df: pd.DataFrame) -> dict`
  - Returns: Dictionary with row count, column count, column names, data types

### 2. Data Processing Module (`data_processor.py`)

**Responsibilities:**
- Calculate per capita income
- Map questionnaire responses to scores
- Calculate knowledge and practice scores
- Handle missing values

**Key Functions:**
- `calculate_per_capita_income(df: pd.DataFrame) -> pd.DataFrame`
  - Adds 'per_capita_income' column
  - Handles division by zero and missing values

- `calculate_knowledge_score(df: pd.DataFrame, question_columns: list) -> pd.DataFrame`
  - Adds 'knowledge_score' column (0-9)
  - Applies scoring rules from questionnaire

- `calculate_practice_score(df: pd.DataFrame, question_columns: list) -> pd.DataFrame`
  - Adds 'practice_score' column (0-7)
  - Applies scoring rules from questionnaire

- `create_scored_dataset(df: pd.DataFrame) -> pd.DataFrame`
  - Orchestrates all scoring calculations
  - Returns complete dataset with all derived fields

### 3. Statistical Analysis Module (`statistical_analysis.py`)

**Responsibilities:**
- Perform maternal education analysis
- Calculate demographic summaries
- Conduct statistical tests
- Generate summary tables

**Key Functions:**
- `analyze_maternal_education_impact(df: pd.DataFrame) -> dict`
  - Groups by maternal education level
  - Calculates mean, std for knowledge and practice scores
  - Performs ANOVA/Kruskal-Wallis test
  - Returns: Dictionary with statistics and p-values

- `calculate_demographic_summaries(df: pd.DataFrame) -> dict`
  - Generates frequency tables for categorical variables
  - Calculates descriptive statistics for continuous variables
  - Returns: Dictionary of summary DataFrames

- `perform_correlation_analysis(df: pd.DataFrame) -> pd.DataFrame`
  - Calculates correlations between continuous variables
  - Returns: Correlation matrix

### 4. Visualization Module (`visualizations.py`)

**Responsibilities:**
- Generate all charts and graphs
- Apply consistent styling
- Save figures to output folder

**Key Functions:**
- `plot_scores_by_maternal_education(df: pd.DataFrame, output_path: str) -> None`
  - Creates bar chart with error bars
  - Saves to PNG at 300 DPI

- `plot_score_distributions(df: pd.DataFrame, output_path: str) -> None`
  - Creates histograms for knowledge and practice scores
  - Saves to PNG at 300 DPI

- `plot_score_boxplots(df: pd.DataFrame, output_path: str) -> None`
  - Creates box plots by maternal education group
  - Saves to PNG at 300 DPI

- `plot_scatter_matrix(df: pd.DataFrame, output_path: str) -> None`
  - Creates scatter plots for continuous variable relationships
  - Saves to PNG at 300 DPI

### 5. Report Generation Module (`report_generator.py`)

**Responsibilities:**
- Generate analysis report document
- Compile all findings into readable format
- Reference tables and figures

**Key Functions:**
- `generate_analysis_report(analysis_results: dict, output_folder: str) -> None`
  - Creates comprehensive text and markdown reports
  - Includes all statistical findings
  - References all generated files

### 6. Output Manager Module (`output_manager.py`)

**Responsibilities:**
- Create and manage output directory
- Save files with descriptive names
- Handle file naming conflicts
- Generate file inventory

**Key Functions:**
- `create_output_folder(base_path: str) -> str`
  - Creates output directory with timestamp
  - Returns: Path to output folder

- `save_dataframe(df: pd.DataFrame, filename: str, output_folder: str) -> str`
  - Saves DataFrame to CSV
  - Returns: Full file path

- `generate_file_inventory(output_folder: str) -> None`
  - Creates inventory of all output files with descriptions

### 7. Main Entry Point (`analyze.py`)

**Responsibilities:**
- Orchestrate entire analysis pipeline
- Handle command-line arguments
- Display progress messages
- Handle errors and logging

**Key Functions:**
- `main(spss_file_path: str, output_base_path: str) -> None`
  - Executes all pipeline stages
  - Handles errors and displays messages

## Data Models

### Input Data Structure (from SPSS file)

Expected columns based on questionnaire:
- Demographics: `age`, `mother_education`, `father_education`, `mother_occupation`, `father_occupation`, `income_per_month`, `no_family_members_male`, `no_family_members_female`
- Menstrual History: `age_at_menarche`, `knew_before_menarche`, `information_source`
- Knowledge Questions (Section III): `q3_1` through `q3_9` (9 questions)
- Practice Questions (Section IV): `q4_1` through `q4_7` (7 questions)

### Scored Dataset Structure

All original columns plus:
- `total_family_members`: Sum of male and female family members
- `per_capita_income`: Calculated field (income / family members)
- `knowledge_score`: Integer 0-9
- `practice_score`: Integer 0-7
- `total_score`: Sum of knowledge and practice scores (0-16)

### Analysis Results Structure

```python
{
    'maternal_education_analysis': {
        'summary_table': pd.DataFrame,  # Education level, n, mean_knowledge, std_knowledge, mean_practice, std_practice
        'anova_knowledge': {'f_statistic': float, 'p_value': float},
        'anova_practice': {'f_statistic': float, 'p_value': float}
    },
    'demographic_summaries': {
        'age_distribution': pd.DataFrame,
        'education_frequencies': pd.DataFrame,
        'income_statistics': pd.DataFrame,
        'family_size_statistics': pd.DataFrame
    },
    'correlations': pd.DataFrame,
    'data_quality_report': {
        'missing_values': pd.DataFrame,
        'invalid_values': pd.DataFrame,
        'warnings': list
    }
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property Reflection

After analyzing all acceptance criteria, I identified several areas of redundancy:

1. **Score validation properties (3.4, 4.4)** can be combined with score calculation properties (3.2, 4.2) since valid range is inherent to correct calculation
2. **Column existence properties (2.4, 3.5, 4.5)** can be combined into a single property about scored dataset structure
3. **File output properties (8.2, 8.3, 8.4, 8.5)** can be combined into a comprehensive output completeness property
4. **Report content properties (9.2, 9.3, 9.4)** can be combined into a single report completeness property
5. **Missing value handling (3.3, 4.3, 12.1)** can be combined into a single consistent missing value handling property
6. **Statistical calculation properties (5.2, 5.3, 6.2)** are similar and can be grouped as correct statistical computation

This reflection reduces ~60 testable criteria to ~25 unique, non-redundant properties.

### Core Properties

**Property 1: SPSS Data Preservation**
*For any* valid SPSS .sav file, loading the file and extracting data should preserve all original values, data types, and structure without loss or modification.
**Validates: Requirements 1.1, 1.4**

**Property 2: Data Quality Detection**
*For any* dataset with missing or invalid values, the system should identify and report all issues with specific row and column references in the data quality report.
**Validates: Requirements 1.2, 12.2, 12.3**

**Property 3: Import Summary Completeness**
*For any* successfully loaded dataset, the import summary should contain the total record count, all variable names, and data type information.
**Validates: Requirements 1.3**

**Property 4: Error Message Descriptiveness**
*For any* invalid or unreadable SPSS file, the system should produce an error message containing both the file path and the specific error type.
**Validates: Requirements 1.5**

**Property 5: Per Capita Income Calculation Correctness**
*For any* record with valid (non-zero, non-null) income and family member values, the calculated per capita income should equal income divided by family members, rounded to 2 decimal places.
**Validates: Requirements 2.1, 2.5**

**Property 6: Division by Zero Prevention**
*For any* record where family member count is zero or null, the system should set per capita income to null and not raise a division error.
**Validates: Requirements 2.2, 2.3**

**Property 7: Knowledge Score Calculation Correctness**
*For any* set of Section III responses, the calculated knowledge score should equal the sum of individual question scores according to the questionnaire guidelines, and be within the range 0-9.
**Validates: Requirements 3.1, 3.2, 3.4**

**Property 8: Practice Score Calculation Correctness**
*For any* set of Section IV responses, the calculated practice score should equal the sum of individual question scores according to the questionnaire guidelines, and be within the range 0-7.
**Validates: Requirements 4.1, 4.2, 4.4**

**Property 9: Missing Response Handling Consistency**
*For any* questionnaire response with missing values, the system should assign a score of 0 for each missing response consistently across all questions.
**Validates: Requirements 3.3, 4.3, 12.1**

**Property 10: Scored Dataset Structure Completeness**
*For any* processed dataset, the scored dataset should contain all original columns plus the derived columns: total_family_members, per_capita_income, knowledge_score, practice_score.
**Validates: Requirements 2.4, 3.5, 4.5**

**Property 11: Maternal Education Grouping Correctness**
*For any* dataset with maternal education data, grouping by maternal education level should partition all records exactly once with no duplicates or omissions.
**Validates: Requirements 5.1**

**Property 12: Statistical Calculation Accuracy**
*For any* grouped data, calculated means and standard deviations for knowledge and practice scores should match the mathematical definitions (mean = sum/count, std = sqrt(variance)).
**Validates: Requirements 5.2, 5.3, 6.2**

**Property 13: Statistical Test Execution**
*For any* maternal education analysis, the system should perform ANOVA or Kruskal-Wallis tests and return valid p-values (0 ≤ p ≤ 1) and confidence intervals.
**Validates: Requirements 5.4, 5.5**

**Property 14: Summary Table Completeness**
*For any* maternal education analysis, the summary table should contain columns for education level, sample size, mean knowledge score, std knowledge score, mean practice score, std practice score, and statistical significance indicators.
**Validates: Requirements 5.6**

**Property 15: Frequency Distribution Validity**
*For any* categorical variable, the sum of frequencies across all categories should equal the total number of records, and percentages should sum to 100%.
**Validates: Requirements 6.1, 6.4**

**Property 16: Cross-Tabulation Consistency**
*For any* cross-tabulation of two categorical variables, the sum of all cells should equal the total record count, and marginal totals should match individual frequency distributions.
**Validates: Requirements 6.3**

**Property 17: Visualization File Format Compliance**
*For any* generated visualization, the saved file should be in PNG format with resolution ≥ 300 DPI.
**Validates: Requirements 7.5**

**Property 18: Output Directory Creation**
*For any* analysis execution, if the output folder does not exist, it should be created before any files are written.
**Validates: Requirements 8.1**

**Property 19: Output File Completeness**
*For any* completed analysis, the output folder should contain the scored dataset CSV, all statistical summary tables, all visualization files, and the analysis report in both TXT and Markdown formats.
**Validates: Requirements 8.2, 8.3, 8.4, 8.5, 9.5**

**Property 20: File Overwrite Prevention**
*For any* analysis execution when output files already exist, new files should be created with timestamp suffixes rather than overwriting existing files.
**Validates: Requirements 8.6**

**Property 21: Analysis Report Structure**
*For any* generated analysis report, it should contain sections for demographics, knowledge scores, practice scores, maternal education analysis, statistical test results, and references to all generated tables and charts.
**Validates: Requirements 9.1, 9.2, 9.3, 9.4**

**Property 22: Pipeline Completeness**
*For any* successful execution of the entry point script, all pipeline stages (data loading, processing, scoring, analysis, visualization, reporting) should complete and produce their expected outputs.
**Validates: Requirements 10.2**

**Property 23: Error Propagation and Halting**
*For any* pipeline stage that encounters a fatal error, the system should halt execution, display an error message, and not proceed to subsequent stages.
**Validates: Requirements 10.4**

**Property 24: Analysis Parameter Logging**
*For any* analysis execution, all parameters (file paths, statistical test choices, significance levels) should be recorded in a log file in the output folder.
**Validates: Requirements 11.3**

**Property 25: Fault Tolerance for Partial Data**
*For any* dataset containing some invalid records, the system should process all valid records and produce results while flagging invalid records in the data quality report.
**Validates: Requirements 12.4, 12.5**

## Error Handling

The system implements a layered error handling strategy:

### Data Loading Errors
- **FileNotFoundError**: Display clear message with file path, suggest checking file location
- **SPSSReadError**: Display message indicating file corruption or format issues
- **PermissionError**: Display message about file access permissions

### Data Processing Errors
- **Missing Required Columns**: Log warning, list missing columns, halt processing
- **Invalid Data Types**: Flag records in data quality report, continue with valid records
- **Division by Zero**: Set result to null, log warning with row number
- **Out of Range Values**: Flag in data quality report, use default value (0 for scores)

### Analysis Errors
- **Insufficient Data for Statistics**: Display warning, skip statistical test, note in report
- **Empty Groups**: Display warning, exclude from analysis, note in report
- **Statistical Test Failures**: Log error details, mark results as unavailable in report

### Output Errors
- **Directory Creation Failure**: Display error, suggest checking permissions, halt
- **File Write Failure**: Display error with filename, suggest checking disk space/permissions
- **Visualization Errors**: Log error, continue with other visualizations, note missing charts in report

### General Error Handling Principles
1. Fail fast for fatal errors (missing input file, cannot create output directory)
2. Continue processing for recoverable errors (invalid individual records)
3. Always log errors with context (row numbers, column names, values)
4. Provide actionable error messages to users
5. Generate data quality report even if analysis fails

## Testing Strategy

The system will employ a dual testing approach combining unit tests for specific scenarios and property-based tests for comprehensive validation.

### Unit Testing Approach

Unit tests will focus on:
- **Specific examples**: Test scoring logic with known questionnaire responses
- **Edge cases**: Empty datasets, single-record datasets, all-missing data
- **Error conditions**: Invalid file paths, corrupted SPSS files, permission errors
- **Integration points**: Module interactions, data flow between pipeline stages

Example unit tests:
- Test knowledge score calculation with all correct answers (should equal 9)
- Test practice score calculation with all incorrect answers (should equal 0)
- Test per capita income with family size = 1 (should equal total income)
- Test loading non-existent file (should raise FileNotFoundError)
- Test creating output folder when parent directory doesn't exist

### Property-Based Testing Approach

Property-based tests will verify universal properties across randomized inputs using the Hypothesis library for Python. Each test will run a minimum of 100 iterations with generated data.

**Test Configuration**:
- Library: Hypothesis (Python property-based testing framework)
- Iterations: 100 minimum per property test
- Tagging: Each test tagged with feature name and property number

**Property Test Coverage**:
- Properties 1-25 (listed above) will each have a corresponding property-based test
- Each test will generate random valid inputs within constraints
- Tests will verify the property holds across all generated inputs

**Example Property Test Structure**:
```python
# Feature: menstrual-hygiene-analysis, Property 5: Per Capita Income Calculation Correctness
@given(income=st.floats(min_value=0.01, max_value=1000000),
       family_size=st.integers(min_value=1, max_value=50))
def test_per_capita_income_calculation(income, family_size):
    df = create_test_dataframe(income, family_size)
    result = calculate_per_capita_income(df)
    expected = round(income / family_size, 2)
    assert result['per_capita_income'].iloc[0] == expected
```

### Test Data Generation

For property-based tests, we will generate:
- **Random SPSS files**: Using pyreadstat to create valid .sav files with random data
- **Random questionnaire responses**: Valid response codes from questionnaire
- **Random demographics**: Age (10-19), education levels, income ranges, family sizes
- **Edge case data**: Missing values, zeros, nulls, extreme values
- **Invalid data**: Out-of-range values, wrong types, corrupted structures

### Integration Testing

Integration tests will verify:
- Complete pipeline execution from SPSS file to final reports
- Correct data flow between all modules
- Output file generation and naming
- Report content accuracy and completeness

### Test Organization

```
tests/
├── unit/
│   ├── test_data_loader.py
│   ├── test_data_processor.py
│   ├── test_statistical_analysis.py
│   ├── test_visualizations.py
│   ├── test_report_generator.py
│   └── test_output_manager.py
├── property/
│   ├── test_properties_data_loading.py      # Properties 1-4
│   ├── test_properties_calculations.py      # Properties 5-10
│   ├── test_properties_statistics.py        # Properties 11-16
│   ├── test_properties_output.py            # Properties 17-21
│   └── test_properties_pipeline.py          # Properties 22-25
├── integration/
│   └── test_full_pipeline.py
└── fixtures/
    ├── sample_spss_files/
    └── expected_outputs/
```

### Continuous Validation

- All tests run automatically before commits
- Property tests ensure correctness across wide input space
- Unit tests catch specific regressions
- Integration tests verify end-to-end functionality
- Data quality reports provide runtime validation

This dual approach ensures both specific correctness (unit tests) and general correctness (property tests), providing high confidence in system reliability for medical research applications.
