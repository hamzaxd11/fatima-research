"""
Report Generation Module

This module generates comprehensive analysis reports summarizing all findings
from the menstrual hygiene survey data analysis.

Requirements: 9.1, 9.2, 9.3, 9.4, 9.5
"""

import pandas as pd
from datetime import datetime
from typing import Dict, Any, Optional
import os


def _format_maternal_education_label(value: Any) -> str:
    mapping = {
        1: 'Illiterate',
        2: 'Primary',
        3: 'Middle',
        4: 'Secondary',
        5: 'Intermediate and above'
    }
    try:
        if pd.isna(value):
            return str(value)
        int_value = int(float(value))
        if int_value in mapping:
            return f"{int_value} ({mapping[int_value]})"
    except Exception:
        pass
    return str(value)


def _format_mean_sd(mean_value: float, sd_value: float) -> str:
    if pd.isna(sd_value):
        return f"{mean_value:.2f} ± N/A"
    return f"{mean_value:.2f} ± {sd_value:.2f}"


def _format_p_value(value: Any) -> str:
    try:
        if value is None or pd.isna(value):
            return "N/A"
        return f"{float(value):.4f}"
    except Exception:
        return "N/A"

def generate_analysis_report(
    analysis_results: Dict[str, Any],
    scored_dataset: pd.DataFrame,
    output_folder: str,
    spss_file_path: Optional[str] = None
) -> tuple[str, str]:
    """
    Generate comprehensive analysis report in both TXT and Markdown formats.
    
    Creates a detailed report with sections for:
    - Demographics summary
    - Knowledge scores analysis
    - Practice scores analysis
    - Maternal education impact analysis
    - Statistical test results with interpretations
    - References to all generated tables and charts
    
    Args:
        analysis_results: Dictionary containing all analysis outputs from statistical_analysis module
        scored_dataset: DataFrame with all calculated scores
        output_folder: Directory where report files will be saved
        spss_file_path: Optional path to original SPSS file for documentation
        
    Returns:
        Tuple of (txt_report_path, md_report_path)
        
    Requirements: 9.1, 9.2, 9.3, 9.4, 9.5
    """
    # Generate report content
    report_lines = []
    
    # Header section
    data_loader_metadata = analysis_results.get('data_loader_metadata')
    report_lines.extend(_generate_header_section(spss_file_path, scored_dataset, data_loader_metadata))
    
    # Demographics section
    report_lines.extend(_generate_demographics_section(analysis_results, scored_dataset))
    
    # Data quality section
    report_lines.extend(_generate_data_quality_section(analysis_results))

    # Knowledge scores section
    report_lines.extend(_generate_knowledge_scores_section(analysis_results, scored_dataset))
    
    # Practice scores section
    report_lines.extend(_generate_practice_scores_section(analysis_results, scored_dataset))
    
    # Maternal education analysis section
    report_lines.extend(_generate_maternal_education_section(analysis_results))
    
    # Correlation analysis section
    report_lines.extend(_generate_correlation_section(analysis_results))
    
    # Generated files reference section
    report_lines.extend(_generate_files_reference_section(output_folder))
    
    # Footer section
    report_lines.extend(_generate_footer_section())
    
    # Join all lines
    report_content = '\n'.join(report_lines)
    
    # Save as TXT
    txt_path = os.path.join(output_folder, 'analysis_report.txt')
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    # Save as Markdown (same content, markdown is plain text compatible)
    md_path = os.path.join(output_folder, 'analysis_report.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    return txt_path, md_path


def _generate_header_section(
    spss_file_path: Optional[str],
    df: pd.DataFrame,
    metadata: Optional[Dict[str, Any]] = None
) -> list:
    """Generate report header with metadata."""
    lines = [
        "=" * 80,
        "MENSTRUAL HYGIENE AWARENESS ANALYSIS REPORT",
        "=" * 80,
        "",
        f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ""
    ]
    
    if spss_file_path:
        lines.append(f"Source Data File: {spss_file_path}")
        lines.append("")
    
    if metadata and metadata.get('number_rows'):
        raw_rows = metadata.get('number_rows')
        filtered_rows = metadata.get('filtered_rows', 0)
        filter_column = metadata.get('filter_column')
        lines.append(f"Raw Records Loaded: {raw_rows}")
        if filtered_rows:
            lines.append(
                f"Records Excluded (missing {filter_column}): {filtered_rows}"
            )
        lines.append("")

    lines.extend([
        f"Total Records Analyzed: {len(df)}",
        "",
        "=" * 80,
        ""
    ])
    
    return lines


def _generate_demographics_section(analysis_results: Dict[str, Any], df: pd.DataFrame) -> list:
    """Generate demographics summary section."""
    lines = [
        "## 1. DEMOGRAPHIC SUMMARY",
        "",
        "This section provides an overview of the study population characteristics.",
        ""
    ]
    
    # Get demographic summaries if available
    demo_summaries = analysis_results.get('demographic_summaries', {})
    
    # Age distribution
    if 'age_freq' in demo_summaries:
        lines.extend([
            "### 1.1 Age Distribution",
            ""
        ])
        age_freq = demo_summaries['age_freq']
        for _, row in age_freq.iterrows():
            lines.append(f"  Age {row['age']}: {row['count']} ({row['percentage']:.1f}%)")
        lines.append("")
    
    # Maternal education distribution
    if 'maternal_education_freq' in demo_summaries:
        lines.extend([
            "### 1.2 Maternal Education Distribution",
            ""
        ])
        mat_ed_freq = demo_summaries['maternal_education_freq']
        for _, row in mat_ed_freq.iterrows():
            label = _format_maternal_education_label(row['maternal_education'])
            lines.append(f"  {label}: {row['count']} ({row['percentage']:.1f}%)")
        lines.append("")
    
    # Continuous variables statistics
    if 'continuous_stats' in demo_summaries:
        lines.extend([
            "### 1.3 Continuous Variables Summary",
            ""
        ])
        cont_stats = demo_summaries['continuous_stats']
        for _, row in cont_stats.iterrows():
            lines.extend([
                f"**{row['variable'].replace('_', ' ').title()}**",
                f"  Count: {int(row['count'])}",
                f"  Mean: {row['mean']:.2f}",
                f"  Median: {row['median']:.2f}",
                f"  Std Dev: {row['std']:.2f}",
                f"  Range: {row['min']:.2f} - {row['max']:.2f}",
                ""
            ])
    
    lines.append("")
    return lines


def _generate_data_quality_section(analysis_results: Dict[str, Any]) -> list:
    """Generate data quality summary section."""
    lines = [
        "## 2. DATA QUALITY SUMMARY",
        "",
        "This section summarizes missingness and data quality checks.",
        ""
    ]

    quality_report = analysis_results.get('data_quality_report', {})
    summary = quality_report.get('summary', {}) if isinstance(quality_report, dict) else {}

    if summary:
        lines.extend([
            f"  Total Rows: {summary.get('total_rows', 'N/A')}",
            f"  Total Columns: {summary.get('total_columns', 'N/A')}",
            f"  Missing Values: {summary.get('missing_value_count', 'N/A')}",
            f"  Invalid Values: {summary.get('invalid_value_count', 'N/A')}",
            f"  Data Quality: {summary.get('data_quality_percentage', 'N/A')}%"
        ])

        core_quality = summary.get('core_data_quality_percentage')
        if core_quality is not None:
            lines.append(f"  Core Data Quality: {core_quality}%")

        conditional_columns = summary.get('conditional_columns', [])
        if conditional_columns:
            lines.append("")
            lines.append("Conditional/Skip-Logic Columns (missingness expected):")
            for col in conditional_columns:
                lines.append(f"  - {col}")

        family_check = analysis_results.get('family_size_consistency', {})
        if family_check.get('status') == 'checked':
            lines.append("")
            lines.append("Family Size Consistency Check:")
            lines.append(
                f"  Checked Rows: {family_check.get('checked_rows', 0)}, "
                f"Mismatches: {family_check.get('mismatch_count', 0)}"
            )
            if family_check.get('mismatch_count', 0) > 0:
                lines.append(f"  Example Mismatch Rows: {family_check.get('mismatch_rows', [])}")

        lines.append("")
    else:
        lines.extend([
            "Data quality summary is unavailable.",
            ""
        ])

    lines.append("")
    return lines


def _generate_knowledge_scores_section(analysis_results: Dict[str, Any], df: pd.DataFrame) -> list:
    """Generate knowledge scores analysis section."""
    lines = [
        "## 3. KNOWLEDGE SCORES ANALYSIS",
        "",
        "Knowledge scores range from 0 to 9, based on responses to Section III questions",
        "about menstrual hygiene awareness.",
        ""
    ]
    
    if 'knowledge_score' in df.columns:
        knowledge_scores = df['knowledge_score'].dropna()
        
        if len(knowledge_scores) > 0:
            lines.extend([
                "### 3.1 Overall Knowledge Score Statistics",
                "",
                f"  Total Respondents: {len(knowledge_scores)}",
                f"  Mean Score: {knowledge_scores.mean():.2f}",
                f"  Median Score: {knowledge_scores.median():.2f}",
                f"  Standard Deviation: {knowledge_scores.std():.2f}",
                f"  Minimum Score: {knowledge_scores.min():.0f}",
                f"  Maximum Score: {knowledge_scores.max():.0f}",
                "",
                "### 3.2 Score Distribution",
                ""
            ])
            
            # Score frequency distribution
            score_counts = knowledge_scores.value_counts().sort_index()
            for score, count in score_counts.items():
                percentage = (count / len(knowledge_scores)) * 100
                lines.append(f"  Score {int(score)}: {count} respondents ({percentage:.1f}%)")
            
            lines.extend([
                "",
                f"**Visualization**: See 'score_distributions.png' for histogram",
                ""
            ])
    
    lines.append("")
    return lines


def _generate_practice_scores_section(analysis_results: Dict[str, Any], df: pd.DataFrame) -> list:
    """Generate practice scores analysis section."""
    lines = [
        "## 4. PRACTICE SCORES ANALYSIS",
        "",
        "Practice scores range from 0 to 7, based on responses to Section IV questions",
        "about actual menstrual hygiene practices.",
        ""
    ]
    
    if 'practice_score' in df.columns:
        practice_scores = df['practice_score'].dropna()
        
        if len(practice_scores) > 0:
            lines.extend([
                "### 4.1 Overall Practice Score Statistics",
                "",
                f"  Total Respondents: {len(practice_scores)}",
                f"  Mean Score: {practice_scores.mean():.2f}",
                f"  Median Score: {practice_scores.median():.2f}",
                f"  Standard Deviation: {practice_scores.std():.2f}",
                f"  Minimum Score: {practice_scores.min():.0f}",
                f"  Maximum Score: {practice_scores.max():.0f}",
                "",
                "### 4.2 Score Distribution",
                ""
            ])
            
            # Score frequency distribution
            score_counts = practice_scores.value_counts().sort_index()
            for score, count in score_counts.items():
                percentage = (count / len(practice_scores)) * 100
                lines.append(f"  Score {int(score)}: {count} respondents ({percentage:.1f}%)")
            
            lines.extend([
                "",
                f"**Visualization**: See 'score_distributions.png' for histogram",
                ""
            ])
    
    lines.append("")
    return lines


def _generate_maternal_education_section(analysis_results: Dict[str, Any]) -> list:
    """Generate maternal education impact analysis section."""
    lines = [
        "## 5. MATERNAL EDUCATION IMPACT ANALYSIS",
        "",
        "This section examines the relationship between maternal education level and",
        "adolescent girls' menstrual hygiene knowledge and practices.",
        ""
    ]
    
    mat_ed_analysis = analysis_results.get('maternal_education_analysis', {})
    
    if mat_ed_analysis and not mat_ed_analysis.get('summary_table', pd.DataFrame()).empty:
        summary_table = mat_ed_analysis['summary_table']
        test_type = mat_ed_analysis.get('test_type', 'ANOVA')
        anova_knowledge = mat_ed_analysis.get('anova_knowledge', {})
        anova_practice = mat_ed_analysis.get('anova_practice', {})
        
        lines.extend([
            "### 5.1 Scores by Maternal Education Level",
            ""
        ])
        
        # Display summary table
        for _, row in summary_table.iterrows():
            label = _format_maternal_education_label(row['education_level'])
            lines.extend([
                f"**{label}** (n={int(row['n'])})",
                f"  Knowledge Score: {_format_mean_sd(row['mean_knowledge'], row['std_knowledge'])}",
                f"  Practice Score: {_format_mean_sd(row['mean_practice'], row['std_practice'])}",
                ""
            ])
        
        # Statistical test results
        test_type_by_outcome = mat_ed_analysis.get('test_type_by_outcome', {})
        assumption_checks = mat_ed_analysis.get('assumption_checks', {})

        lines.extend([
            "### 5.2 Statistical Significance Testing",
            "",
            f"**Test Used**: {test_type}",
            ""
        ])
        
        # Knowledge scores test
        if 'p_value' in anova_knowledge:
            p_val_k = anova_knowledge['p_value']
            f_stat_k = anova_knowledge.get('f_statistic', 0)
            effect_k = anova_knowledge.get('effect_size')
            effect_k_type = anova_knowledge.get('effect_size_type')
            outcome_test_k = test_type_by_outcome.get('knowledge')
            
            lines.extend([
                "**Knowledge Scores:**",
                f"  Test Type: {outcome_test_k}" if outcome_test_k else "  Test Type: (see overall)",
                f"  Test Statistic: {f_stat_k:.4f}",
                f"  P-value: {p_val_k:.4f}",
            ])

            if effect_k is not None and not pd.isna(effect_k):
                lines.append(f"  Effect Size ({effect_k_type}): {effect_k:.4f}")

            if assumption_checks.get('knowledge'):
                checks = assumption_checks['knowledge']
                lines.append(
                    "  Assumptions: Shapiro-Wilk min p="
                    f"{_format_p_value(checks.get('normality_min_p'))}, "
                    f"Levene p={_format_p_value(checks.get('variance_p'))}"
                )
                if checks.get('small_groups') or checks.get('insufficient_normality'):
                    lines.append("  Note: Small group sizes limit parametric assumptions")
            
            if p_val_k < 0.001:
                interpretation = "highly significant (p < 0.001)"
            elif p_val_k < 0.01:
                interpretation = "very significant (p < 0.01)"
            elif p_val_k < 0.05:
                interpretation = "significant (p < 0.05)"
            else:
                interpretation = "not significant (p ≥ 0.05)"
            
            lines.extend([
                f"  Interpretation: The difference in knowledge scores across maternal",
                f"                  education levels is {interpretation}.",
                ""
            ])
        
        # Practice scores test
        if 'p_value' in anova_practice:
            p_val_p = anova_practice['p_value']
            f_stat_p = anova_practice.get('f_statistic', 0)
            effect_p = anova_practice.get('effect_size')
            effect_p_type = anova_practice.get('effect_size_type')
            outcome_test_p = test_type_by_outcome.get('practice')
            
            lines.extend([
                "**Practice Scores:**",
                f"  Test Type: {outcome_test_p}" if outcome_test_p else "  Test Type: (see overall)",
                f"  Test Statistic: {f_stat_p:.4f}",
                f"  P-value: {p_val_p:.4f}",
            ])

            if effect_p is not None and not pd.isna(effect_p):
                lines.append(f"  Effect Size ({effect_p_type}): {effect_p:.4f}")

            if assumption_checks.get('practice'):
                checks = assumption_checks['practice']
                lines.append(
                    "  Assumptions: Shapiro-Wilk min p="
                    f"{_format_p_value(checks.get('normality_min_p'))}, "
                    f"Levene p={_format_p_value(checks.get('variance_p'))}"
                )
                if checks.get('small_groups') or checks.get('insufficient_normality'):
                    lines.append("  Note: Small group sizes limit parametric assumptions")
            
            if p_val_p < 0.001:
                interpretation = "highly significant (p < 0.001)"
            elif p_val_p < 0.01:
                interpretation = "very significant (p < 0.01)"
            elif p_val_p < 0.05:
                interpretation = "significant (p < 0.05)"
            else:
                interpretation = "not significant (p ≥ 0.05)"
            
            lines.extend([
                f"  Interpretation: The difference in practice scores across maternal",
                f"                  education levels is {interpretation}.",
                ""
            ])
        
        lines.extend([
            "**Visualizations**:",
            "  - See 'scores_by_maternal_education.png' for bar chart with error bars",
            "  - See 'score_boxplots.png' for box plots by education level",
            ""
        ])
    else:
        lines.extend([
            "Maternal education analysis could not be performed due to insufficient data.",
            ""
        ])
    
    lines.append("")
    return lines


def _generate_correlation_section(analysis_results: Dict[str, Any]) -> list:
    """Generate correlation analysis section."""
    lines = [
        "## 6. CORRELATION ANALYSIS",
        "",
        "Pearson correlation coefficients between continuous variables (complete-case).",
        ""
    ]
    
    correlations = analysis_results.get('correlations', pd.DataFrame())
    
    if not correlations.empty:
        lines.append("### 6.1 Correlation Matrix")
        lines.append("")
        
        # Display key correlations
        lines.append("**Key Findings:**")
        lines.append("")

        pvalues = analysis_results.get('correlation_pvalues', pd.DataFrame())
        seen_pairs = set()

        def format_pair_label(var_name: str) -> str:
            return var_name.replace('_', ' ').title()

        for source in ['knowledge_score', 'practice_score']:
            if source not in correlations.columns:
                continue
            for col in correlations.columns:
                if col in [source, 'total_score']:
                    continue
                pair_key = tuple(sorted([source, col]))
                if pair_key in seen_pairs:
                    continue
                corr_val = correlations.loc[source, col]
                if pd.isna(corr_val):
                    continue

                p_val = None
                if not pvalues.empty and source in pvalues.columns and col in pvalues.columns:
                    p_val = pvalues.loc[source, col]

                if abs(corr_val) >= 0.3 and (p_val is None or p_val < 0.05):
                    label = f"{format_pair_label(source)} ↔ {format_pair_label(col)}"
                    if p_val is not None:
                        lines.append(f"  {label}: r={corr_val:.3f}, p={p_val:.4f}")
                    else:
                        lines.append(f"  {label}: r={corr_val:.3f}")

                seen_pairs.add(pair_key)
        
        lines.extend([
            "",
            "**Visualization**: See 'scatter_matrix.png' for scatter plots",
            ""
        ])
    else:
        lines.extend([
            "Correlation analysis could not be performed due to insufficient data.",
            ""
        ])
    
    lines.append("")
    return lines


def _generate_files_reference_section(output_folder: str) -> list:
    """Generate section listing all output files."""
    lines = [
        "## 7. GENERATED OUTPUT FILES",
        "",
        "All analysis outputs have been saved to the output folder:",
        f"{output_folder}",
        "",
        "### 7.1 Data Files",
        ""
    ]
    
    # List expected data files
    data_files = [
        ("scored_dataset.csv", "Complete dataset with all calculated scores and derived fields"),
        ("maternal_education_summary.csv", "Summary statistics by maternal education level"),
        ("demographic_age_freq.csv", "Frequency distribution for age"),
        ("demographic_maternal_education_freq.csv", "Frequency distribution for maternal education"),
        ("demographic_paternal_education_freq.csv", "Frequency distribution for paternal education"),
        ("demographic_maternal_occupation_freq.csv", "Frequency distribution for maternal occupation"),
        ("demographic_paternal_occupation_freq.csv", "Frequency distribution for paternal occupation"),
        ("demographic_continuous_stats.csv", "Descriptive statistics for continuous variables"),
        ("correlation_matrix.csv", "Correlation coefficients between continuous variables"),
        ("correlation_pvalues.csv", "P-values for Pearson correlations"),
        ("data_quality_summary.txt", "Data quality assessment summary"),
        ("data_quality_missing_values.csv", "Missing value details"),
        ("data_quality_invalid_values.csv", "Invalid value details (if any)")
    ]
    
    for filename, description in data_files:
        lines.append(f"  - **{filename}**: {description}")
    
    lines.extend([
        "",
        "### 7.2 Visualization Files",
        ""
    ])
    
    # List expected visualization files
    viz_files = [
        ("scores_by_maternal_education.png", "Bar chart showing mean scores by education level"),
        ("score_distributions.png", "Histograms of knowledge and practice score distributions"),
        ("score_boxplots.png", "Box plots comparing scores across education groups"),
        ("scatter_matrix.png", "Scatter plot matrix for continuous variables")
    ]
    
    for filename, description in viz_files:
        lines.append(f"  - **{filename}**: {description}")
    
    lines.extend([
        "",
        "### 7.3 Report Files",
        "",
        "  - **analysis_report.txt**: This report in plain text format",
        "  - **analysis_report.md**: This report in Markdown format",
        "  - **FILE_INVENTORY.md**: Complete inventory of all output files",
        ""
    ])
    
    return lines


def _generate_footer_section() -> list:
    """Generate report footer."""
    lines = [
        "=" * 80,
        "",
        "## NOTES",
        "",
        "- All statistical tests use α = 0.05 significance level",
        "- Missing values were handled according to predefined rules (0 for scores, null for calculations)",
        "- Conditional/skip-logic columns are reported separately in data quality summaries",
        "- Group sizes may be imbalanced; interpret small-n groups with caution",
        "- All visualizations are saved at 300 DPI resolution in PNG format",
        "- For detailed methodology, refer to the analysis documentation",
        "",
        "=" * 80,
        "",
        "END OF REPORT",
        ""
    ]
    
    return lines
