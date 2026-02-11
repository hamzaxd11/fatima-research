# Menstrual Hygiene Analysis System

A Python-based data analysis pipeline for medical research that processes SPSS survey data to analyze menstrual hygiene awareness among adolescent girls in sub-urban Lahore, Pakistan.

## Overview

This system analyzes the relationship between maternal education and menstrual hygiene knowledge and practices among adolescent girls. It processes survey data, calculates derived metrics and scores, performs statistical analyses, and generates comprehensive reports with visualizations.

## Features

- SPSS (.sav) file import and validation
- Automated calculation of knowledge and practice scores
- Statistical analysis of maternal education impact
- Demographic summary statistics
- Data visualization (bar charts, histograms, box plots, scatter plots)
- Comprehensive analysis reports
- Data quality reporting

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Operating System: Windows, macOS, or Linux

### Setup Instructions

1. **Clone or download this repository**

   ```bash
   git clone <repository-url>
   cd menstrual-hygiene-analysis
   ```

   Or download and extract the ZIP file to your desired location.

2. **Create a virtual environment (recommended)**

   This isolates the project dependencies from your system Python installation.

   On Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   On macOS/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install required dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   This will install:
   - pandas (≥2.0.0) - Data manipulation and analysis
   - numpy (≥1.24.0) - Numerical computing
   - scipy (≥1.10.0) - Statistical tests
   - matplotlib (≥3.7.0) - Data visualization
   - pyreadstat (≥1.2.0) - SPSS file reading
   - hypothesis (≥6.82.0) - Property-based testing (for development)

4. **Verify installation**

   ```bash
   python -c "import pandas, numpy, scipy, matplotlib, pyreadstat; print('All dependencies installed successfully!')"
   ```

### Troubleshooting Installation

- **pyreadstat installation fails**: This package requires C compilers. On Windows, install Microsoft C++ Build Tools. On macOS, install Xcode Command Line Tools with `xcode-select --install`. On Linux, install `build-essential` package.

- **Permission errors**: Use `pip install --user -r requirements.txt` to install packages for your user only.

- **Python version issues**: Verify your Python version with `python --version`. If you have multiple Python versions, use `python3` instead of `python`.

## Usage

### Basic Usage

Run the analysis with a single command:

```bash
python analyze.py <path_to_spss_file> [output_folder_path]
```

### Command-Line Arguments

- `spss_file_path` (required): Path to the SPSS .sav file containing survey data
- `output_folder_path` (optional): Base directory where analysis results will be saved. Defaults to "output" if not specified. A timestamped subfolder will be created automatically.

### Usage Examples

**Example 1: Basic usage with default output folder**
```bash
python analyze.py "survey_data.sav"
```
This creates output in `output/analysis_YYYYMMDD_HHMMSS/`

**Example 2: Specify custom output location**
```bash
python analyze.py "menstrual hygiene spss.sav fatima and ayesha (1).sav" results
```
This creates output in `results/analysis_YYYYMMDD_HHMMSS/`

**Example 3: Using absolute paths**
```bash
python analyze.py "C:\Users\Researcher\Data\survey.sav" "C:\Users\Researcher\Results"
```

**Example 4: File paths with spaces (use quotes)**
```bash
python analyze.py "path/to/my survey data.sav" "my analysis results"
```

**Example 5: Get help**
```bash
python analyze.py --help
```

### What Happens During Execution

When you run the analysis, the system will:

1. **Create output folder** - A timestamped folder is created to store all results
2. **Load SPSS data** - Reads and validates the .sav file
3. **Process data** - Calculates scores and derived fields
4. **Assess quality** - Checks for missing and invalid values
5. **Perform analysis** - Runs statistical tests and generates summaries
6. **Create visualizations** - Generates all charts and graphs
7. **Generate report** - Creates comprehensive analysis report

Progress messages are displayed at each stage. The entire process typically takes 10-30 seconds depending on dataset size.

## Output Files

The system generates a timestamped output folder (e.g., `output/analysis_20240211_143022/`) containing all analysis results. This prevents overwriting previous analyses.

### Data Files

**scored_dataset.csv**
- Complete dataset with all original variables plus calculated fields
- Includes: per_capita_income, knowledge_score, practice_score, total_score
- Use this file for further analysis or verification of calculations
- Format: CSV with headers, UTF-8 encoding

