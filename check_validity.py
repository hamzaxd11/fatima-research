import pandas as pd
import numpy as np
import os
import glob
from scipy import stats

# find latest scored dataset
output_dirs = ['output_final', 'output']
list_of_files = []
for out_dir in output_dirs:
    if os.path.exists(out_dir):
        list_of_files.extend(glob.glob(os.path.join(out_dir, 'analysis_*')))

if not list_of_files:
    print("No analysis output found.")
    exit()

latest_folder = max(list_of_files, key=os.path.getctime)
csv_path = os.path.join(latest_folder, 'scored_dataset.csv')
print(f"Analyzing: {csv_path}")

df = pd.read_csv(csv_path)

print(f"\n--- 1. Logic & Consistency Checks ---")
# Family Members Sum Check
# Try to find relevant columns
male_col = next((c for c in df.columns if 'male' in c.lower() and 'family' in c.lower() and 'female' not in c.lower()), None)
female_col = next((c for c in df.columns if 'female' in c.lower() and 'family' in c.lower()), None)
total_col = next((c for c in df.columns if 'total' in c.lower() and 'family' in c.lower()), None)

if male_col and female_col and total_col:
    df['calc_total'] = df[male_col].fillna(0) + df[female_col].fillna(0)
    mismatches = df[df['calc_total'] != df[total_col]]
    if len(mismatches) > 0:
        print(f"WARNING: {len(mismatches)} records have mismatched family member counts.")
        print(mismatches[[male_col, female_col, total_col, 'calc_total']].head())
    else:
        print("PASS: Family member counts are consistent.")
else:
    print(f"SKIP: Could not identify family member columns for verification. Found: {male_col}, {female_col}, {total_col}")

# Age Range Check
age_col = next((c for c in df.columns if 'age' in c.lower() and 'menarche' not in c.lower()), None)
if age_col:
    print(f"\nAge Range: {df[age_col].min()} - {df[age_col].max()}")
    if df[age_col].min() < 10 or df[age_col].max() > 19:
        print("WARNING: Age values outside typical adolescent range (10-19).")
    else:
        print("PASS: Age values within expected range.")

print(f"\n--- 2. Outlier Detection (Z-Score > 3) ---")
numeric_cols = ['knowledge_score', 'practice_score', 'per_capita_income']
for col in numeric_cols:
    if col in df.columns:
        data = df[col].dropna()
        z_scores = np.abs(stats.zscore(data))
        outliers = data[z_scores > 3]
        if len(outliers) > 0:
            print(f"WARNING: {col} has {len(outliers)} outliers (Z > 3).")
            print(f"Values: {outliers.values}")
        else:
            print(f"PASS: {col} has no significant outliers.")

print(f"\n--- 3. Confounder Analysis ---")
# Check if Age or Income correlates with Scores
if age_col and 'knowledge_score' in df.columns:
    corr, p = stats.pearsonr(df[age_col], df['knowledge_score'])
    print(f"Correlation Age vs Knowledge: r={corr:.3f}, p={p:.3f}")
    if p < 0.05:
        print("  -> SIGNIFICANT: Age might be a confounder for Knowledge.")

if 'per_capita_income' in df.columns and 'practice_score' in df.columns:
    # Filter for non-null
    temp_df = df.dropna(subset=['per_capita_income', 'practice_score'])
    if len(temp_df) > 2:
        corr, p = stats.pearsonr(temp_df['per_capita_income'], temp_df['practice_score'])
        print(f"Correlation Income vs Practice: r={corr:.3f}, p={p:.3f}")
        if p < 0.05:
            print("  -> SIGNIFICANT: Income might be a confounder for Practice.")

print(f"\n--- 4. Small Group Analysis ---")
maternal_col = next((c for c in df.columns if 'mother' in c.lower() and 'education' in c.lower()), None)
if maternal_col:
    counts = df[maternal_col].value_counts().sort_index()
    print("Group Sizes:")
    print(counts)
    small_groups = counts[counts < 5]
    if len(small_groups) > 0:
        print(f"WARNING: found {len(small_groups)} groups with < 5 samples.")
        print("Recommendation: Merge small groups (e.g., Levels 3,4,5).")

