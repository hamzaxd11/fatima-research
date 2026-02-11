"""
Visualization Module

This module provides functions for generating charts and graphs to visualize
menstrual hygiene survey data analysis results.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from typing import Optional, List
import warnings
import os


# Configure matplotlib for high-quality output
matplotlib.rcParams['figure.dpi'] = 300
matplotlib.rcParams['savefig.dpi'] = 300
matplotlib.rcParams['savefig.format'] = 'png'
matplotlib.rcParams['font.size'] = 10
matplotlib.rcParams['axes.labelsize'] = 11
matplotlib.rcParams['axes.titlesize'] = 12
matplotlib.rcParams['xtick.labelsize'] = 9
matplotlib.rcParams['ytick.labelsize'] = 9
matplotlib.rcParams['legend.fontsize'] = 9


def _find_column(df: pd.DataFrame, possible_names: List[str]) -> Optional[str]:
    """
    Helper function to find a column by trying multiple possible names.
    
    Args:
        df: DataFrame to search
        possible_names: List of possible column names
        
    Returns:
        Column name if found, None otherwise
    """
    for name in possible_names:
        if name in df.columns:
            return name
    return None


def plot_scores_by_maternal_education(
    df: pd.DataFrame,
    output_path: str,
    filename: str = 'scores_by_maternal_education.png'
) -> None:
    """
    Generate bar chart showing mean knowledge and practice scores by maternal education level.
    
    Creates a grouped bar chart with error bars showing standard deviations.
    Includes axis labels, title, and legend.
    
    Args:
        df: DataFrame with maternal education and score columns
        output_path: Directory path where the chart will be saved
        filename: Name of the output file (default: 'scores_by_maternal_education.png')
        
    Requirements: 7.1, 7.5, 7.6
    """
    # Find maternal education column
    maternal_ed_col = _find_column(df, [
        'mother_education', 'Mother_education', 'MotherEducation',
        'maternal_education', 'Maternal_education'
    ])
    
    if maternal_ed_col is None:
        warnings.warn("Maternal education column not found. Skipping bar chart generation.")
        return
    
    # Check for score columns
    if 'knowledge_score' not in df.columns or 'practice_score' not in df.columns:
        warnings.warn("Score columns not found. Skipping bar chart generation.")
        return
    
    # Prepare data
    analysis_df = df[[maternal_ed_col, 'knowledge_score', 'practice_score']].copy()
    analysis_df = analysis_df.dropna()
    
    if len(analysis_df) == 0:
        warnings.warn("No valid data for bar chart. Skipping generation.")
        return
    
    # Group by maternal education and calculate means and stds
    grouped = analysis_df.groupby(maternal_ed_col)
    means = grouped.agg({
        'knowledge_score': 'mean',
        'practice_score': 'mean'
    })
    stds = grouped.agg({
        'knowledge_score': 'std',
        'practice_score': 'std'
    })
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Set up bar positions
    x = np.arange(len(means))
    width = 0.35
    
    # Create bars
    bars1 = ax.bar(x - width/2, means['knowledge_score'], width,
                   yerr=stds['knowledge_score'], capsize=5,
                   label='Knowledge Score', color='#3498db', alpha=0.8)
    bars2 = ax.bar(x + width/2, means['practice_score'], width,
                   yerr=stds['practice_score'], capsize=5,
                   label='Practice Score', color='#e74c3c', alpha=0.8)
    
    # Customize chart
    ax.set_xlabel('Maternal Education Level', fontweight='bold')
    ax.set_ylabel('Mean Score', fontweight='bold')
    ax.set_title('Knowledge and Practice Scores by Maternal Education Level', fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(means.index, rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Adjust layout and save
    plt.tight_layout()
    full_path = os.path.join(output_path, filename)
    plt.savefig(full_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Bar chart saved to: {full_path}")


def plot_score_distributions(
    df: pd.DataFrame,
    output_path: str,
    filename: str = 'score_distributions.png'
) -> None:
    """
    Generate histograms showing the distribution of knowledge and practice scores.
    
    Creates side-by-side histograms for both score types.
    Includes axis labels, titles, and bin counts.
    
    Args:
        df: DataFrame with score columns
        output_path: Directory path where the chart will be saved
        filename: Name of the output file (default: 'score_distributions.png')
        
    Requirements: 7.2, 7.5, 7.6
    """
    # Check for score columns
    if 'knowledge_score' not in df.columns or 'practice_score' not in df.columns:
        warnings.warn("Score columns not found. Skipping histogram generation.")
        return
    
    # Prepare data
    knowledge_scores = df['knowledge_score'].dropna()
    practice_scores = df['practice_score'].dropna()
    
    if len(knowledge_scores) == 0 and len(practice_scores) == 0:
        warnings.warn("No valid score data for histograms. Skipping generation.")
        return
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Knowledge score histogram
    if len(knowledge_scores) > 0:
        ax1.hist(knowledge_scores, bins=range(0, 11), edgecolor='black',
                color='#3498db', alpha=0.7, align='left')
        ax1.set_xlabel('Knowledge Score', fontweight='bold')
        ax1.set_ylabel('Frequency', fontweight='bold')
        ax1.set_title('Distribution of Knowledge Scores', fontweight='bold', pad=15)
        ax1.set_xticks(range(0, 10))
        ax1.grid(axis='y', alpha=0.3, linestyle='--')
        ax1.axvline(knowledge_scores.mean(), color='red', linestyle='--',
                   linewidth=2, label=f'Mean: {knowledge_scores.mean():.2f}')
        ax1.legend()
    
    # Practice score histogram
    if len(practice_scores) > 0:
        ax2.hist(practice_scores, bins=range(0, 9), edgecolor='black',
                color='#e74c3c', alpha=0.7, align='left')
        ax2.set_xlabel('Practice Score', fontweight='bold')
        ax2.set_ylabel('Frequency', fontweight='bold')
        ax2.set_title('Distribution of Practice Scores', fontweight='bold', pad=15)
        ax2.set_xticks(range(0, 8))
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        ax2.axvline(practice_scores.mean(), color='red', linestyle='--',
                   linewidth=2, label=f'Mean: {practice_scores.mean():.2f}')
        ax2.legend()
    
    # Adjust layout and save
    plt.tight_layout()
    full_path = os.path.join(output_path, filename)
    plt.savefig(full_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Histograms saved to: {full_path}")


def plot_score_boxplots(
    df: pd.DataFrame,
    output_path: str,
    filename: str = 'score_boxplots.png'
) -> None:
    """
    Generate box plots comparing score distributions across maternal education groups.
    
    Creates side-by-side box plots for knowledge and practice scores,
    grouped by maternal education level.
    Includes axis labels, titles, and legends.
    
    Args:
        df: DataFrame with maternal education and score columns
        output_path: Directory path where the chart will be saved
        filename: Name of the output file (default: 'score_boxplots.png')
        
    Requirements: 7.3, 7.5, 7.6
    """
    # Find maternal education column
    maternal_ed_col = _find_column(df, [
        'mother_education', 'Mother_education', 'MotherEducation',
        'maternal_education', 'Maternal_education'
    ])
    
    if maternal_ed_col is None:
        warnings.warn("Maternal education column not found. Skipping box plot generation.")
        return
    
    # Check for score columns
    if 'knowledge_score' not in df.columns or 'practice_score' not in df.columns:
        warnings.warn("Score columns not found. Skipping box plot generation.")
        return
    
    # Prepare data
    analysis_df = df[[maternal_ed_col, 'knowledge_score', 'practice_score']].copy()
    analysis_df = analysis_df.dropna()
    
    if len(analysis_df) == 0:
        warnings.warn("No valid data for box plots. Skipping generation.")
        return
    
    # Get unique education levels
    education_levels = sorted(analysis_df[maternal_ed_col].unique())
    
    # Prepare data for box plots
    knowledge_data = [analysis_df[analysis_df[maternal_ed_col] == level]['knowledge_score'].values
                     for level in education_levels]
    practice_data = [analysis_df[analysis_df[maternal_ed_col] == level]['practice_score'].values
                    for level in education_levels]
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Knowledge score box plot
    bp1 = ax1.boxplot(knowledge_data, labels=education_levels, patch_artist=True)
    for patch in bp1['boxes']:
        patch.set_facecolor('#3498db')
        patch.set_alpha(0.7)
    ax1.set_xlabel('Maternal Education Level', fontweight='bold')
    ax1.set_ylabel('Knowledge Score', fontweight='bold')
    ax1.set_title('Knowledge Scores by Maternal Education', fontweight='bold', pad=15)
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Practice score box plot
    bp2 = ax2.boxplot(practice_data, labels=education_levels, patch_artist=True)
    for patch in bp2['boxes']:
        patch.set_facecolor('#e74c3c')
        patch.set_alpha(0.7)
    ax2.set_xlabel('Maternal Education Level', fontweight='bold')
    ax2.set_ylabel('Practice Score', fontweight='bold')
    ax2.set_title('Practice Scores by Maternal Education', fontweight='bold', pad=15)
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Adjust layout and save
    plt.tight_layout()
    full_path = os.path.join(output_path, filename)
    plt.savefig(full_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Box plots saved to: {full_path}")


def plot_scatter_matrix(
    df: pd.DataFrame,
    output_path: str,
    filename: str = 'scatter_matrix.png'
) -> None:
    """
    Generate scatter plots showing relationships between continuous variables.
    
    Creates a matrix of scatter plots for:
    - Age, income, family size, per capita income
    - Knowledge score, practice score
    
    Includes axis labels and titles.
    
    Args:
        df: DataFrame with continuous variables
        output_path: Directory path where the chart will be saved
        filename: Name of the output file (default: 'scatter_matrix.png')
        
    Requirements: 7.4, 7.5, 7.6
    """
    # Define variables to include in scatter matrix
    var_mappings = {
        'Age': ['age', 'Age'],
        'Income': ['income_per_month', 'Income_per_month', 'IncomePerMonth'],
        'Family Size': ['total_family_members', 'Total_family_members', 'TotalFamilyMembers'],
        'Per Capita Income': ['per_capita_income', 'Per_capita_income', 'PerCapitaIncome'],
        'Knowledge Score': ['knowledge_score'],
        'Practice Score': ['practice_score']
    }
    
    # Find available columns
    available_data = {}
    for var_name, possible_cols in var_mappings.items():
        col = _find_column(df, possible_cols)
        if col:
            data = pd.to_numeric(df[col], errors='coerce')
            if data.notna().sum() > 0:
                available_data[var_name] = data
    
    if len(available_data) < 2:
        warnings.warn("Insufficient continuous variables for scatter matrix. Skipping generation.")
        return
    
    # Create DataFrame with available variables
    scatter_df = pd.DataFrame(available_data).dropna()
    
    if len(scatter_df) < 2:
        warnings.warn("Insufficient data points for scatter matrix. Skipping generation.")
        return
    
    # Determine grid size
    n_vars = len(scatter_df.columns)
    
    # Create figure with subplots
    fig, axes = plt.subplots(n_vars, n_vars, figsize=(12, 12))
    
    # If only 2 variables, axes won't be 2D array
    if n_vars == 2:
        axes = np.array([[axes[0], axes[1]], [axes[2], axes[3]]])
    
    var_names = list(scatter_df.columns)
    
    # Create scatter plots
    for i in range(n_vars):
        for j in range(n_vars):
            ax = axes[i, j] if n_vars > 1 else axes
            
            if i == j:
                # Diagonal: histogram
                ax.hist(scatter_df[var_names[i]], bins=15, edgecolor='black',
                       color='#3498db', alpha=0.7)
                ax.set_ylabel('Frequency', fontsize=8)
            else:
                # Off-diagonal: scatter plot
                ax.scatter(scatter_df[var_names[j]], scatter_df[var_names[i]],
                          alpha=0.5, s=20, color='#2ecc71')
            
            # Set labels
            if i == n_vars - 1:
                ax.set_xlabel(var_names[j], fontsize=8, fontweight='bold')
            else:
                ax.set_xticklabels([])
            
            if j == 0:
                ax.set_ylabel(var_names[i], fontsize=8, fontweight='bold')
            else:
                ax.set_yticklabels([])
            
            # Grid
            ax.grid(alpha=0.2, linestyle='--')
            ax.tick_params(labelsize=7)
    
    # Add overall title
    fig.suptitle('Scatter Matrix of Continuous Variables', fontsize=14, fontweight='bold', y=0.995)
    
    # Adjust layout and save
    plt.tight_layout()
    full_path = os.path.join(output_path, filename)
    plt.savefig(full_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Scatter matrix saved to: {full_path}")


def generate_all_visualizations(
    df: pd.DataFrame,
    output_path: str
) -> None:
    """
    Generate all visualizations for the analysis.
    
    Convenience function that calls all individual plotting functions.
    
    Args:
        df: DataFrame with all required data
        output_path: Directory path where charts will be saved
        
    Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6
    """
    print("\nGenerating visualizations...")
    
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    # Generate each visualization
    try:
        plot_scores_by_maternal_education(df, output_path)
    except Exception as e:
        warnings.warn(f"Failed to generate bar chart: {str(e)}")
    
    try:
        plot_score_distributions(df, output_path)
    except Exception as e:
        warnings.warn(f"Failed to generate histograms: {str(e)}")
    
    try:
        plot_score_boxplots(df, output_path)
    except Exception as e:
        warnings.warn(f"Failed to generate box plots: {str(e)}")
    
    try:
        plot_scatter_matrix(df, output_path)
    except Exception as e:
        warnings.warn(f"Failed to generate scatter matrix: {str(e)}")
    
    print("Visualization generation complete.")
