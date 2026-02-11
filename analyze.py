#!/usr/bin/env python3
"""
Menstrual Hygiene Analysis Pipeline

Main entry point for the menstrual hygiene awareness analysis system.
This script orchestrates the complete analysis pipeline from SPSS data loading
through statistical analysis, visualization, and report generation.

Usage:
    python analyze.py <spss_file_path> [output_folder]

Arguments:
    spss_file_path: Path to the SPSS .sav file containing survey data
    output_folder: Optional base path for output folder (default: "output")

Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 11.3
"""

import sys
import os
import argparse
import logging
from datetime import datetime
from pathlib import Path

# Import analysis modules
from src.data_loader import load_spss_file, validate_required_columns, generate_data_summary
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


def setup_logging(output_folder: str) -> str:
    """
    Configure logging for the analysis pipeline.
    
    Creates a log file in the output folder and configures console output.
    
    Args:
        output_folder: Directory where log file will be saved
        
    Returns:
        Path to the log file
    """
    log_file = os.path.join(output_folder, 'analysis.log')
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return log_file


def parse_arguments():
    """
    Parse command-line arguments.
    
    Returns:
        Namespace object with parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Menstrual Hygiene Awareness Analysis System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python analyze.py data.sav
    python analyze.py data.sav custom_output
    python analyze.py "path/to/survey data.sav" results

For more information, see README.md
        """
    )
    
    parser.add_argument(
        'spss_file',
        type=str,
        help='Path to the SPSS .sav file containing survey data'
    )
    
    parser.add_argument(
        'output_base',
        type=str,
        nargs='?',
        default='output',
        help='Base directory for output files (default: output)'
    )
    
    return parser.parse_args()


def log_analysis_parameters(spss_file: str, output_folder: str):
    """
    Log all analysis parameters for reproducibility.
    
    Args:
        spss_file: Path to SPSS input file
        output_folder: Path to output folder
    """
    logging.info("=" * 80)
    logging.info("ANALYSIS PARAMETERS")
    logging.info("=" * 80)
    logging.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"SPSS File: {spss_file}")
    logging.info(f"Output Folder: {output_folder}")
    logging.info(f"Python Version: {sys.version}")
    logging.info(f"Working Directory: {os.getcwd()}")
    logging.info("=" * 80)


