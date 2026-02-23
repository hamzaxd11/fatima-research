from pathlib import Path
import os
import glob
import pandas as pd
import numpy as np

ROOT_DIR = Path(__file__).resolve().parents[2]

output_dirs = [ROOT_DIR / 'output_verify', ROOT_DIR / 'output']
list_of_files = []
for out_dir in output_dirs:
    if os.path.exists(out_dir):
        list_of_files.extend(glob.glob(os.path.join(str(out_dir), 'analysis_*')))

latest_folder = max(list_of_files, key=os.path.getctime)
csv_path = os.path.join(latest_folder, 'scored_dataset.csv')
print(f"Reading: {csv_path}")

df = pd.read_csv(csv_path)

print(f"Total Rows: {len(df)}")
print(f"Overall Mean Knowledge: {df['knowledge_score'].mean():.4f}")

# Filter out rows where MotherEducation is missing
valid_df = df.dropna(subset=['MotherEducation'])
print(f"Valid Rows (with MotherEducation): {len(valid_df)}")
print(f"Valid Mean Knowledge: {valid_df['knowledge_score'].mean():.4f}")

# Calculate weighted difference
expected_mean = valid_df['knowledge_score'].mean()
actual_mean = df['knowledge_score'].mean()

print(f"\nDifference: {expected_mean - actual_mean:.4f}")
if abs(expected_mean - actual_mean) > 0.5:
    print("CONFIRMED: Massive skew due to empty rows.")
else:
    print("Skew is minimal.")
