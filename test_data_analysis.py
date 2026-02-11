"""
Test script to load and analyze the actual SPSS data file.
This will help us understand the data structure, columns, and types.
"""

import sys
import pandas as pd
from src.data_loader import load_spss_file, generate_data_summary
from src.data_processor import create_scored_dataset

# Set pandas display options for better output
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 50)

def main():
    # Load the SPSS file
    spss_file = 'menstrual hygiene spss.sav fatima and ayesha (1).sav'
    
    print("=" * 80)
    print("LOADING SPSS DATA FILE")
    print("=" * 80)
    print(f"File: {spss_file}\n")
    
    try:
        df, metadata = load_spss_file(spss_file)
        print(f"✓ Successfully loaded SPSS file")
        print(f"  Rows: {len(df)}")
        print(f"  Columns: {len(df.columns)}")
        print()
        
        # Display column information
        print("=" * 80)
        print("COLUMN INFORMATION")
        print("=" * 80)
        print(f"\nTotal columns: {len(df.columns)}\n")
        
        print("Column names and data types:")
        print("-" * 80)
        for i, (col, dtype) in enumerate(df.dtypes.items(), 1):
            missing = df[col].isna().sum()
            missing_pct = (missing / len(df) * 100) if len(df) > 0 else 0
            print(f"{i:3d}. {col:40s} | Type: {str(dtype):10s} | Missing: {missing:3d} ({missing_pct:5.1f}%)")
        
        # Check for expected columns
        print("\n" + "=" * 80)
        print("CHECKING FOR EXPECTED COLUMNS")
        print("=" * 80)
        
        expected_patterns = {
            'Demographics': ['age', 'mother', 'father', 'income', 'family'],
            'Section III (Knowledge)': ['q3_', 'Q3_', 'knowledge', 'Knowledge'],
            'Section IV (Practice)': ['q4_', 'Q4_', 'practice', 'Practice']
        }
        
        for category, patterns in expected_patterns.items():
            print(f"\n{category}:")
            found_cols = []
            for col in df.columns:
                col_lower = col.lower()
                if any(pattern.lower() in col_lower for pattern in patterns):
                    found_cols.append(col)
            
            if found_cols:
                for col in found_cols:
                    print(f"  ✓ {col}")
            else:
                print(f"  ✗ No columns found matching patterns: {patterns}")
        
        # Display first few rows
        print("\n" + "=" * 80)
        print("SAMPLE DATA (First 5 rows)")
        print("=" * 80)
        print(df.head())
        
        # Display data summary statistics
        print("\n" + "=" * 80)
        print("DATA SUMMARY STATISTICS")
        print("=" * 80)
        summary = generate_data_summary(df)
        print(f"\nRow count: {summary['row_count']}")
        print(f"Column count: {summary['column_count']}")
        print(f"\nColumns with missing values:")
        missing_cols = {k: v for k, v in summary['missing_value_counts'].items() if v > 0}
        if missing_cols:
            for col, count in sorted(missing_cols.items(), key=lambda x: x[1], reverse=True):
                pct = (count / summary['row_count'] * 100) if summary['row_count'] > 0 else 0
                print(f"  {col:40s}: {count:3d} ({pct:5.1f}%)")
        else:
            print("  No missing values found")
        
        # Try to process the data
        print("\n" + "=" * 80)
        print("TESTING DATA PROCESSING")
        print("=" * 80)
        
        try:
            scored_df = create_scored_dataset(df)
            print("✓ Successfully processed data")
            print(f"\nNew columns added:")
            new_cols = set(scored_df.columns) - set(df.columns)
            for col in sorted(new_cols):
                print(f"  ✓ {col}")
            
            # Display score statistics
            if 'knowledge_score' in scored_df.columns:
                print(f"\nKnowledge Score Statistics:")
                print(f"  Mean: {scored_df['knowledge_score'].mean():.2f}")
                print(f"  Std:  {scored_df['knowledge_score'].std():.2f}")
                print(f"  Min:  {scored_df['knowledge_score'].min()}")
                print(f"  Max:  {scored_df['knowledge_score'].max()}")
            
            if 'practice_score' in scored_df.columns:
                print(f"\nPractice Score Statistics:")
                print(f"  Mean: {scored_df['practice_score'].mean():.2f}")
                print(f"  Std:  {scored_df['practice_score'].std():.2f}")
                print(f"  Min:  {scored_df['practice_score'].min()}")
                print(f"  Max:  {scored_df['practice_score'].max()}")
            
            if 'per_capita_income' in scored_df.columns:
                valid_pci = scored_df['per_capita_income'].dropna()
                print(f"\nPer Capita Income Statistics:")
                print(f"  Valid records: {len(valid_pci)}/{len(scored_df)}")
                if len(valid_pci) > 0:
                    print(f"  Mean: {valid_pci.mean():.2f}")
                    print(f"  Std:  {valid_pci.std():.2f}")
                    print(f"  Min:  {valid_pci.min():.2f}")
                    print(f"  Max:  {valid_pci.max():.2f}")
            
            # Save sample output
            print("\n" + "=" * 80)
            print("SAVING SAMPLE OUTPUT")
            print("=" * 80)
            output_file = 'output/sample_scored_data.csv'
            scored_df.to_csv(output_file, index=False)
            print(f"✓ Saved scored dataset to: {output_file}")
            
        except Exception as e:
            print(f"✗ Error processing data: {e}")
            import traceback
            traceback.print_exc()
        
    except Exception as e:
        print(f"✗ Error loading SPSS file: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    return 0

if __name__ == '__main__':
    sys.exit(main())
