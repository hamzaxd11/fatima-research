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


def _compute_eta_squared(groups: List[np.ndarray]) -> float:
    try:
        all_values = np.concatenate(groups)
        if all_values.size == 0:
            return np.nan
        overall_mean = np.mean(all_values)
        ss_between = 0.0
        for group in groups:
            if len(group) == 0:
                continue
            ss_between += len(group) * (np.mean(group) - overall_mean) ** 2
        ss_total = np.sum((all_values - overall_mean) ** 2)
        return float(ss_between / ss_total) if ss_total > 0 else np.nan
    except Exception:
        return np.nan


def _compute_epsilon_squared(h_stat: float, n: int, k: int) -> float:
    try:
        if n <= 1:
            return np.nan
        return float(h_stat / (n - 1))
    except Exception:
        return np.nan


_CONTINUOUS_VAR_MAPPINGS = {
    'age': ['age', 'Age'],
    'income_per_month': ['income_per_month', 'Income_per_month', 'IncomePerMonth'],
    'total_family_members': ['total_family_members', 'Total_family_members', 'TotalFamilyMembers'],
    'per_capita_income': ['per_capita_income', 'Per_capita_income', 'PerCapitaIncome'],
    'knowledge_score': ['knowledge_score'],
    'practice_score': ['practice_score'],
    'total_score': ['total_score']
}


_EDUCATION_LABELS = {
    1: 'Illiterate',
    2: 'Primary',
    3: 'Middle',
    4: 'Secondary',
    5: 'Intermediate and above'
}


def _map_education_label(value: Any) -> Any:
    try:
        if pd.isna(value):
            return value
        int_value = int(float(value))
        return _EDUCATION_LABELS.get(int_value, value)
    except Exception:
        return value


def _build_correlation_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    available_cols = {}
    for var_name, possible_names in _CONTINUOUS_VAR_MAPPINGS.items():
        for name in possible_names:
            if name in df.columns:
                available_cols[var_name] = name
                break

    if not available_cols:
        return pd.DataFrame()

    correlation_df = pd.DataFrame()
    for var_name, col_name in available_cols.items():
        correlation_df[var_name] = pd.to_numeric(df[col_name], errors='coerce')

    correlation_df = correlation_df.dropna()
    return correlation_df