**maternal_education_summary.csv**
- Summary statistics grouped by maternal education level
- Columns: education_level, n (sample size), mean_knowledge, std_knowledge, mean_practice, std_practice
- Includes statistical significance indicators
- Use this for quick comparison across education groups

**demographic_*.csv files**
- Frequency distributions for categorical variables (age, education, occupation)
- Includes counts, percentages, and proportions
- Separate files for each demographic variable analyzed

**correlation_matrix.csv**
- Pearson correlation coefficients between all continuous variables
- Symmetric matrix format with variable names as row/column headers
- Values range from -1 (perfect negative correlation) to +1 (perfect positive correlation)

**data_quality_*.csv files**
- Lists all missing values with row numbers and variable names
- Lists all invalid values with details about the issue
- Use these files to identify and address data quality problems

### Visualizations (PNG format, 300 DPI)

All visualizations are publication-ready with high resolution (300 DPI) suitable for research papers and presentations.

**scores_by_maternal_education.png**
- Grouped bar chart showing mean knowledge and practice scores by maternal education level
- Includes error bars representing standard deviations
- Color-coded: Blue for knowledge scores, Red for practice scores
- Dimensions: 10" × 6"

**score_distributions.png**
- Side-by-side histograms showing frequency distributions
- Left panel: Knowledge scores (0-9 scale)
- Right panel: Practice scores (0-7 scale)
- Includes mean lines for reference
- Dimensions: 12" × 5"

**score_boxplots.png**
- Box plots comparing score distributions across maternal education groups
- Shows median, quartiles, and outliers for each group
- Left panel: Knowledge scores, Right panel: Practice scores
- Useful for identifying group differences and data spread
- Dimensions: 14" × 6"

**scatter_matrix.png**
- Matrix of scatter plots showing relationships between continuous variables
- Includes: age, income, family size, per capita income, knowledge score, practice score
- Diagonal shows histograms of each variable
- Off-diagonal shows pairwise scatter plots
- Useful for identifying correlations and patterns
- Dimensions: 12" × 12"

### Reports

**analysis_report.txt**
- Comprehensive plain text report of all findings
- Sections: Demographics, Knowledge Scores, Practice Scores, Maternal Education Analysis, Correlations
- Includes statistical test results with interpretations
- References all generated tables and charts
- Suitable for printing or email

**analysis_report.md**
- Same content as TXT report but in Markdown format
- Can be rendered in GitHub, Jupyter notebooks, or converted to HTML/PDF
- Better formatting for digital viewing

**data_quality_summary.txt**
- Summary of data quality assessment
- Lists total missing values, invalid values, and affected rows/columns
- Includes data quality percentage score
- Warnings and recommendations for data cleaning

**FILE_INVENTORY.md**
- Complete list of all generated files with descriptions and file sizes
- Useful for understanding what was generated and locating specific outputs

**analysis.log**
- Detailed execution log with timestamps
- Records all analysis parameters (file paths, settings)
- Includes progress messages and any warnings/errors
- Useful for troubleshooting and reproducibility

## Project Structure

