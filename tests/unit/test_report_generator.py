"""
Unit tests for report_generator module

Tests report generation functionality with sample data.
"""

import os
import tempfile
import pandas as pd
import numpy as np
from src.report_generator import generate_analysis_report


def test_report_generation_basic():
    """Test that report generation works with minimal data."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create minimal scored dataset
        scored_dataset = pd.DataFrame({
            'age': [15, 16, 17],
            'mother_education': ['Primary', 'Secondary', 'Intermediate'],
            'knowledge_score': [5, 7, 8],
            'practice_score': [4, 5, 6]
        })
        
        # Create minimal analysis results
        analysis_results = {
            'demographic_summaries': {},
            'maternal_education_analysis': {},
            'correlations': pd.DataFrame()
        }
        
        # Generate report
        txt_path, md_path = generate_analysis_report(
            analysis_results=analysis_results,
            scored_dataset=scored_dataset,
            output_folder=temp_dir,
            spss_file_path="test_data.sav"
        )
        
        # Verify files were created
        assert os.path.exists(txt_path), "TXT report not created"
        assert os.path.exists(md_path), "Markdown report not created"
        
        print(f"✓ Basic report generated: {txt_path}")


def test_report_generation_complete():
    """Test report generation with complete analysis results."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create sample scored dataset
        np.random.seed(42)
        n_samples = 50
        
        scored_dataset = pd.DataFrame({
            'age': np.random.randint(13, 19, n_samples),
            'mother_education': np.random.choice(['Illiterate', 'Primary', 'Secondary', 'Intermediate'], n_samples),
            'income_per_month': np.random.randint(10000, 50000, n_samples),
            'total_family_members': np.random.randint(3, 10, n_samples),
            'per_capita_income': np.random.uniform(1000, 10000, n_samples),
            'knowledge_score': np.random.randint(0, 10, n_samples),
            'practice_score': np.random.randint(0, 8, n_samples),
            'total_score': np.random.randint(0, 17, n_samples)
        })
        
        # Create complete analysis results
        analysis_results = {
            'demographic_summaries': {
                'age_freq': pd.DataFrame({
                    'age': [13, 14, 15, 16, 17, 18],
                    'count': [8, 10, 12, 9, 7, 4],
                    'percentage': [16.0, 20.0, 24.0, 18.0, 14.0, 8.0],
                    'proportion': [0.16, 0.20, 0.24, 0.18, 0.14, 0.08]
                }),
                'maternal_education_freq': pd.DataFrame({
                    'maternal_education': ['Illiterate', 'Primary', 'Secondary', 'Intermediate'],
                    'count': [12, 15, 18, 5],
                    'percentage': [24.0, 30.0, 36.0, 10.0],
                    'proportion': [0.24, 0.30, 0.36, 0.10]
                }),
                'continuous_stats': pd.DataFrame({
                    'variable': ['age', 'income', 'family_size', 'per_capita_income'],
                    'count': [50, 50, 50, 50],
                    'mean': [15.5, 30000, 6.2, 5000],
                    'median': [15.0, 28000, 6.0, 4800],
                    'std': [1.8, 12000, 2.1, 2500],
                    'min': [13, 10000, 3, 1000],
                    'max': [18, 50000, 10, 10000],
                    'q25': [14, 20000, 5, 3000],
                    'q75': [17, 40000, 8, 7000]
                })
            },
            'maternal_education_analysis': {
                'summary_table': pd.DataFrame({
                    'education_level': ['Illiterate', 'Primary', 'Secondary', 'Intermediate'],
                    'n': [12, 15, 18, 5],
                    'mean_knowledge': [4.2, 5.5, 6.8, 7.2],
                    'std_knowledge': [1.5, 1.3, 1.1, 0.8],
                    'mean_practice': [3.1, 4.2, 5.3, 5.8],
                    'std_practice': [1.2, 1.0, 0.9, 0.7],
                    'knowledge_significant': [True, True, True, True],
                    'practice_significant': [True, True, True, True]
                }),
                'anova_knowledge': {'f_statistic': 12.45, 'p_value': 0.0001},
                'anova_practice': {'f_statistic': 15.32, 'p_value': 0.00005},
                'test_type': 'ANOVA'
            },
            'correlations': pd.DataFrame({
                'knowledge_score': [1.0, 0.65, 0.42, 0.38],
                'practice_score': [0.65, 1.0, 0.51, 0.45],
                'age': [0.42, 0.51, 1.0, 0.15],
                'per_capita_income': [0.38, 0.45, 0.15, 1.0]
            }, index=['knowledge_score', 'practice_score', 'age', 'per_capita_income'])
        }
        
        # Generate report
        txt_path, md_path = generate_analysis_report(
            analysis_results=analysis_results,
            scored_dataset=scored_dataset,
            output_folder=temp_dir,
            spss_file_path="test_data.sav"
        )
        
        # Verify files were created
        assert os.path.exists(txt_path), "TXT report not created"
        assert os.path.exists(md_path), "Markdown report not created"
        
        # Verify content
        with open(txt_path, 'r', encoding='utf-8') as f:
            txt_content = f.read()
        
        # Check for key sections (Requirements 9.2, 9.3, 9.4)
        assert "MENSTRUAL HYGIENE AWARENESS ANALYSIS REPORT" in txt_content, "Missing report title"
        assert "DEMOGRAPHIC SUMMARY" in txt_content, "Missing demographics section"
        assert "KNOWLEDGE SCORES ANALYSIS" in txt_content, "Missing knowledge scores section"
        assert "PRACTICE SCORES ANALYSIS" in txt_content, "Missing practice scores section"
        assert "MATERNAL EDUCATION IMPACT ANALYSIS" in txt_content, "Missing maternal education section"
        assert "CORRELATION ANALYSIS" in txt_content, "Missing correlation section"
        assert "GENERATED OUTPUT FILES" in txt_content, "Missing files reference section"
        
        # Check for statistical results (Requirement 9.3)
        assert "P-value:" in txt_content, "Missing p-value in report"
        assert "Test Statistic:" in txt_content, "Missing test statistic in report"
        assert "ANOVA" in txt_content, "Missing test type in report"
        
        # Check for file references (Requirement 9.4)
        assert "scores_by_maternal_education.png" in txt_content, "Missing bar chart reference"
        assert "score_distributions.png" in txt_content, "Missing histogram reference"
        assert "score_boxplots.png" in txt_content, "Missing boxplot reference"
        assert "scatter_matrix.png" in txt_content, "Missing scatter matrix reference"
        
        print(f"✓ Complete report generated: {txt_path}")
        print(f"✓ Report contains all required sections")
        print(f"✓ Report length: {len(txt_content)} characters")


def test_report_content_structure():
    """Test that report has proper structure and formatting."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create minimal data
        scored_dataset = pd.DataFrame({
            'knowledge_score': [5, 6, 7],
            'practice_score': [4, 5, 6]
        })
        
        analysis_results = {
            'demographic_summaries': {},
            'maternal_education_analysis': {},
            'correlations': pd.DataFrame()
        }
        
        # Generate report
        txt_path, md_path = generate_analysis_report(
            analysis_results=analysis_results,
            scored_dataset=scored_dataset,
            output_folder=temp_dir
        )
        
        # Read content
        with open(txt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verify structure (Requirement 9.1)
        assert content.startswith("="), "Report doesn't start with separator"
        assert "Report Generated:" in content, "Missing generation timestamp"
        assert "Total Records Analyzed:" in content, "Missing record count"
        assert "END OF REPORT" in content, "Missing report footer"
        
        print("✓ Report structure is correct")


if __name__ == '__main__':
    print("Running report_generator tests...")
    print("=" * 80)
    
    test_report_generation_basic()
    test_report_generation_complete()
    test_report_content_structure()
    
    print("=" * 80)
    print("✓ All report_generator tests passed!")
