"""
Statistical Analysis Module

This module provides functions for performing statistical analyses on the
menstrual hygiene survey data, including maternal education impact analysis,
demographic summaries, and correlation analysis.
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Any, Optional
import warnings


def analyze_maternal_education_impact(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze the relationship between maternal education and hygiene awareness scores.
    
    Groups data by maternal education level and calculates:
    - Mean knowledge and practice scores for each education level
    - Standard deviations for each group
    - Statistical tests (ANOVA or Kruskal-Wallis) to determine significance
    - P-values and confidence intervals
    
    Args:
        df: DataFrame with 'knowledge_score', 'practice_score', and maternal education column
        
    Returns:
        Dictionary containing:
        - summary_table: DataFrame with education level, n, means, stds
        - anova_knowledge: Dict with f_statistic and p_value for knowledge scores
        - anova_practice: Dict with f_statistic and p_value for practice scores
        - test_type: String indicating which test was used (ANOVA or Kruskal-Wallis)
        
    Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6
    """
    # Find maternal education column (try different name variations)
    maternal_ed_col = None
    for col in df.columns:
        col_lower = col.lower()
        if 'mother' in col_lower and 'education' in col_lower:
            maternal_ed_col = col
            break
        elif 'maternal' in col_lower and 'education' in col_lower:
            maternal_ed_col = col
            break
    
    if maternal_ed_col is None:
        warnings.warn("Maternal education column not found in dataset")
        return {
            'summary_table': pd.DataFrame(),
            'anova_knowledge': {'f_statistic': np.nan, 'p_value': np.nan},
            'anova_practice': {'f_statistic': np.nan, 'p_value': np.nan},
            'test_type': 'None'
        }
    
    # Check if required score columns exist
    if 'knowledge_score' not in df.columns or 'practice_score' not in df.columns:
        warnings.warn("Knowledge or practice score columns not found in dataset")
        return {
            'summary_table': pd.DataFrame(),
            'anova_knowledge': {'f_statistic': np.nan, 'p_value': np.nan},
            'anova_practice': {'f_statistic': np.nan, 'p_value': np.nan},
            'test_type': 'None'
        }
    
    # Remove rows with missing maternal education or scores
    analysis_df = df[[maternal_ed_col, 'knowledge_score', 'practice_score']].copy()
    analysis_df = analysis_df.dropna()
    
    if len(analysis_df) == 0:
        warnings.warn("No valid records for maternal education analysis")
        return {
            'summary_table': pd.DataFrame(),
            'anova_knowledge': {'f_statistic': np.nan, 'p_value': np.nan},
            'anova_practice': {'f_statistic': np.nan, 'p_value': np.nan},
            'test_type': 'None'
        }
    
    # Group by maternal education level
    grouped = analysis_df.groupby(maternal_ed_col)
    
    # Calculate summary statistics
    summary_data = []
    for education_level, group in grouped:
        summary_data.append({
            'education_level': education_level,
            'n': len(group),
            'mean_knowledge': group['knowledge_score'].mean(),
            'std_knowledge': group['knowledge_score'].std(ddof=1),
            'mean_practice': group['practice_score'].mean(),
            'std_practice': group['practice_score'].std(ddof=1)
        })
    
    summary_table = pd.DataFrame(summary_data)
    
    # Prepare data for statistical tests
    # Each group becomes a separate array for the statistical test
    groups_knowledge = [group['knowledge_score'].values for _, group in grouped]
    groups_practice = [group['practice_score'].values for _, group in grouped]
    
    # Determine which statistical test to use:
    # - ANOVA (Analysis of Variance): Parametric test for comparing means across groups
    #   Assumptions: Normal distribution, equal variances, independent samples
    #   More powerful when assumptions are met
    # - Kruskal-Wallis: Non-parametric alternative to ANOVA
    #   Used when: Small sample sizes, non-normal distributions, unequal variances
    #   More robust but less powerful than ANOVA
    # 
    # We default to ANOVA and fall back to Kruskal-Wallis if ANOVA fails
    test_type = 'ANOVA'
    
    # Check if we have enough groups
    if len(groups_knowledge) < 2:
        warnings.warn("Insufficient groups for statistical testing (need at least 2)")
        return {
            'summary_table': summary_table,
            'anova_knowledge': {'f_statistic': np.nan, 'p_value': np.nan},
            'anova_practice': {'f_statistic': np.nan, 'p_value': np.nan},
            'test_type': 'None'
        }
    
    # Perform statistical tests for knowledge scores
    try:
        # ANOVA (Analysis of Variance) - One-way ANOVA
        # Null hypothesis: All group means are equal
        # Alternative hypothesis: At least one group mean differs
        # Returns: F-statistic and p-value
        # F-statistic: Ratio of between-group variance to within-group variance
        # p-value: Probability of observing this F-statistic if null hypothesis is true
        # Interpretation: p < 0.05 suggests significant differences between groups
        f_stat_k, p_value_k = stats.f_oneway(*groups_knowledge)
        anova_knowledge = {'f_statistic': float(f_stat_k), 'p_value': float(p_value_k)}
    except Exception as e:
        warnings.warn(f"ANOVA failed for knowledge scores, using Kruskal-Wallis: {str(e)}")
        try:
            # Kruskal-Wallis H-test - Non-parametric alternative to ANOVA
            # Tests whether samples originate from the same distribution
            # Null hypothesis: All groups have the same median
            # Returns: H-statistic and p-value
            # H-statistic: Measures how much group ranks differ from expected
            # More robust to outliers and non-normal distributions than ANOVA
            h_stat_k, p_value_k = stats.kruskal(*groups_knowledge)
            anova_knowledge = {'f_statistic': float(h_stat_k), 'p_value': float(p_value_k)}
            test_type = 'Kruskal-Wallis'
        except Exception as e2:
            warnings.warn(f"Statistical test failed for knowledge scores: {str(e2)}")
            anova_knowledge = {'f_statistic': np.nan, 'p_value': np.nan}
            test_type = 'Failed'
    
    # Perform statistical tests for practice scores
    # Use the same test type as determined for knowledge scores for consistency
    try:
        if test_type == 'ANOVA':
            # One-way ANOVA for practice scores
            f_stat_p, p_value_p = stats.f_oneway(*groups_practice)
            anova_practice = {'f_statistic': float(f_stat_p), 'p_value': float(p_value_p)}
        else:
            # Kruskal-Wallis test for practice scores
            h_stat_p, p_value_p = stats.kruskal(*groups_practice)
            anova_practice = {'f_statistic': float(h_stat_p), 'p_value': float(p_value_p)}
    except Exception as e:
        warnings.warn(f"Statistical test failed for practice scores: {str(e)}")
        anova_practice = {'f_statistic': np.nan, 'p_value': np.nan}
    
    # Add significance indicators to summary table
    # Using standard alpha level of 0.05 (5% significance level)
    # If p < 0.05: Reject null hypothesis, differences are statistically significant
    # If p >= 0.05: Fail to reject null hypothesis, differences may be due to chance
    alpha = 0.05
    summary_table['knowledge_significant'] = anova_knowledge['p_value'] < alpha if not np.isnan(anova_knowledge['p_value']) else False
    summary_table['practice_significant'] = anova_practice['p_value'] < alpha if not np.isnan(anova_practice['p_value']) else False
    
    return {
        'summary_table': summary_table,
        'anova_knowledge': anova_knowledge,
        'anova_practice': anova_practice,
        'test_type': test_type
    }