def main():
    """
    Main pipeline orchestration function.
    
    Executes all analysis stages in sequence:
    1. Data loading and validation
    2. Data processing and scoring
    3. Statistical analysis
    4. Visualization generation
    5. Report generation
    6. Output file management
    
    Handles errors at each stage and provides clear progress messages.
    """
    # Parse command-line arguments
    args = parse_arguments()
    spss_file_path = args.spss_file
    output_base_path = args.output_base
    
    try:
        # ===================================================================
        # STAGE 0: Setup
        # ===================================================================
        print("\n" + "=" * 80)
        print("MENSTRUAL HYGIENE AWARENESS ANALYSIS")
        print("=" * 80)
        print(f"\nStarting analysis at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Input file: {spss_file_path}")
        
        # Create output folder
        print("\n[1/7] Creating output folder...")
        output_folder = create_output_folder(output_base_path)
        print(f"      Output folder created: {output_folder}")
        
        # Setup logging
        log_file = setup_logging(output_folder)
        log_analysis_parameters(spss_file_path, output_folder)
        
        # ===================================================================
        # STAGE 1: Data Loading
        # ===================================================================
        print("\n[2/7] Loading SPSS data file...")
        logging.info("Stage 1: Loading SPSS data file")
        
        try:
            df, metadata = load_spss_file(spss_file_path)
            logging.info(f"Successfully loaded {len(df)} records with {len(df.columns)} variables")
            print(f"      Loaded {len(df)} records with {len(df.columns)} variables")
            
            # Generate and display data summary
            summary = generate_data_summary(df)
            logging.info(f"Data summary: {summary['row_count']} rows, {summary['column_count']} columns")
            
        except FileNotFoundError as e:
            logging.error(f"File not found: {str(e)}")
            print(f"\nERROR: {str(e)}")
            print("\nPlease check that the file path is correct and try again.")
            sys.exit(1)
        except PermissionError as e:
            logging.error(f"Permission denied: {str(e)}")
            print(f"\nERROR: {str(e)}")
            print("\nPlease check file permissions and try again.")
            sys.exit(1)
        except Exception as e:
            logging.error(f"Failed to load SPSS file: {str(e)}")
            print(f"\nERROR: Failed to load SPSS file")
            print(f"Details: {str(e)}")
            sys.exit(1)
        
        # ===================================================================
        # STAGE 2: Data Processing and Scoring
        # ===================================================================
        print("\n[3/7] Processing data and calculating scores...")
        logging.info("Stage 2: Data processing and scoring")
        
        try:
            scored_df = create_scored_dataset(df)
            logging.info("Successfully calculated all scores and derived fields")
            print(f"      Calculated scores for {len(scored_df)} records")
            
            # Save scored dataset
            scored_file = save_dataframe(scored_df, 'scored_dataset.csv', output_folder)
            logging.info(f"Scored dataset saved to: {scored_file}")
            print(f"      Scored dataset saved: scored_dataset.csv")
            
        except Exception as e:
            logging.error(f"Failed during data processing: {str(e)}")
            print(f"\nERROR: Failed during data processing")
            print(f"Details: {str(e)}")
            sys.exit(1)
        
        # ===================================================================
        # STAGE 3: Data Quality Assessment
        # ===================================================================
        print("\n[4/7] Assessing data quality...")
        logging.info("Stage 3: Data quality assessment")
        
        try:
            quality_report = generate_data_quality_report(scored_df, output_path=output_folder)
            logging.info(f"Data quality: {quality_report['summary']['data_quality_percentage']}%")
            print(f"      Data quality: {quality_report['summary']['data_quality_percentage']}%")
            print(f"      Missing values: {quality_report['summary']['missing_value_count']}")
            print(f"      Invalid values: {quality_report['summary']['invalid_value_count']}")
            
        except Exception as e:
            logging.warning(f"Data quality assessment encountered issues: {str(e)}")
            print(f"      Warning: Data quality assessment incomplete")
            quality_report = {'summary': {}, 'warnings': []}
        
        # ===================================================================
        # STAGE 4: Statistical Analysis
        # ===================================================================
        print("\n[5/7] Performing statistical analyses...")
        logging.info("Stage 4: Statistical analysis")
        
        analysis_results = {}
        
        try:
            # Maternal education analysis
            print("      - Analyzing maternal education impact...")
            mat_ed_analysis = analyze_maternal_education_impact(scored_df)
            analysis_results['maternal_education_analysis'] = mat_ed_analysis
            
            if not mat_ed_analysis['summary_table'].empty:
                logging.info(f"Maternal education analysis complete: {len(mat_ed_analysis['summary_table'])} groups")
                
                # Save summary table
                save_dataframe(
                    mat_ed_analysis['summary_table'],
                    'maternal_education_summary.csv',
                    output_folder
                )
            
            # Demographic summaries
            print("      - Calculating demographic summaries...")
            demo_summaries = calculate_demographic_summaries(scored_df)
            analysis_results['demographic_summaries'] = demo_summaries
            logging.info(f"Demographic summaries calculated: {len(demo_summaries)} tables")
            
            # Save demographic summaries
            for name, summary_df in demo_summaries.items():
                if not summary_df.empty:
                    save_dataframe(summary_df, f'demographic_{name}.csv', output_folder)
            
            # Correlation analysis
            print("      - Performing correlation analysis...")
            correlations = perform_correlation_analysis(scored_df)
            analysis_results['correlations'] = correlations
            
            if not correlations.empty:
                logging.info("Correlation analysis complete")
                save_dataframe(correlations, 'correlation_matrix.csv', output_folder)
            
            # Add data quality report to results
            analysis_results['data_quality_report'] = quality_report
            
            print("      Statistical analyses complete")
            
        except Exception as e:
            logging.error(f"Failed during statistical analysis: {str(e)}")
            print(f"\nERROR: Failed during statistical analysis")
            print(f"Details: {str(e)}")
            sys.exit(1)
        
        # ===================================================================
        # STAGE 5: Visualization Generation
        # ===================================================================
        print("\n[6/7] Generating visualizations...")
        logging.info("Stage 5: Visualization generation")
        
        try:
            generate_all_visualizations(scored_df, output_folder)
            logging.info("All visualizations generated successfully")
            print("      All visualizations generated")
            
        except Exception as e:
            logging.warning(f"Some visualizations failed to generate: {str(e)}")
            print(f"      Warning: Some visualizations may be incomplete")
        
        # ===================================================================
        # STAGE 6: Report Generation
        # ===================================================================
        print("\n[7/7] Generating analysis report...")
        logging.info("Stage 6: Report generation")
        
        try:
            txt_report, md_report = generate_analysis_report(
                analysis_results,
                scored_df,
                output_folder,
                spss_file_path
            )
            logging.info(f"Analysis reports generated: {txt_report}, {md_report}")
            print("      Analysis report generated")
            
        except Exception as e:
            logging.error(f"Failed to generate report: {str(e)}")
            print(f"\nERROR: Failed to generate report")
            print(f"Details: {str(e)}")
            sys.exit(1)
        
        # ===================================================================
        # STAGE 7: File Inventory
        # ===================================================================
        try:
            file_descriptions = {
                'scored_dataset.csv': 'Complete dataset with all calculated scores',
                'maternal_education_summary.csv': 'Summary statistics by maternal education level',
                'correlation_matrix.csv': 'Correlation coefficients between continuous variables',
                'scores_by_maternal_education.png': 'Bar chart of mean scores by education level',
                'score_distributions.png': 'Histograms of score distributions',
                'score_boxplots.png': 'Box plots comparing scores across education groups',
                'scatter_matrix.png': 'Scatter plot matrix for continuous variables',
                'analysis_report.txt': 'Comprehensive analysis report (text format)',
                'analysis_report.md': 'Comprehensive analysis report (markdown format)',
                'analysis.log': 'Analysis execution log with all parameters and messages',
                'data_quality_summary.txt': 'Data quality assessment summary'
            }
            
            inventory_file = generate_file_inventory(output_folder, file_descriptions)
            logging.info(f"File inventory generated: {inventory_file}")
            
        except Exception as e:
            logging.warning(f"Failed to generate file inventory: {str(e)}")
        
        # ===================================================================
        # SUCCESS
        # ===================================================================
        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)
        print(f"\nAll outputs have been saved to:")
        print(f"  {output_folder}")
        print(f"\nKey files:")
        print(f"  - scored_dataset.csv: Complete dataset with calculated scores")
        print(f"  - analysis_report.txt: Comprehensive analysis report")
        print(f"  - FILE_INVENTORY.md: Complete list of all output files")
        print(f"  - analysis.log: Detailed execution log")
        print(f"\nVisualization files:")
        print(f"  - scores_by_maternal_education.png")
        print(f"  - score_distributions.png")
        print(f"  - score_boxplots.png")
        print(f"  - scatter_matrix.png")
        print(f"\nAnalysis completed successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80 + "\n")
        
        logging.info("Analysis pipeline completed successfully")
        
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user")
        logging.warning("Analysis interrupted by user (KeyboardInterrupt)")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUNEXPECTED ERROR: {str(e)}")
        logging.error(f"Unexpected error in main pipeline: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
