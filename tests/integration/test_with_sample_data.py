"""
Integration tests using actual SPSS sample data.

Tests the complete pipeline with the real SPSS file from the project,
verifying that analysis results are reasonable and all visualizations
are generated correctly.

Requirements: 1.1, 10.2
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
from src.output_manager import save_dataframe
from src.data_quality import generate_data_quality_report


class TestWithSampleData:
    """Integration tests using actual SPSS sample data."""
    
    @pytest.fixture
    def spss_file_path(self):
        """Get path to the actual SPSS file in the project."""
        # Look for SPSS file in project root
        project_root = os.path.join(os.path.dirname(__file__), '..', '..')
        spss_file = os.path.join(project_root, 'menstrual hygiene spss.sav fatima and ayesha (1).sav')
        
        if not os.path.exists(spss_file):
            pytest.skip(f"SPSS file not found at {spss_file}")
        
        return spss_file
    
    @pytest.fixture
    def temp_output_dir(self):
        """Create a temporary output directory for tests."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Cleanup after test
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    
    def test_load_actual_spss_file(self, spss_file_path):
        """
        Test loading the actual SPSS file from the project.
        
        Verifies that the real survey data can be loaded successfully
        and contains expected structure.
        """
        df, metadata = load_spss_file(spss_file_path)
        
        # Verify data was loaded
        assert df is not None
        assert len(df) > 0, "SPSS file should contain data"
        assert len(df.columns) > 0, "SPSS file should have columns"
        
        # Generate summary
        summary = generate_data_summary(df)
        assert summary['row_count'] > 0
        assert summary['column_count'] > 0
        
        print(f"\nLoaded {summary['row_count']} records with {summary['column_count']} columns")
    
    def test_analysis_with_actual_data(self, spss_file_path, temp_output_dir):
        """
        Test complete analysis pipeline with actual SPSS data.
        
        Verifies that the real survey data produces reasonable analysis
        results and all outputs are generated.
        """
        # Load actual data
        df, metadata = load_spss_file(spss_file_path)
        
        # Process and score
        scored_df = create_scored_dataset(df)
        
        # Verify scores are in valid ranges
        if 'knowledge_score' in scored_df.columns:
            knowledge_scores = scored_df['knowledge_score'].dropna()
            assert knowledge_scores.min() >= 0, "Knowledge scores should be >= 0"
            assert knowledge_scores.max() <= 9, "Knowledge scores should be <= 9"
            print(f"\nKnowledge scores: min={knowledge_scores.min()}, max={knowledge_scores.max()}, mean={knowledge_scores.mean():.2f}")
        
        if 'practice_score' in scored_df.columns:
            practice_scores = scored_df['practice_score'].dropna()
            assert practice_scores.min() >= 0, "Practice scores should be >= 0"
            assert practice_scores.max() <= 7, "Practice scores should be <= 7"
            print(f"Practice scores: min={practice_scores.min()}, max={practice_scores.max()}, mean={practice_scores.mean():.2f}")
        
        # Verify per capita income calculation
        if 'per_capita_income' in scored_df.columns:
            pci = scored_df['per_capita_income'].dropna()
            assert (pci >= 0).all(), "Per capita income should be non-negative"
            print(f"Per capita income: min={pci.min():.2f}, max={pci.max():.2f}, mean={pci.mean():.2f}")
        
        # Save scored dataset
        scored_file = save_dataframe(scored_df, 'scored_dataset.csv', temp_output_dir)
        assert os.path.exists(scored_file)
        
        # Verify saved file can be read back
        saved_df = pd.read_csv(scored_file)
        assert len(saved_df) == len(scored_df)
    
    def test_statistical_analysis_results_reasonable(self, spss_file_path, temp_output_dir):
        """
        Verify statistical analysis produces reasonable results.
        
        Tests that maternal education analysis, demographic summaries,
        and correlations produce valid statistical outputs.
        """
        # Load and process data
        df, metadata = load_spss_file(spss_file_path)
        scored_df = create_scored_dataset(df)
        
        # Maternal education analysis
        mat_ed_analysis = analyze_maternal_education_impact(scored_df)
        
        assert 'summary_table' in mat_ed_analysis
        summary_table = mat_ed_analysis['summary_table']
        
        if not summary_table.empty:
            # Verify summary table structure
            assert 'education_level' in summary_table.columns or summary_table.index.name == 'education_level'
            assert 'n' in summary_table.columns
            
            # Verify sample sizes are positive
            assert (summary_table['n'] > 0).all(), "All groups should have positive sample sizes"
            
            # Verify means are in valid ranges if present
            if 'mean_knowledge' in summary_table.columns:
                means = summary_table['mean_knowledge'].dropna()
                assert (means >= 0).all() and (means <= 9).all(), "Knowledge means should be in [0, 9]"
            
            if 'mean_practice' in summary_table.columns:
                means = summary_table['mean_practice'].dropna()
                assert (means >= 0).all() and (means <= 7).all(), "Practice means should be in [0, 7]"
            
            print(f"\nMaternal education groups: {len(summary_table)}")
            print(summary_table)
        
        # Demographic summaries
        demo_summaries = calculate_demographic_summaries(scored_df)
        assert len(demo_summaries) > 0, "Should generate demographic summaries"
        
        # Correlation analysis
        correlations = perform_correlation_analysis(scored_df)
        
        if not correlations.empty:
            # Verify correlation values are in [-1, 1]
            assert (correlations >= -1).all().all(), "Correlations should be >= -1"
            assert (correlations <= 1).all().all(), "Correlations should be <= 1"
            
            # Diagonal should be 1 (correlation with self)
            for col in correlations.columns:
                if col in correlations.index:
                    assert abs(correlations.loc[col, col] - 1.0) < 0.01, "Self-correlation should be 1"
    
    def test_all_visualizations_generated(self, spss_file_path, temp_output_dir):
        """
        Verify all visualizations are generated with actual data.
        
        Tests that all required charts and graphs are created successfully
        using the real survey data.
        """
        # Load and process data
        df, metadata = load_spss_file(spss_file_path)
        scored_df = create_scored_dataset(df)
        
        # Generate visualizations
        generate_all_visualizations(scored_df, temp_output_dir)
        
        # Check that all expected visualization files exist
        expected_viz_files = [
            'scores_by_maternal_education.png',
            'score_distributions.png',
            'score_boxplots.png',
            'scatter_matrix.png'
        ]
        
        for viz_file in expected_viz_files:
            viz_path = os.path.join(temp_output_dir, viz_file)
            assert os.path.exists(viz_path), f"Visualization {viz_file} not created"
            
            # Verify file is not empty
            file_size = os.path.getsize(viz_path)
            assert file_size > 0, f"Visualization {viz_file} is empty"
            print(f"\n{viz_file}: {file_size} bytes")
    
    def test_data_quality_report_with_actual_data(self, spss_file_path, temp_output_dir):
        """
        Test data quality assessment with actual survey data.
        
        Verifies that data quality issues in the real dataset are
        properly identified and reported.
        """
        # Load and process data
        df, metadata = load_spss_file(spss_file_path)
        scored_df = create_scored_dataset(df)
        
        # Generate data quality report
        quality_report = generate_data_quality_report(scored_df, output_path=temp_output_dir)
        
        assert 'summary' in quality_report
        summary = quality_report['summary']
        
        # Verify summary contains expected fields
        assert 'total_rows' in summary
        assert 'missing_value_count' in summary
        assert 'invalid_value_count' in summary
        assert 'data_quality_percentage' in summary
        
        # Verify quality percentage is in valid range
        quality_pct = summary['data_quality_percentage']
        assert 0 <= quality_pct <= 100, "Quality percentage should be in [0, 100]"
        
        print(f"\nData Quality Summary:")
        print(f"  Total records: {summary['total_rows']}")
        print(f"  Missing values: {summary['missing_value_count']}")
        print(f"  Invalid values: {summary['invalid_value_count']}")
        print(f"  Quality: {quality_pct}%")
        
        # Verify quality report file was created
        quality_file = os.path.join(temp_output_dir, 'data_quality_summary.txt')
        assert os.path.exists(quality_file), "Data quality report file should be created"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