def perform_sensitivity_analyses(df: pd.DataFrame) -> pd.DataFrame:
    """Run and tabulate the manuscript's sensitivity and robustness checks."""
    maternal_col = next(
        (
            col
            for col in df.columns
            if ('mother' in col.lower() or 'maternal' in col.lower())
            and 'education' in col.lower()
        ),
        None,
    )
    age_col = next((name for name in ('Age', 'age') if name in df.columns), None)
    income_col = next(
        (name for name in ('IncomePerMonth', 'income_per_month') if name in df.columns),
        None,
    )
    rows = []

    if maternal_col:
        primary_tests = []
        for outcome in ('knowledge_score', 'practice_score'):
            analyzed = df[[maternal_col, outcome]].dropna()
            groups = [group[outcome].values for _, group in analyzed.groupby(maternal_col)]
            if len(groups) < 2 or analyzed[outcome].nunique() < 2:
                continue
            statistic, p_value = stats.kruskal(*groups)
            primary_tests.append((outcome, statistic, p_value, len(analyzed)))

        order = sorted(range(len(primary_tests)), key=lambda index: primary_tests[index][2])
        adjusted = [np.nan] * len(primary_tests)
        running = 0.0
        for rank, index in enumerate(order):
            candidate = min((len(primary_tests) - rank) * primary_tests[index][2], 1.0)
            running = max(running, candidate)
            adjusted[index] = running
        for index, (outcome, statistic, _, analyzed_n) in enumerate(primary_tests):
            rows.append(
                {
                    'analysis': 'Holm-adjusted primary outcome',
                    'variables': outcome,
                    'statistic': statistic,
                    'p_value': adjusted[index],
                    'effect_size': np.nan,
                    'n': analyzed_n,
                }
            )

        practice_items = [
            'WhichTypeOfAbsorbentDoYouUseDuringMensturation',
            'UsePaperToDisposeThePadByWrapping',
            'WhereDisposeTheUsedPads',
            'HowManyTimeUsualyChangeTheClothandSanitaryPad',
            'HowManyTimesTakeBathDuringMensturation',
            'CleanYourExternalGenitaliaThroughlyWaterDuringMensturation',
            'AfterThatWashHandsWithSoapAndWater',
        ]
        if all(column in df.columns for column in practice_items):
            complete = df.dropna(subset=[maternal_col, *practice_items])
            groups = [
                group['practice_score'].values
                for _, group in complete.groupby(maternal_col)
            ]
            if len(groups) >= 2 and complete['practice_score'].nunique() >= 2:
                statistic, p_value = stats.kruskal(*groups)
            else:
                statistic, p_value = np.nan, np.nan
            rows.append(
                {
                    'analysis': 'Complete-case practice responses',
                    'variables': 'practice_score',
                    'statistic': statistic,
                    'p_value': p_value,
                    'effect_size': _compute_epsilon_squared(
                        statistic, len(complete), len(groups)
                    ),
                    'n': len(complete),
                }
            )

        reduced = df[df[maternal_col] != 5]
        for outcome in ('knowledge_score', 'practice_score'):
            analyzed = reduced[[maternal_col, outcome]].dropna()
            groups = [group[outcome].values for _, group in analyzed.groupby(maternal_col)]
            if len(groups) >= 2 and analyzed[outcome].nunique() >= 2:
                statistic, p_value = stats.kruskal(*groups)
                rows.append(
                    {
                        'analysis': f'Kruskal-Wallis excluding {maternal_col}=5',
                        'variables': outcome,
                        'statistic': statistic,
                        'p_value': p_value,
                        'effect_size': _compute_epsilon_squared(statistic, len(analyzed), len(groups)),
                        'n': len(analyzed),
                    }
                )

        process_col = 'WhatDoYouThinkAboutThePrecessofMensturation'
        if process_col in df.columns:
            archived = df['knowledge_score'].copy()
            responses = pd.to_numeric(df[process_col], errors='coerce')
            archived = archived - (responses == 1).astype(int) + (responses == 2).astype(int)
            archived_frame = pd.DataFrame({maternal_col: df[maternal_col], 'score': archived}).dropna()
            groups = [group['score'].values for _, group in archived_frame.groupby(maternal_col)]
            statistic, p_value = stats.kruskal(*groups)
            rows.append(
                {
                    'analysis': 'Archived pathological-response scoring key',
                    'variables': 'knowledge_score',
                    'statistic': statistic,
                    'p_value': p_value,
                    'effect_size': _compute_epsilon_squared(
                        statistic, len(archived_frame), len(groups)
                    ),
                    'n': len(archived_frame),
                }
            )

        for outcome in ('knowledge_score', 'practice_score'):
            pair = df[[maternal_col, outcome]].dropna()
            statistic, p_value = stats.spearmanr(pair[maternal_col], pair[outcome])
            rows.append(
                {
                    'analysis': 'Spearman ordinal trend',
                    'variables': f'{maternal_col} vs {outcome}',
                    'statistic': statistic,
                    'p_value': p_value,
                    'effect_size': np.nan,
                    'n': len(pair),
                }
            )

        if age_col:
            analyzed = df[[maternal_col, age_col]].dropna()
            groups = [group[age_col].values for _, group in analyzed.groupby(maternal_col)]
            if len(groups) < 2 or analyzed[age_col].nunique() < 2:
                statistic, p_value = np.nan, np.nan
            else:
                statistic, p_value = stats.kruskal(*groups)
            rows.append(
                {
                    'analysis': 'Kruskal-Wallis confounder check',
                    'variables': f'{age_col} by {maternal_col}',
                    'statistic': statistic,
                    'p_value': p_value,
                    'effect_size': _compute_epsilon_squared(statistic, len(analyzed), len(groups)),
                    'n': len(analyzed),
                }
            )

    spearman_pairs = [
        (age_col, 'knowledge_score'),
        (age_col, 'practice_score'),
        ('knowledge_score', 'practice_score'),
        (income_col, 'knowledge_score'),
        (income_col, 'practice_score'),
    ]
    for left, right in spearman_pairs:
        if not left or left not in df.columns or right not in df.columns:
            continue
        pair = df[[left, right]].dropna()
        statistic, p_value = stats.spearmanr(pair[left], pair[right])
        rows.append(
            {
                'analysis': 'Spearman correlation',
                'variables': f'{left} vs {right}',
                'statistic': statistic,
                'p_value': p_value,
                'effect_size': np.nan,
                'n': len(pair),
            }
        )

    return pd.DataFrame(rows)

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
            'test_type': 'None',
            'test_type_by_outcome': {},
            'assumption_checks': {}
        }
    
    # Check if required score columns exist
    if 'knowledge_score' not in df.columns or 'practice_score' not in df.columns:
        warnings.warn("Knowledge or practice score columns not found in dataset")
        return {
            'summary_table': pd.DataFrame(),
            'anova_knowledge': {'f_statistic': np.nan, 'p_value': np.nan},
            'anova_practice': {'f_statistic': np.nan, 'p_value': np.nan},
            'test_type': 'None',
            'test_type_by_outcome': {},
            'assumption_checks': {}
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
            'test_type': 'None',
            'test_type_by_outcome': {},
            'assumption_checks': {}
        }
    
    # Group by maternal education level
    grouped = analysis_df.groupby(maternal_ed_col)
    
    # Calculate summary statistics
    summary_data = []
    for education_level, group in grouped:
        summary_data.append({
            'education_level': education_level,
            'education_label': _map_education_label(education_level),
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
    
    # Check assumptions for ANOVA
    # 1. Normality (Shapiro-Wilk test)
    #    If p < 0.05, data is NOT normal.
    # 2. Homogeneity of Variance (Levene's test)
    #    If p < 0.05, variances are NOT equal.
    # 3. Minimum group size (n >= 3) for reliable assumption testing

    def check_assumptions(groups: List[np.ndarray], label: str) -> Dict[str, Any]:
        normality_pvalues = []
        tested_groups = 0
        small_groups = any(len(g) < 2 for g in groups)
        insufficient_normality = any(len(g) < 3 for g in groups)

        try:
            for g in groups:
                if len(g) >= 3:
                    if np.all(g == g[0]):
                        normality_pvalues.append(0.0)
                        tested_groups += 1
                    else:
                        _, p_norm = stats.shapiro(g)
                        normality_pvalues.append(float(p_norm))
                        tested_groups += 1
        except Exception as e:
            warnings.warn(f"Normality check failed for {label} scores: {str(e)}")

        normality_ok = all(p >= 0.05 for p in normality_pvalues) if normality_pvalues else False

        p_var = np.nan
        variance_ok = False
        try:
            if len(groups) >= 2 and all(len(g) >= 2 for g in groups):
                _, p_var = stats.levene(*groups)
                variance_ok = p_var >= 0.05
        except Exception as e:
            warnings.warn(f"Variance check failed for {label} scores: {str(e)}")

        use_parametric = normality_ok and variance_ok and not small_groups and not insufficient_normality

        return {
            'normality_min_p': min(normality_pvalues) if normality_pvalues else np.nan,
            'normality_tested_groups': tested_groups,
            'variance_p': float(p_var) if not np.isnan(p_var) else np.nan,
            'small_groups': small_groups,
            'insufficient_normality': insufficient_normality,
            'use_parametric': use_parametric
        }

    assumption_checks = {
        'knowledge': check_assumptions(groups_knowledge, 'knowledge'),
        'practice': check_assumptions(groups_practice, 'practice')
    }

    use_parametric_knowledge = assumption_checks['knowledge']['use_parametric']
    use_parametric_practice = assumption_checks['practice']['use_parametric']

    test_type_by_outcome = {
        'knowledge': 'ANOVA' if use_parametric_knowledge else 'Kruskal-Wallis',
        'practice': 'ANOVA' if use_parametric_practice else 'Kruskal-Wallis'
    }

    # Determine overall test type
    if test_type_by_outcome['knowledge'] == test_type_by_outcome['practice']:
        test_type = f"{test_type_by_outcome['knowledge']} (Robust)" if 'Kruskal' in test_type_by_outcome['knowledge'] else 'ANOVA'
    else:
        test_type = 'Mixed (ANOVA/Kruskal)'

    # Perform statistical tests for knowledge scores
    try:
        if use_parametric_knowledge:
            f_stat_k, p_value_k = stats.f_oneway(*groups_knowledge)
            anova_knowledge = {
                'f_statistic': float(f_stat_k),
                'p_value': float(p_value_k),
                'effect_size': _compute_eta_squared(groups_knowledge),
                'effect_size_type': 'eta_squared'
            }
        else:
            h_stat_k, p_value_k = stats.kruskal(*groups_knowledge)
            anova_knowledge = {
                'f_statistic': float(h_stat_k),
                'p_value': float(p_value_k),
                'effect_size': _compute_epsilon_squared(float(h_stat_k), len(analysis_df), len(groups_knowledge)),
                'effect_size_type': 'epsilon_squared'
            }
            if test_type == 'ANOVA':
                test_type = 'Mixed (ANOVA/Kruskal)'
            
    except Exception as e:
        warnings.warn(f"Statistical test failed for knowledge scores: {str(e)}")
        anova_knowledge = {'f_statistic': np.nan, 'p_value': np.nan}
    
    # Perform statistical tests for practice scores
    try:
        if use_parametric_practice:
            f_stat_p, p_value_p = stats.f_oneway(*groups_practice)
            anova_practice = {
                'f_statistic': float(f_stat_p),
                'p_value': float(p_value_p),
                'effect_size': _compute_eta_squared(groups_practice),
                'effect_size_type': 'eta_squared'
            }
        else:
            h_stat_p, p_value_p = stats.kruskal(*groups_practice)
            anova_practice = {
                'f_statistic': float(h_stat_p),
                'p_value': float(p_value_p),
                'effect_size': _compute_epsilon_squared(float(h_stat_p), len(analysis_df), len(groups_practice)),
                'effect_size_type': 'epsilon_squared'
            }
            if test_type == 'ANOVA':
                test_type = 'Mixed (ANOVA/Kruskal)'
            
    except Exception as e:
        warnings.warn(f"Statistical test failed for practice scores: {str(e)}")
        anova_practice = {'f_statistic': np.nan, 'p_value': np.nan}
    
    return {
        'summary_table': summary_table,
        'anova_knowledge': anova_knowledge,
        'anova_practice': anova_practice,
        'test_type': test_type,
        'test_type_by_outcome': test_type_by_outcome,
        'assumption_checks': assumption_checks,
        'significant_unadjusted': {
            'knowledge': bool(anova_knowledge['p_value'] < 0.05),
            'practice': bool(anova_practice['p_value'] < 0.05),
        },
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
            if var_name in {'maternal_education', 'paternal_education'}:
                freq_table[f'{var_name}_label'] = freq_table[var_name].apply(_map_education_label)
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
    correlation_df = _build_correlation_dataframe(df)
    if correlation_df.empty:
        warnings.warn("No continuous variables found for correlation analysis")
        return pd.DataFrame()
    
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


def perform_correlation_pvalues(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate p-values for Pearson correlations between continuous variables.
    """
    correlation_df = _build_correlation_dataframe(df)
    if correlation_df.empty or len(correlation_df) < 2:
        warnings.warn("Insufficient data for correlation p-values")
        return pd.DataFrame()

    cols = correlation_df.columns
    p_matrix = pd.DataFrame(np.nan, index=cols, columns=cols)

    try:
        for i, col_i in enumerate(cols):
            for j, col_j in enumerate(cols):
                if i == j:
                    p_matrix.loc[col_i, col_j] = 0.0
                elif i < j:
                    _, p_val = stats.pearsonr(correlation_df[col_i], correlation_df[col_j])
                    p_matrix.loc[col_i, col_j] = p_val
                    p_matrix.loc[col_j, col_i] = p_val
        return p_matrix
    except Exception as e:
        warnings.warn(f"Correlation p-value analysis failed: {str(e)}")
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