```
.
├── src/                          # Source code modules
│   ├── data_loader.py           # SPSS file reading and validation
│   ├── data_processor.py        # Score calculations and derived fields
│   ├── statistical_analysis.py  # Statistical tests and summaries
│   ├── visualizations.py        # Chart and graph generation
│   ├── report_generator.py      # Report creation
│   ├── output_manager.py        # Output file management
│   └── data_quality.py          # Data quality checks
├── tests/                        # Test suite
│   ├── unit/                    # Unit tests
│   ├── property/                # Property-based tests
│   ├── integration/             # Integration tests
│   └── fixtures/                # Test data and fixtures
├── output/                       # Analysis outputs (generated)
├── analyze.py                    # Main entry point script
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Data Requirements

The SPSS file should contain the following variables:

### Demographics
- `age`: Respondent age
- `mother_education`: Maternal education level
- `father_education`: Paternal education level
- `mother_occupation`: Maternal occupation
- `father_occupation`: Paternal occupation
- `income_per_month`: Monthly family income
- `no_family_members_male`: Number of male family members
- `no_family_members_female`: Number of female family members

### Knowledge Questions (Section III)
- `q3_1` through `q3_9`: Nine knowledge assessment questions

### Practice Questions (Section IV)
- `q4_1` through `q4_7`: Seven practice assessment questions

## Scoring System

### Knowledge Score (0-9)
Calculated from Section III responses according to questionnaire scoring guidelines. Missing responses are assigned a score of 0.

### Practice Score (0-7)
Calculated from Section IV responses according to questionnaire scoring guidelines. Missing responses are assigned a score of 0.

### Per Capita Income
Calculated as: Monthly Income / Total Family Members (rounded to 2 decimal places)

## Statistical Methods

- **Descriptive Statistics**: Mean, median, standard deviation, min, max
- **Frequency Distributions**: For categorical variables
- **Statistical Tests**: ANOVA or Kruskal-Wallis test for group comparisons
- **Correlation Analysis**: Pearson correlation for continuous variables

## Error Handling

The system handles various error conditions gracefully:

- Missing or invalid SPSS files
- Missing data values (assigned score of 0 for questionnaire responses)
- Division by zero (per capita income set to null)
- Invalid or out-of-range values (flagged in data quality report)
- Insufficient data for statistical tests (noted in report)

## Troubleshooting

### Common Issues and Solutions

#### File Not Found Errors

**Problem**: `FileNotFoundError: SPSS file not found at path: ...`

**Solutions**:
- Verify the file path is correct and the file exists
- Use absolute paths instead of relative paths if unsure
- On Windows, use forward slashes (/) or double backslashes (\\\\) in paths
- Put file paths with spaces in quotes: `"my file.sav"`
- Check that you're running the command from the correct directory

**Example**:
```bash
# Wrong (relative path, file not in current directory)
python analyze.py data.sav

# Right (absolute path)
python analyze.py "C:/Users/Researcher/Documents/data.sav"
```

#### SPSS File Reading Errors

**Problem**: `Error reading SPSS file` or `Cannot read SPSS file`

**Solutions**:
- Ensure the file is a valid SPSS .sav format (not .por or .zsav)
- Check if the file is corrupted by opening it in SPSS first
- Verify the file is not open in another program
- Try re-exporting the file from SPSS
- Ensure pyreadstat is installed correctly: `pip install --upgrade pyreadstat`

**Problem**: `pyreadstat` installation fails

**Solutions**:
- **Windows**: Install Microsoft C++ Build Tools from https://visualstudio.microsoft.com/visual-cpp-build-tools/
- **macOS**: Install Xcode Command Line Tools: `xcode-select --install`
- **Linux**: Install build essentials: `sudo apt-get install build-essential` (Ubuntu/Debian)

#### Permission Errors

**Problem**: `PermissionError: Cannot read file` or `Cannot create output folder`

**Solutions**:
- Check file permissions - ensure you have read access to the SPSS file
- Ensure you have write permissions for the output directory
- On Windows, run Command Prompt as Administrator if needed
- Don't use system-protected directories (like C:\\ root) for output
- Close the SPSS file if it's open in another program

#### Missing Output Files

**Problem**: Some expected output files are not generated

**Solutions**:
- Check the analysis.log file for errors or warnings
- Review the data_quality_summary.txt for data issues
- Ensure your dataset has the required columns (see Data Requirements section)
- Some outputs are only generated if sufficient data exists (e.g., maternal education analysis requires maternal education column)
- Check console output for warning messages

#### Statistical Test Failures

**Problem**: `Statistical test failed` or `Insufficient data for statistics`

**Solutions**:
- Verify you have at least 2 groups with data for group comparisons
- Check for excessive missing values in key variables
- Review data_quality_summary.txt for issues
- Ensure maternal education column exists and has valid values
- Need at least 3 observations per group for meaningful statistics

#### Visualization Errors

**Problem**: Charts are not generated or appear blank

**Solutions**:
- Ensure matplotlib is installed: `pip install --upgrade matplotlib`
- Check that you have sufficient data for visualization
- Review analysis.log for specific error messages
- Verify your system supports graphical output (some servers don't)
- Try updating matplotlib: `pip install --upgrade matplotlib`

#### Memory Errors

**Problem**: `MemoryError` or system runs out of memory

**Solutions**:
- Close other applications to free up RAM
- For very large datasets (>100,000 rows), consider using a machine with more RAM
- Process data in chunks if possible
- Check if your dataset has unexpectedly large file size

#### Python Version Issues

**Problem**: `SyntaxError` or `ModuleNotFoundError`

**Solutions**:
- Verify Python version: `python --version` (need 3.8 or higher)
- Use `python3` instead of `python` if you have multiple versions
- Recreate virtual environment with correct Python version
- Update pip: `python -m pip install --upgrade pip`

#### Encoding Errors

**Problem**: `UnicodeDecodeError` or garbled text in outputs

**Solutions**:
- Ensure your SPSS file uses UTF-8 or compatible encoding
- On Windows, use Command Prompt with UTF-8: `chcp 65001`
- Check that variable names don't contain special characters
- Re-export SPSS file with UTF-8 encoding if possible

### Getting Help

If you encounter issues not covered here:

1. Check the `analysis.log` file in the output folder for detailed error messages
2. Review the `data_quality_summary.txt` for data-related issues
3. Ensure all dependencies are up to date: `pip install --upgrade -r requirements.txt`
4. Try running with a small test dataset to isolate the issue
5. Contact the research supervisors:
   - Dr. Naureen Omar
   - Dr. Ayesha Javed
   - Dr. Fatima Sohail

### Reporting Bugs

When reporting issues, please include:
- Python version (`python --version`)
- Operating system and version
- Full error message from console
- Contents of analysis.log file
- Sample of your data structure (column names, not actual data)

## Example Analysis Workflow

This section provides a complete walkthrough of analyzing menstrual hygiene survey data from start to finish.

### Step 1: Prepare Your Environment

```bash
# Navigate to project directory
cd menstrual-hygiene-analysis

