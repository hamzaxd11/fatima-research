"""
Convert SPSS data to multiple readable formats for review.
"""

import pandas as pd
from src.data_loader import load_spss_file
from src.data_processor import create_scored_dataset

# Load the SPSS file
print("Loading SPSS data...")
df, metadata = load_spss_file('menstrual hygiene spss.sav fatima and ayesha (1).sav')

# Process the data to add scores
print("Processing data and calculating scores...")
scored_df = create_scored_dataset(df)

# Save in multiple formats
print("\nSaving converted data in multiple formats...")

# 1. Original data as CSV
output_file_original = 'output/original_data.csv'
df.to_csv(output_file_original, index=False)
print(f"✓ Original data saved to: {output_file_original}")

# 2. Scored data as CSV
output_file_scored = 'output/scored_data_with_calculations.csv'
scored_df.to_csv(output_file_scored, index=False)
print(f"✓ Scored data saved to: {output_file_scored}")

# 3. Excel format with multiple sheets
output_file_excel = 'output/menstrual_hygiene_data.xlsx'
with pd.ExcelWriter(output_file_excel, engine='openpyxl') as writer:
    # Original data
    df.to_excel(writer, sheet_name='Original Data', index=False)
    
    # Scored data
    scored_df.to_excel(writer, sheet_name='Scored Data', index=False)
    
    # Summary statistics
    summary_stats = pd.DataFrame({
        'Metric': ['Total Records', 'Total Columns', 'Knowledge Score Mean', 
                   'Knowledge Score Std', 'Practice Score Mean', 'Practice Score Std',
                   'Total Score Mean', 'Total Score Std', 'Per Capita Income Mean',
                   'Per Capita Income Std', 'Valid Per Capita Records'],
        'Value': [
            len(scored_df),
            len(scored_df.columns),
            scored_df['knowledge_score'].mean(),
            scored_df['knowledge_score'].std(),
            scored_df['practice_score'].mean(),
            scored_df['practice_score'].std(),
            scored_df['total_score'].mean(),
            scored_df['total_score'].std(),
            scored_df['per_capita_income'].mean(),
            scored_df['per_capita_income'].std(),
            scored_df['per_capita_income'].notna().sum()
        ]
    })
    summary_stats.to_excel(writer, sheet_name='Summary Statistics', index=False)
    
    # Score distributions
    score_dist = pd.DataFrame({
        'Knowledge Score': scored_df['knowledge_score'].value_counts().sort_index(),
        'Practice Score': scored_df['practice_score'].value_counts().sort_index(),
        'Total Score': scored_df['total_score'].value_counts().sort_index()
    }).fillna(0).astype(int)
    score_dist.to_excel(writer, sheet_name='Score Distributions')
    
    # Missing data analysis
    missing_data = pd.DataFrame({
        'Column': df.columns,
        'Missing Count': [df[col].isna().sum() for col in df.columns],
        'Missing Percentage': [f"{(df[col].isna().sum() / len(df) * 100):.1f}%" for col in df.columns]
    })
    missing_data = missing_data[missing_data['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
    missing_data.to_excel(writer, sheet_name='Missing Data Analysis', index=False)

print(f"✓ Excel file with multiple sheets saved to: {output_file_excel}")

# 4. Human-readable text report
output_file_txt = 'output/data_report.txt'
with open(output_file_txt, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("MENSTRUAL HYGIENE DATA ANALYSIS REPORT\n")
    f.write("=" * 80 + "\n\n")
    
    f.write(f"Total Records: {len(scored_df)}\n")
    f.write(f"Total Columns: {len(scored_df.columns)}\n\n")
    
    f.write("=" * 80 + "\n")
    f.write("SCORE STATISTICS\n")
    f.write("=" * 80 + "\n\n")
    
    f.write("Knowledge Score (0-9):\n")
    f.write(f"  Mean:   {scored_df['knowledge_score'].mean():.2f}\n")
    f.write(f"  Median: {scored_df['knowledge_score'].median():.2f}\n")
    f.write(f"  Std:    {scored_df['knowledge_score'].std():.2f}\n")
    f.write(f"  Min:    {scored_df['knowledge_score'].min()}\n")
    f.write(f"  Max:    {scored_df['knowledge_score'].max()}\n\n")
    
    f.write("Practice Score (0-7):\n")
    f.write(f"  Mean:   {scored_df['practice_score'].mean():.2f}\n")
    f.write(f"  Median: {scored_df['practice_score'].median():.2f}\n")
    f.write(f"  Std:    {scored_df['practice_score'].std():.2f}\n")
    f.write(f"  Min:    {scored_df['practice_score'].min()}\n")
    f.write(f"  Max:    {scored_df['practice_score'].max()}\n\n")
    
    f.write("Total Score (0-16):\n")
    f.write(f"  Mean:   {scored_df['total_score'].mean():.2f}\n")
    f.write(f"  Median: {scored_df['total_score'].median():.2f}\n")
    f.write(f"  Std:    {scored_df['total_score'].std():.2f}\n")
    f.write(f"  Min:    {scored_df['total_score'].min()}\n")
    f.write(f"  Max:    {scored_df['total_score'].max()}\n\n")
    
    f.write("Per Capita Income:\n")
    valid_pci = scored_df['per_capita_income'].dropna()
    f.write(f"  Valid Records: {len(valid_pci)}/{len(scored_df)} ({len(valid_pci)/len(scored_df)*100:.1f}%)\n")
    f.write(f"  Mean:   {valid_pci.mean():.2f}\n")
    f.write(f"  Median: {valid_pci.median():.2f}\n")
    f.write(f"  Std:    {valid_pci.std():.2f}\n")
    f.write(f"  Min:    {valid_pci.min():.2f}\n")
    f.write(f"  Max:    {valid_pci.max():.2f}\n\n")
    
    f.write("=" * 80 + "\n")
    f.write("SCORE DISTRIBUTIONS\n")
    f.write("=" * 80 + "\n\n")
    
    f.write("Knowledge Score Distribution:\n")
    for score in range(10):
        count = (scored_df['knowledge_score'] == score).sum()
        pct = count / len(scored_df) * 100
        bar = "█" * int(pct / 2)
        f.write(f"  {score}: {count:3d} ({pct:5.1f}%) {bar}\n")
    
    f.write("\nPractice Score Distribution:\n")
    for score in range(8):
        count = (scored_df['practice_score'] == score).sum()
        pct = count / len(scored_df) * 100
        bar = "█" * int(pct / 2)
        f.write(f"  {score}: {count:3d} ({pct:5.1f}%) {bar}\n")
    
    f.write("\n" + "=" * 80 + "\n")
    f.write("SAMPLE DATA (First 10 Records)\n")
    f.write("=" * 80 + "\n\n")
    
    # Show key columns for first 10 records
    sample_cols = ['Age', 'MotherEducation', 'IncomePerMonth', 'total_family_members', 
                   'per_capita_income', 'knowledge_score', 'practice_score', 'total_score']
    sample_data = scored_df[sample_cols].head(10)
    f.write(sample_data.to_string())
    
    f.write("\n\n" + "=" * 80 + "\n")
    f.write("COLUMN NAMES\n")
    f.write("=" * 80 + "\n\n")
    
    for i, col in enumerate(scored_df.columns, 1):
        f.write(f"{i:2d}. {col}\n")

print(f"✓ Text report saved to: {output_file_txt}")

# 5. Save a subset with just the key columns for easy viewing
output_file_key = 'output/key_data_columns.csv'
key_columns = [
    'Age', 'MotherEducation', 'FatherEducation', 
    'IncomePerMonth', 'total_family_members', 'per_capita_income',
    'RangeOfUsualAgeOfMenarche', 'WhatDoYouThinkAboutThePrecessofMensturation',
    'OrganOfBodyResponsibleForMenarche', 'RangeOfNormalDurationOfMensturalBleeding',
    'AfterHowManyDaysDoYouMensturateEveryMonth',
    'WhichTypeOfAbsorbentDoYouUseDuringMensturation',
    'HowManyTimeUsualyChangeTheClothandSanitaryPad',
    'HowManyTimesTakeBathDuringMensturation',
    'knowledge_score', 'practice_score', 'total_score'
]
key_data = scored_df[[col for col in key_columns if col in scored_df.columns]]
key_data.to_csv(output_file_key, index=False)
print(f"✓ Key columns data saved to: {output_file_key}")

print("\n" + "=" * 80)
print("CONVERSION COMPLETE!")
print("=" * 80)
print("\nFiles created:")
print(f"  1. {output_file_original} - Original SPSS data as CSV")
print(f"  2. {output_file_scored} - Scored data with calculations")
print(f"  3. {output_file_excel} - Excel file with multiple sheets")
print(f"  4. {output_file_txt} - Human-readable text report")
print(f"  5. {output_file_key} - Key columns only for easy viewing")
print("\nYou can now open these files to review the data!")