def calculate_demographic_summaries(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Calculate comprehensive demographic summary statistics.
    
    Generates:
    - Frequency distributions for categorical variables
    - Descriptive statistics for continuous variables
    - Percentages and proportions for all frequency distributions
    
    Args:
        df: DataFrame with demographic variables
        
    Returns:
        Dictionary of DataFrames containing:
        - age_distribution: Frequency table for age
        - maternal_education_freq: Frequency table for maternal education
        - paternal_education_freq: Frequency table for paternal education
        - maternal_occupation_freq: Frequency table for maternal occupation
        - paternal_occupation_freq: Frequency table for paternal occupation
        - continuous_stats: Descriptive statistics for continuous variables
        
    Requirements: 6.1, 6.2, 6.3, 6.4
    """
    summaries = {}
    
    # Define categorical and continuous variables
    categorical_mappings = {
        'age': ['age', 'Age'],
        'maternal_education': ['mother_education', 'Mother_education', 'MotherEducation', 'maternal_education'],
        'paternal_education': ['father_education', 'Father_education', 'FatherEducation', 'paternal_education'],
        'maternal_occupation': ['mother_occupation', 'Mother_occupation', 'MotherOccupation', 'maternal_occupation'],
        'paternal_occupation': ['father_occupation', 'Father_occupation', 'FatherOccupation', 'paternal_occupation']
    }
    
    continuous_mappings = {
        'age': ['age', 'Age'],
        'income': ['income_per_month', 'Income_per_month', 'IncomePerMonth', 'income'],
        'family_size': ['total_family_members', 'Total_family_members', 'TotalFamilyMembers'],
        'per_capita_income': ['per_capita_income', 'Per_capita_income', 'PerCapitaIncome']
    }
    
    # Helper function to find column
    def find_column(df: pd.DataFrame, possible_names: List[str]) -> Optional[str]:
        for name in possible_names:
            if name in df.columns:
                return name
        return None
    
    # Calculate frequency distributions for categorical variables
    for var_name, possible_cols in categorical_mappings.items():
        col = find_column(df, possible_cols)
        if col:
            freq_table = df[col].value_counts().reset_index()
            freq_table.columns = [var_name, 'count']
            freq_table['percentage'] = (freq_table['count'] / freq_table['count'].sum() * 100).round(2)
            freq_table['proportion'] = (freq_table['count'] / freq_table['count'].sum()).round(4)
            freq_table = freq_table.sort_values('count', ascending=False)
            summaries[f'{var_name}_freq'] = freq_table
    
    # Calculate descriptive statistics for continuous variables
    continuous_stats = []
    for var_name, possible_cols in continuous_mappings.items():
        col = find_column(df, possible_cols)
        if col:
            data = pd.to_numeric(df[col], errors='coerce').dropna()
            if len(data) > 0:
                continuous_stats.append({
                    'variable': var_name,
                    'count': len(data),
                    'mean': data.mean(),
                    'median': data.median(),
                    'std': data.std(ddof=1),
                    'min': data.min(),
                    'max': data.max(),
                    'q25': data.quantile(0.25),
                    'q75': data.quantile(0.75)
                })
    
    if continuous_stats:
        summaries['continuous_stats'] = pd.DataFrame(continuous_stats)
    
    return summaries


def perform_correlation_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate correlations between continuous variables.
    
    Computes Pearson correlation coefficients between:
    - Age, income, family size, per capita income
    - Knowledge score, practice score, total score
    
    Args:
        df: DataFrame with continuous variables
        
    Returns:
        DataFrame containing correlation matrix
        
    Requirements: 6.4
    """
    # Define continuous variables to correlate
    continuous_vars = []
    var_mappings = {
        'age': ['age', 'Age'],
        'income_per_month': ['income_per_month', 'Income_per_month', 'IncomePerMonth'],
        'total_family_members': ['total_family_members', 'Total_family_members', 'TotalFamilyMembers'],
        'per_capita_income': ['per_capita_income', 'Per_capita_income', 'PerCapitaIncome'],
        'knowledge_score': ['knowledge_score'],
        'practice_score': ['practice_score'],
        'total_score': ['total_score']
    }
    
    # Find which columns exist
    available_cols = {}
    for var_name, possible_names in var_mappings.items():
        for name in possible_names:
            if name in df.columns:
                available_cols[var_name] = name
                break
    
    if not available_cols:
        warnings.warn("No continuous variables found for correlation analysis")
        return pd.DataFrame()
    
    # Extract data for correlation
    correlation_df = pd.DataFrame()
    for var_name, col_name in available_cols.items():
        correlation_df[var_name] = pd.to_numeric(df[col_name], errors='coerce')
    
    # Remove rows with any missing values
    correlation_df = correlation_df.dropna()
    
    if len(correlation_df) < 2:
        warnings.warn("Insufficient data for correlation analysis (need at least 2 complete records)")
        return pd.DataFrame()
    
    # Calculate correlation matrix
    # Pearson correlation coefficient measures linear relationship between variables
    # Range: -1 (perfect negative correlation) to +1 (perfect positive correlation)
    # 0 indicates no linear relationship
    # 
    # Interpretation guidelines:
    # |r| < 0.3: Weak correlation
    # 0.3 ≤ |r| < 0.7: Moderate correlation
    # |r| ≥ 0.7: Strong correlation
    #
    # Note: Correlation does not imply causation
    # Significant correlation only indicates variables tend to vary together
    try:
        corr_matrix = correlation_df.corr(method='pearson')
        return corr_matrix
    except Exception as e:
        warnings.warn(f"Correlation analysis failed: {str(e)}")
        return pd.DataFrame()


def generate_cross_tabulation(
    df: pd.DataFrame,
    var1_name: str,
    var2_name: str,
    var1_possible_cols: Optional[List[str]] = None,
    var2_possible_cols: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Generate cross-tabulation table for two categorical variables.
    
    Args:
        df: DataFrame with categorical variables
        var1_name: Name for first variable (for output)
        var2_name: Name for second variable (for output)
        var1_possible_cols: List of possible column names for first variable
        var2_possible_cols: List of possible column names for second variable
        
    Returns:
        DataFrame containing cross-tabulation with row/column totals
        
    Requirements: 6.3
    """
    # Helper function to find column
    def find_column(df: pd.DataFrame, possible_names: List[str]) -> Optional[str]:
        if possible_names is None:
            return None
        for name in possible_names:
            if name in df.columns:
                return name
        return None
    
    col1 = find_column(df, var1_possible_cols) if var1_possible_cols else None
    col2 = find_column(df, var2_possible_cols) if var2_possible_cols else None
    
    if col1 is None or col2 is None:
        warnings.warn(f"Could not find columns for cross-tabulation: {var1_name} x {var2_name}")
        return pd.DataFrame()
    
    # Create cross-tabulation
    try:
        crosstab = pd.crosstab(
            df[col1],
            df[col2],
            margins=True,
            margins_name='Total'
        )
        crosstab.index.name = var1_name
        crosstab.columns.name = var2_name
        return crosstab
    except Exception as e:
        warnings.warn(f"Cross-tabulation failed for {var1_name} x {var2_name}: {str(e)}")
        return pd.DataFrame()
