import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Load the scored dataset
# Using the one from the verification run
# Find the latest analysis folder
import os
import glob

# Find the latest analysis folder
# Try to find the latest analysis folder in output_verify
output_dirs = ['output_verify', 'output']
list_of_files = []

for out_dir in output_dirs:
    if os.path.exists(out_dir):
        # Using glob to find analysis folders
        found = glob.glob(os.path.join(out_dir, 'analysis_*'))
        list_of_files.extend(found)

if not list_of_files:
    # Fallback: try listing directory contents manually if glob fails
    for out_dir in output_dirs:
        if os.path.exists(out_dir):
            for item in os.listdir(out_dir):
                if item.startswith('analysis_'):
                    list_of_files.append(os.path.join(out_dir, item))

if not list_of_files:
    print("No analysis output found in output_verify or output.")
    # Debug info
    print(f"CWD: {os.getcwd()}")
    if os.path.exists('output'):
        print(f"Output contents: {os.listdir('output')}")
    if os.path.exists('output_verify'):
        print(f"Output_verify contents: {os.listdir('output_verify')}")
    exit()

latest_folder = max(list_of_files, key=os.path.getctime)
csv_path = os.path.join(latest_folder, 'scored_dataset.csv')
print(f"Using dataset: {csv_path}")

df = pd.read_csv(csv_path)

# Filter for valid maternal education and scores
# We need to reproduce the exact filtering: non-null maternal education
# Find the column
maternal_col = None
for col in df.columns:
    if 'MotherEducation' in col:
        maternal_col = col
        break

if not maternal_col:
    print("Maternal education column not found.")
    exit()

# Filter data
analysis_df = df.dropna(subset=[maternal_col, 'practice_score'])
analysis_df = analysis_df[analysis_df['practice_score'].notna()]

print(f"Valid N for Practice Score: {len(analysis_df)}")
print(f"Groups: {analysis_df[maternal_col].unique()}")
print(analysis_df[maternal_col].value_counts())

# 1. Normality Check (Shapiro-Wilk)
# ANOVA assumes residuals are normally distributed
print("\n--- Normality Check (Shapiro-Wilk) ---")
# Get residuals from the ANOVA model
model = ols(f'practice_score ~ C({maternal_col})', data=analysis_df).fit()
w, p_norm = stats.shapiro(model.resid)
print(f"Shapiro-Wilk: W={w:.4f}, p={p_norm:.4f}")
if p_norm < 0.05:
    print("WARNING: Residuals are NOT normally distributed (p < 0.05). ANOVA assumption violated.")
else:
    print("Residuals appear normally distributed.")

# 2. Homogeneity of Variance (Levene's Test)
# ANOVA assumes equal variances across groups
print("\n--- Homogeneity of Variance (Levene's Test) ---")
groups = [group['practice_score'].values for name, group in analysis_df.groupby(maternal_col)]
stat, p_levene = stats.levene(*groups)
print(f"Levene's Test: stat={stat:.4f}, p={p_levene:.4f}")
if p_levene < 0.05:
    print("WARNING: Variances are NOT equal (p < 0.05). ANOVA assumption violated.")
else:
    print("Variances appear equal.")

# 3. Effect Size (Eta-Squared)
# How much of the variance in Practice Score is explained by Maternal Education?
print("\n--- Effect Size (Eta-Squared) ---")
aov_table = sm.stats.anova_lm(model, typ=2)
print(aov_table)
ss_between = aov_table['sum_sq'].iloc[0]
ss_total = aov_table['sum_sq'].sum()
eta_sq = ss_between / ss_total
print(f"\nEta-Squared: {eta_sq:.4f}")

# Interpretation of Eta-Squared
if eta_sq < 0.01:
    print("Effect Size: Negligible")
elif eta_sq < 0.06:
    print("Effect Size: Small")
elif eta_sq < 0.14:
    print("Effect Size: Medium")
else:
    print("Effect Size: Large")

# 4. Post-hoc Tests (Tukey HSD)
# Which specific groups are different?
print("\n--- Post-hoc Tests (Tukey HSD) ---")
from statsmodels.stats.multicomp import pairwise_tukeyhsd
tukey = pairwise_tukeyhsd(endog=analysis_df['practice_score'], groups=analysis_df[maternal_col], alpha=0.05)
print(tukey)

# 5. P-Hacking Check (Kruskal-Wallis comparison)
print("\n--- Robustness Check (Kruskal-Wallis) ---")
h_stat, p_kruskal = stats.kruskal(*groups)
print(f"Kruskal-Wallis: H={h_stat:.4f}, p={p_kruskal:.4f}")

if p_kruskal < 0.05:
    print("Result is robust (significant in non-parametric test too).")
else:
    print("WARNING: Result is NOT significant in non-parametric test. ANOVA result might be fragile.")
