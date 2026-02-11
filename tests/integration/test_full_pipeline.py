"""
Integration tests for the complete analysis pipeline.

Tests the full workflow from SPSS file loading through all analysis stages
to final output generation. Validates that all expected outputs are created
and contain reasonable data.

Requirements: 10.2, 8.2, 8.3, 8.4, 8.5, 9.1
"""

import os
import sys
import tempfile
import shutil
import pytest
import pandas as pd
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.data_loader import load_spss_file, generate_data_summary
from src.data_processor import create_scored_dataset
from src.statistical_analysis import (
    analyze_maternal_education_impact,
    calculate_demographic_summaries,
    perform_correlation_analysis
)
from src.visualizations import generate_all_visualizations
from src.report_generator import generate_analysis_report
from src.output_manager import create_output_folder, save_dataframe, generate_file_inventory
from src.data_quality import generate_data_quality_report


class TestFullPipeline:
    """Integration tests for complete pipeline execution."""
    
    @pytest.fixture
    def temp_output_dir(self):
        """Create a temporary output directory for tests."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Cleanup after test
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def sample_spss_data(self):
        """Create minimal sample SPSS-like data for testing."""
        data = {
            'age': [15, 16, 14, 17, 15],
            'mother_education': ['Illiterate', 'Primary', 'Secondary', 'Intermediate and above', 'Middle'],
            'father_education': ['Primary', 'Secondary', 'Intermediate and above', 'Secondary', 'Middle'],
            'income_per_month': [20000, 30000, 40000, 50000, 25000],
            'no_family_members_male': [3, 2, 4, 3, 2],
            'no_family_members_female': [2, 3, 2, 3, 3],
            # Knowledge questions (Section III) - 9 questions
            'q3_1': [1, 1, 0, 1, 1],
            'q3_2': [1, 0, 1, 1, 0],
            'q3_3': [0, 1, 1, 1, 1],
            'q3_4': [1, 1, 1, 0, 1],
            'q3_5': [1, 0, 1, 1, 1],
            'q3_6': [0, 1, 0, 1, 0],
            'q3_7': [1, 1, 1, 1, 1],
            'q3_8': [1, 0, 1, 0, 1],
            'q3_9': [0, 1, 0, 1, 1],
            # Practice questions (Section IV) - 7 questions
            'q4_1': [1, 1, 0, 1, 1],
            'q4_2': [1, 0, 1, 1, 0],
            'q4_3': [0, 1, 1, 1, 1],
            'q4_4': [1, 1, 1, 0, 1],
            'q4_5': [1, 0, 1, 1, 1],
            'q4_6': [0, 1, 0, 1, 0],
            'q4_7': [1, 1, 1, 1, 1],
        }
        return pd.DataFrame(data)
    
    def test_complete_pipeline_execution(self, sample_spss_data, temp_output_dir):
        """
        Test complete workflow from data loading to output generation.
        
        Verifies that all pipeline stages execute successfully and produce
        expected outputs without errors.
        """
        # Stage 1: Data Processing
        scored_df = create_scored_dataset(sample_spss_data)
        
        # Verify scored dataset has expected columns
        assert 'knowledge_score' in scored_df.columns
        assert 'practice_score' in scored_df.columns
        assert 'per_capita_income' in scored_df.columns
        assert 'total_family_members' in scored_df.columns
        assert len(scored_df) == len(sample_spss_data)
        
        # Stage 2: Save scored dataset
        scored_file = save_dataframe(scored_df, 'scored_dataset.csv', temp_output_dir)
        assert os.path.exists(scored_file)
        
        # Stage 3: Data Quality Assessment
        quality_report = generate_data_quality_report(scored_df, output_path=temp_output_dir)
        assert 'summary' in quality_report
        assert 'missing_value_count' in quality_report['summary']
        
        # Stage 4: Statistical Analysis
        mat_ed_analysis = analyze_maternal_education_impact(scored_df)
        assert 'summary_table' in mat_ed_analysis
        assert not mat_ed_analysis['summary_table'].empty
        
        demo_summaries = calculate_demographic_summaries(scored_df)
        assert len(demo_summaries) > 0
        
        correlations = perform_correlation_analysis(scored_df)
        assert not correlations.empty
        
        # Stage 5: Visualizations
        generate_all_visualizations(scored_df, temp_output_dir)
        
        # Check that visualization files were created
        expected_viz_files = [
            'scores_by_maternal_education.png',
            'score_distributions.png',
            'score_boxplots.png',
            'scatter_matrix.png'
        ]
        
        for viz_file in expected_viz_files:
            viz_path = os.path.join(temp_output_dir, viz_file)
            assert os.path.exists(viz_path), f"Visualization file {viz_file} not created"
        
        # Stage 6: Report Generation
        analysis_results = {
            'maternal_education_analysis': mat_ed_analysis,
            'demographic_summaries': demo_summaries,
            'correlations': correlations,
            'data_quality_report': quality_report
        }
        
        txt_report, md_report = generate_analysis_report(
            analysis_results,
            scored_df,
            temp_output_dir,
            'test_data.sav'
        )
        
        assert os.path.exists(txt_report)
        assert os.path.exists(md_report)
        
        # Verify report content is not empty
        with open(txt_report, 'r', encoding='utf-8') as f:
            txt_content = f.read()
            assert len(txt_content) > 0
            assert 'MENSTRUAL HYGIENE AWARENESS ANALYSIS' in txt_content
        
        with open(md_report, 'r', encoding='utf-8') as f:
            md_content = f.read()
            assert len(md_content) > 0
            assert 'MENSTRUAL HYGIENE AWARENESS ANALYSIS REPORT' in md_content
    
    def test_all_output_files_generated(self, sample_spss_data, temp_output_dir):
        """
        Verify all expected output files are generated.
        
        Tests that the complete pipeline produces all required CSV files,
        visualizations, and reports.
        """
        # Run complete pipeline
        scored_df = create_scored_dataset(sample_spss_data)
        save_dataframe(scored_df, 'scored_dataset.csv', temp_output_dir)
        
        quality_report = generate_data_quality_report(scored_df, output_path=temp_output_dir)
        
        mat_ed_analysis = analyze_maternal_education_impact(scored_df)
        save_dataframe(
            mat_ed_analysis['summary_table'],
            'maternal_education_summary.csv',
            temp_output_dir
        )
        
        demo_summaries = calculate_demographic_summaries(scored_df)
        for name, summary_df in demo_summaries.items():
            if not summary_df.empty:
                save_dataframe(summary_df, f'demographic_{name}.csv', temp_output_dir)
        
        correlations = perform_correlation_analysis(scored_df)
        save_dataframe(correlations, 'correlation_matrix.csv', temp_output_dir)
        
        generate_all_visualizations(scored_df, temp_output_dir)
        
        analysis_results = {
            'maternal_education_analysis': mat_ed_analysis,
            'demographic_summaries': demo_summaries,
            'correlations': correlations,
            'data_quality_report': quality_report
        }
        
        generate_analysis_report(
            analysis_results,
            scored_df,
            temp_output_dir,
            'test_data.sav'
        )
        
        # Verify all expected files exist
        expected_files = [
            'scored_dataset.csv',
            'maternal_education_summary.csv',
            'correlation_matrix.csv',
            'scores_by_maternal_education.png',
            'score_distributions.png',
            'score_boxplots.png',
            'scatter_matrix.png',
            'analysis_report.txt',
            'analysis_report.md',
            'data_quality_summary.txt'
        ]
        
        for expected_file in expected_files:
            file_path = os.path.join(temp_output_dir, expected_file)
            assert os.path.exists(file_path), f"Expected output file {expected_file} not found"
    
    def test_report_content_accuracy(self, sample_spss_data, temp_output_dir):
        """
        Verify report content includes all required sections and data.
        
        Tests that generated reports contain demographic summaries,
        statistical results, and references to all tables and charts.
        """
        # Run pipeline
        scored_df = create_scored_dataset(sample_spss_data)
        quality_report = generate_data_quality_report(scored_df, output_path=temp_output_dir)
        
        mat_ed_analysis = analyze_maternal_education_impact(scored_df)
        demo_summaries = calculate_demographic_summaries(scored_df)
        correlations = perform_correlation_analysis(scored_df)
        
        generate_all_visualizations(scored_df, temp_output_dir)
        
        analysis_results = {
            'maternal_education_analysis': mat_ed_analysis,
            'demographic_summaries': demo_summaries,
            'correlations': correlations,
            'data_quality_report': quality_report
        }
        
        txt_report, md_report = generate_analysis_report(
            analysis_results,
            scored_df,
            temp_output_dir,
            'test_data.sav'
        )
        
        # Read and verify text report content
        with open(txt_report, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for required sections
        assert 'DEMOGRAPHIC SUMMARY' in content
        assert 'KNOWLEDGE SCORES' in content or 'Knowledge Score' in content
        assert 'PRACTICE SCORES' in content or 'Practice Score' in content
        assert 'MATERNAL EDUCATION' in content or 'Maternal Education' in content
        
        # Check for statistical results
        assert 'Mean' in content or 'mean' in content
        assert 'Standard Deviation' in content or 'Std' in content
        
        # Check for file references
        assert 'scored_dataset.csv' in content
        assert '.png' in content  # References to visualization files
        
        # Verify markdown report has similar content
        with open(md_report, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        assert '##' in md_content  # Has markdown headers
        assert 'scored_dataset.csv' in md_content


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
