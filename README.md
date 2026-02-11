# Menstrual Hygiene Analysis System

A Python-based data analysis pipeline for analyzing menstrual hygiene awareness among adolescent girls in sub-urban Lahore, Pakistan.

## Overview

This system analyzes the relationship between maternal education and menstrual hygiene knowledge and practices. It processes SPSS survey data, calculates scores, performs statistical analyses, and generates comprehensive reports with visualizations.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Verify installation**

   ```bash
   python -c "import pandas, numpy, scipy, matplotlib, pyreadstat; print('Ready!')"
   ```

## Usage

### Run Analysis

```bash
python analyze.py "menstrual hygiene spss.sav fatima and ayesha (1).sav"
```

This will:
1. Load the SPSS data file
2. Calculate knowledge and practice scores
3. Perform statistical analyses
4. Generate visualizations
5. Create a comprehensive report

All outputs are saved to `output/analysis_YYYYMMDD_HHMMSS/`

### What You Get

The analysis generates a timestamped output folder containing:

**Data Files:**
- `scored_dataset.csv` - Original data + calculated scores (knowledge_score, practice_score, per_capita_income)
- `maternal_education_summary.csv` - Statistics by maternal education level
- `correlation_matrix.csv` - Correlations between variables
- `demographic_*.csv` - Demographic summaries

**Visualizations (300 DPI PNG):**
- `scores_by_maternal_education.png` - Bar chart comparing scores across education levels
- `score_distributions.png` - Histograms of score distributions
- `score_boxplots.png` - Box plots by education group
- `scatter_matrix.png` - Scatter plots showing variable relationships

**Reports:**
- `analysis_report.txt` - Complete analysis report with all findings
- `analysis_report.md` - Same report in Markdown format
- `data_quality_summary.txt` - Data quality assessment
- `analysis.log` - Detailed execution log

## Understanding the Results

### Scored Dataset

The `scored_dataset.csv` contains:
- **All original SPSS data** (37 columns from the .sav file)
- **Calculated fields:**
  - `total_family_members` - Sum of male and female family members
  - `per_capita_income` - Monthly income divided by family members
  - `knowledge_score` - Score from 0-9 based on Section III questions
  - `practice_score` - Score from 0-7 based on Section IV questions
  - `total_score` - Sum of knowledge and practice scores

### Analysis Report

The `analysis_report.txt` includes:

1. **Demographic Summary** - Age, education, income distributions
2. **Knowledge Scores** - Mean, median, distribution (0-9 scale)
3. **Practice Scores** - Mean, median, distribution (0-7 scale)
4. **Maternal Education Impact** - Scores by education level with statistical tests
5. **Correlation Analysis** - Relationships between variables

### Key Statistics

From the latest analysis (160 records):
- **Knowledge Score**: Mean = 4.36, Range = 0-8
- **Practice Score**: Mean = 4.26, Range = 0-7
- **Maternal Education Impact**: 
  - Knowledge scores: Not significant (p = 0.26)
  - Practice scores: Significant (p = 0.04)

## Data Requirements

Your SPSS file should contain:

**Demographics:**
- Age, maternal/paternal education and occupation
- Income per month, number of family members

**Knowledge Questions (Section III):**
- Q3_1 through Q3_9 (9 questions)

**Practice Questions (Section IV):**
- Q4_1 through Q4_7 (7 questions)

## Scoring System

- **Knowledge Score (0-9)**: Based on Section III responses
- **Practice Score (0-7)**: Based on Section IV responses
- **Missing responses**: Assigned score of 0
- **Per Capita Income**: Income / Family Members (rounded to 2 decimals)

## Statistical Methods

- Descriptive statistics (mean, median, std dev)
- ANOVA for group comparisons
- Pearson correlation for continuous variables
- Significance level: α = 0.05

## Troubleshooting

**File not found:**
```bash
# Use quotes for filenames with spaces
python analyze.py "menstrual hygiene spss.sav fatima and ayesha (1).sav"
```

**SPSS file reading errors:**
- Ensure file is valid .sav format
- Check pyreadstat is installed: `pip install --upgrade pyreadstat`

**Missing visualizations:**
- Check `analysis.log` for errors
- Ensure matplotlib is installed: `pip install --upgrade matplotlib`

**Data quality issues:**
- Review `data_quality_summary.txt` in output folder
- Check for missing values in key variables

## Project Structure

```
.
├── src/                    # Source code modules
├── tests/                  # Test suite
├── output/                 # Analysis outputs (generated)
├── analyze.py              # Main script
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run integration tests
python -m pytest tests/integration/
```

## Contact

For questions or issues:
- Dr. Naureen Omar
- Dr. Ayesha Javed
- Dr. Fatima Sohail

## Acknowledgments

Developed for MBBS student research on menstrual hygiene awareness among adolescent girls in sub-urban Lahore, Pakistan.