# Activate virtual environment (if using one)
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Verify installation
python -c "import pandas, pyreadstat; print('Ready to analyze!')"
```

### Step 2: Prepare Your Data

Ensure your SPSS file contains the required variables:

**Required demographic variables**:
- Age or similar age field
- Mother education or maternal education field
- Income per month
- Number of family members (male and female)

**Required questionnaire variables**:
- Section III questions (Q3_1 through Q3_9) for knowledge assessment
- Section IV questions (Q4_1 through Q4_7) for practice assessment

**Tip**: Open your SPSS file in SPSS first to verify variable names and check for obvious data issues.

### Step 3: Run the Analysis

```bash
# Basic command
python analyze.py "menstrual hygiene spss.sav fatima and ayesha (1).sav" output

# You'll see progress messages like:
# [1/7] Creating output folder...
# [2/7] Loading SPSS data file...
# [3/7] Processing data and calculating scores...
# [4/7] Assessing data quality...
# [5/7] Performing statistical analyses...
# [6/7] Generating visualizations...
# [7/7] Generating analysis report...
```

The analysis typically completes in 10-30 seconds.

### Step 4: Review Data Quality

Before interpreting results, check data quality:

```bash
# Navigate to output folder
cd output/analysis_20240211_143022  # Use your actual timestamp

