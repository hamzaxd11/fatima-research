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
    report_lines.extend(_generate_header_section(spss_file_path, scored_dataset))
    
    # Demographics section
    report_lines.extend(_generate_demographics_section(analysis_results, scored_dataset))
    
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


def _generate_header_section(spss_file_path: Optional[str], df: pd.DataFrame) -> list:
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
            lines.append(f"  {row['maternal_education']}: {row['count']} ({row['percentage']:.1f}%)")
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


def _generate_knowledge_scores_section(analysis_results: Dict[str, Any], df: pd.DataFrame) -> list:
    """Generate knowledge scores analysis section."""
    lines = [
        "## 2. KNOWLEDGE SCORES ANALYSIS",
        "",
        "Knowledge scores range from 0 to 9, based on responses to Section III questions",
        "about menstrual hygiene awareness.",
        ""
    ]
    
    if 'knowledge_score' in df.columns:
        knowledge_scores = df['knowledge_score'].dropna()
        
        if len(knowledge_scores) > 0:
            lines.extend([
                "### 2.1 Overall Knowledge Score Statistics",
                "",
                f"  Total Respondents: {len(knowledge_scores)}",
                f"  Mean Score: {knowledge_scores.mean():.2f}",
                f"  Median Score: {knowledge_scores.median():.2f}",
                f"  Standard Deviation: {knowledge_scores.std():.2f}",
                f"  Minimum Score: {knowledge_scores.min():.0f}",
                f"  Maximum Score: {knowledge_scores.max():.0f}",
                "",
                "### 2.2 Score Distribution",
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
        "## 3. PRACTICE SCORES ANALYSIS",
        "",
        "Practice scores range from 0 to 7, based on responses to Section IV questions",
        "about actual menstrual hygiene practices.",
        ""
    ]
    
    if 'practice_score' in df.columns:
        practice_scores = df['practice_score'].dropna()
        
        if len(practice_scores) > 0:
            lines.extend([
                "### 3.1 Overall Practice Score Statistics",
                "",
                f"  Total Respondents: {len(practice_scores)}",
                f"  Mean Score: {practice_scores.mean():.2f}",
                f"  Median Score: {practice_scores.median():.2f}",
                f"  Standard Deviation: {practice_scores.std():.2f}",
                f"  Minimum Score: {practice_scores.min():.0f}",
                f"  Maximum Score: {practice_scores.max():.0f}",
                "",
                "### 3.2 Score Distribution",
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
        "## 4. MATERNAL EDUCATION IMPACT ANALYSIS",
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
            "### 4.1 Scores by Maternal Education Level",
            ""
        ])
        
        # Display summary table
        for _, row in summary_table.iterrows():
            lines.extend([
                f"**{row['education_level']}** (n={int(row['n'])})",
                f"  Knowledge Score: {row['mean_knowledge']:.2f} ± {row['std_knowledge']:.2f}",
                f"  Practice Score: {row['mean_practice']:.2f} ± {row['std_practice']:.2f}",
                ""
            ])
        
        # Statistical test results
        lines.extend([
            "### 4.2 Statistical Significance Testing",
            "",
            f"**Test Used**: {test_type}",
            ""
        ])
        
        # Knowledge scores test
        if 'p_value' in anova_knowledge:
            p_val_k = anova_knowledge['p_value']
            f_stat_k = anova_knowledge.get('f_statistic', 0)
            
            lines.extend([
                "**Knowledge Scores:**",
                f"  Test Statistic: {f_stat_k:.4f}",
                f"  P-value: {p_val_k:.4f}",
            ])
            
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
            
            lines.extend([
                "**Practice Scores:**",
                f"  Test Statistic: {f_stat_p:.4f}",
                f"  P-value: {p_val_p:.4f}",
            ])
            
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
        "## 5. CORRELATION ANALYSIS",
        "",
        "Pearson correlation coefficients between continuous variables.",
        ""
    ]
    
    correlations = analysis_results.get('correlations', pd.DataFrame())
    
    if not correlations.empty:
        lines.append("### 5.1 Correlation Matrix")
        lines.append("")
        
        # Display key correlations
        lines.append("**Key Findings:**")
        lines.append("")
        
        # Find correlations with knowledge and practice scores
        if 'knowledge_score' in correlations.columns:
            for col in correlations.columns:
                if col != 'knowledge_score':
                    corr_val = correlations.loc['knowledge_score', col]
                    if abs(corr_val) > 0.3:  # Only show moderate to strong correlations
                        lines.append(f"  Knowledge Score ↔ {col.replace('_', ' ').title()}: {corr_val:.3f}")
        
        if 'practice_score' in correlations.columns:
            for col in correlations.columns:
                if col != 'practice_score':
                    corr_val = correlations.loc['practice_score', col]
                    if abs(corr_val) > 0.3:
                        lines.append(f"  Practice Score ↔ {col.replace('_', ' ').title()}: {corr_val:.3f}")
        
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
        "## 6. GENERATED OUTPUT FILES",
        "",
        "All analysis outputs have been saved to the output folder:",
        f"{output_folder}",
        "",
        "### 6.1 Data Files",
        ""
    ]
    
    # List expected data files
    data_files = [
        ("scored_dataset.csv", "Complete dataset with all calculated scores and derived fields"),
        ("maternal_education_summary.csv", "Summary statistics by maternal education level"),
        ("demographic_summaries.csv", "Frequency distributions and descriptive statistics"),
        ("correlation_matrix.csv", "Correlation coefficients between continuous variables")
    ]
    
    for filename, description in data_files:
        lines.append(f"  - **{filename}**: {description}")
    
    lines.extend([
        "",
        "### 6.2 Visualization Files",
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
        "### 6.3 Report Files",
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
        "- All visualizations are saved at 300 DPI resolution in PNG format",
        "- For detailed methodology, refer to the analysis documentation",
        "",
        "=" * 80,
        "",
        "END OF REPORT",
        ""
    ]
    
    return lines