# Open data quality summary
notepad data_quality_summary.txt  # Windows
cat data_quality_summary.txt      # macOS/Linux
```

**What to look for**:
- Data quality percentage (aim for >90%)
- Number of missing values
- Number of invalid values
- Affected rows and columns

**Action items**:
- If data quality is low (<80%), review the missing/invalid value CSV files
- Consider cleaning the original data and re-running analysis
- Document any data quality issues in your research notes

### Step 5: Review Statistical Results

Open the main analysis report:

```bash
notepad analysis_report.txt  # Windows
cat analysis_report.txt      # macOS/Linux
```

**Key sections to review**:

1. **Demographics Summary** - Understand your sample characteristics
   - Check sample size and distribution
   - Verify age ranges are appropriate
   - Review education level distributions

2. **Knowledge Scores Analysis** - Assess awareness levels
   - Note mean and median scores
   - Check score distribution (are most scores high or low?)
   - Identify any unusual patterns

3. **Practice Scores Analysis** - Evaluate actual behaviors
   - Compare practice scores to knowledge scores
   - Look for knowledge-practice gaps
   - Note areas where practice is particularly low

4. **Maternal Education Impact** - Main research question
   - Review mean scores by education level
   - Check statistical significance (p-values)
   - Note effect sizes and practical significance

### Step 6: Examine Visualizations

Open the PNG files to visualize your findings:

**scores_by_maternal_education.png**
- Shows clear comparison across education groups
- Error bars indicate variability within groups
- Use this chart in presentations and papers

**score_distributions.png**
- Shows overall score patterns
- Identify if scores are normally distributed
- Check for ceiling/floor effects

**score_boxplots.png**
- Shows median, quartiles, and outliers
- Useful for identifying group differences
- Reveals data spread and skewness

**scatter_matrix.png**
- Explore relationships between variables
- Identify potential confounding factors
- Check for unexpected correlations

### Step 7: Interpret Statistical Tests

From the analysis report, interpret the maternal education analysis:

**If p < 0.05** (statistically significant):
- There IS a significant relationship between maternal education and scores
- Higher maternal education is associated with different awareness/practice levels
- This supports the hypothesis that maternal education influences adolescent hygiene awareness

**If p ≥ 0.05** (not statistically significant):
- No significant relationship detected in this sample
- Differences between groups may be due to chance
- Consider sample size, data quality, or other factors

**Important**: Statistical significance doesn't always mean practical significance. Consider:
- Effect size (how large are the differences?)
- Clinical/practical relevance (are differences meaningful in real life?)
- Sample size (small samples may miss real effects)

### Step 8: Use Results in Your Research

**For your research paper**:
1. Copy relevant statistics from analysis_report.txt
2. Insert visualizations (PNG files) as figures
3. Reference the scored_dataset.csv for detailed results
4. Cite statistical methods used (ANOVA/Kruskal-Wallis)

**For presentations**:
1. Use bar charts and box plots for clear visual communication
2. Highlight key statistics (means, p-values)
3. Show data quality metrics to establish credibility

**For further analysis**:
1. Open scored_dataset.csv in Excel or SPSS for additional analyses
2. Use correlation_matrix.csv to explore relationships
3. Filter data by specific groups for subgroup analyses

### Step 9: Document Your Analysis

Create a research log documenting:
- Date of analysis
- SPSS file used (with version/date)
- Output folder location
- Key findings and interpretations
- Any data quality issues encountered
- Decisions made during analysis

**Tip**: Keep the entire output folder as a record. The analysis.log file contains all parameters for reproducibility.

### Step 10: Reproduce or Update Analysis

If you need to re-run with updated data:

```bash
# New analysis with updated data
python analyze.py "updated_survey_data.sav" output

# This creates a new timestamped folder, preserving previous results
```

**Best practices**:
- Never delete previous analysis folders until paper is published
- Document what changed between analyses
- Compare results across different data versions
- Keep original SPSS files backed up

### Complete Example Session

```bash
# Full workflow from start to finish
cd menstrual-hygiene-analysis
venv\Scripts\activate
python analyze.py "survey_data.sav" results
cd results/analysis_20240211_143022
notepad data_quality_summary.txt
notepad analysis_report.txt
explorer .  # Opens folder in Windows Explorer to view charts
```

### Tips for Success

1. **Always check data quality first** - Don't interpret results from poor quality data
2. **Review visualizations** - Charts often reveal issues not obvious in statistics
3. **Consider context** - Statistical significance must be interpreted in research context
4. **Document everything** - Keep detailed notes for reproducibility
5. **Backup your work** - Keep copies of data, outputs, and analysis logs
6. **Consult supervisors** - Discuss unexpected findings before finalizing conclusions

## Dependencies

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **scipy**: Statistical tests and functions
- **matplotlib**: Data visualization
- **pyreadstat**: SPSS file reading
- **hypothesis**: Property-based testing (development)

## Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run unit tests only
python -m pytest tests/unit/

# Run property-based tests
python -m pytest tests/property/

# Run integration tests
python -m pytest tests/integration/
```

## License

This project is developed for medical research purposes at [Institution Name].

## Contact

For questions or issues, please contact:
- Dr. Naureen Omar
- Dr. Ayesha Javed
- Dr. Fatima Sohail

## Acknowledgments

This system was developed to support MBBS student research on menstrual hygiene awareness among adolescent girls in sub-urban Lahore, Pakistan.
