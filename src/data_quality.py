"""
Data Quality Module

This module provides functions for detecting and reporting data quality issues
including missing values, invalid values, and other data anomalies.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import warnings


def detect_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect and report missing values in the dataset.
    
    Args:
        df: DataFrame to check for missing values
        
    Returns:
        DataFrame with columns: row_number, variable_name, issue_type
        containing all missing value locations
        
    Requirements: 1.2, 12.1, 12.2
    """
    missing_records = []
    
    for col in df.columns:
        # Find rows with missing values in this column
        missing_mask = df[col].isna()
        missing_indices = df.index[missing_mask].tolist()
        
        for idx in missing_indices:
            missing_records.append({
                'row_number': idx + 1,  # 1-based row numbering for user readability
                'variable_name': col,
                'issue_type': 'Missing Value',
                'current_value': 'NaN',
                'details': f'Missing value in column "{col}"'
            })
    
    if missing_records:
        return pd.DataFrame(missing_records)
    else:
        return pd.DataFrame(columns=['row_number', 'variable_name', 'issue_type', 'current_value', 'details'])


def detect_invalid_values(df: pd.DataFrame, validation_rules: Optional[Dict[str, Dict[str, Any]]] = None) -> pd.DataFrame:
    """
    Detect and flag invalid values based on validation rules.
    
    Validation rules define expected ranges and valid values for each column.
    Default rules check for common issues like negative values in numeric columns
    that should be positive (age, income, family size, scores).
    
    Args:
        df: DataFrame to check for invalid values
        validation_rules: Dictionary mapping column names to validation rules.
                         Each rule can specify:
                         - 'min': minimum valid value
                         - 'max': maximum valid value
                         - 'valid_values': list of valid discrete values
                         - 'type': expected data type
        
    Returns:
        DataFrame with columns: row_number, variable_name, issue_type, current_value, details
        containing all invalid value locations
        
    Requirements: 1.2, 12.2, 12.3
    """
    invalid_records = []
    
    # Default validation rules if none provided
    if validation_rules is None:
        validation_rules = _get_default_validation_rules(df)
    
    for col, rules in validation_rules.items():
        if col not in df.columns:
            continue
        
        col_data = df[col]
        
        # Check minimum value constraint
        if 'min' in rules:
            min_val = rules['min']
            invalid_mask = (col_data.notna()) & (pd.to_numeric(col_data, errors='coerce') < min_val)
            invalid_indices = df.index[invalid_mask].tolist()
            
            for idx in invalid_indices:
                invalid_records.append({
                    'row_number': idx + 1,
                    'variable_name': col,
                    'issue_type': 'Out of Range (Below Minimum)',
                    'current_value': str(col_data.iloc[idx]),
                    'details': f'Value {col_data.iloc[idx]} is below minimum {min_val}'
                })
        
        # Check maximum value constraint
        if 'max' in rules:
            max_val = rules['max']
            invalid_mask = (col_data.notna()) & (pd.to_numeric(col_data, errors='coerce') > max_val)
            invalid_indices = df.index[invalid_mask].tolist()
            
            for idx in invalid_indices:
                invalid_records.append({
                    'row_number': idx + 1,
                    'variable_name': col,
                    'issue_type': 'Out of Range (Above Maximum)',
                    'current_value': str(col_data.iloc[idx]),
                    'details': f'Value {col_data.iloc[idx]} is above maximum {max_val}'
                })
        
        # Check valid values constraint
        if 'valid_values' in rules:
            valid_vals = rules['valid_values']
            # Convert to numeric for comparison if needed
            numeric_data = pd.to_numeric(col_data, errors='coerce')
            invalid_mask = (col_data.notna()) & (~numeric_data.isin(valid_vals))
            invalid_indices = df.index[invalid_mask].tolist()
            
            for idx in invalid_indices:
                invalid_records.append({
                    'row_number': idx + 1,
                    'variable_name': col,
                    'issue_type': 'Invalid Value',
                    'current_value': str(col_data.iloc[idx]),
                    'details': f'Value {col_data.iloc[idx]} is not in valid set: {valid_vals}'
                })
    
    if invalid_records:
        return pd.DataFrame(invalid_records)
    else:
        return pd.DataFrame(columns=['row_number', 'variable_name', 'issue_type', 'current_value', 'details'])


def _get_default_validation_rules(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """
    Generate default validation rules based on column names and data types.
    
    Args:
        df: DataFrame to generate rules for
        
    Returns:
        Dictionary of validation rules
    """
    rules = {}
    
    # Age-related columns
    age_columns = [col for col in df.columns if 'age' in col.lower()]
    for col in age_columns:
        rules[col] = {'min': 0, 'max': 120}
    
    # Income-related columns
    income_columns = [col for col in df.columns if 'income' in col.lower()]
    for col in income_columns:
        rules[col] = {'min': 0}
    
    # Family member columns
    family_columns = [col for col in df.columns if 'family' in col.lower() and 'member' in col.lower()]
    for col in family_columns:
        rules[col] = {'min': 0, 'max': 100}
    
    # Score columns
    if 'knowledge_score' in df.columns:
        rules['knowledge_score'] = {'min': 0, 'max': 9}
    if 'practice_score' in df.columns:
        rules['practice_score'] = {'min': 0, 'max': 7}
    if 'total_score' in df.columns:
        rules['total_score'] = {'min': 0, 'max': 16}
    
    return rules


def generate_data_quality_report(
    df: pd.DataFrame,
    validation_rules: Optional[Dict[str, Dict[str, Any]]] = None,
    output_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate a comprehensive data quality report.
    
    This function detects missing values, invalid values, and provides summary
    statistics about data quality issues. The report includes row numbers and
    variable names for all identified issues.
    
    Args:
        df: DataFrame to analyze
        validation_rules: Optional custom validation rules
        output_path: Optional path to save the report CSV files
        
    Returns:
        Dictionary containing:
        - 'missing_values': DataFrame with missing value details
        - 'invalid_values': DataFrame with invalid value details
        - 'summary': Dictionary with summary statistics
        - 'warnings': List of warning messages
        
    Requirements: 1.2, 12.1, 12.2, 12.3, 12.5
    """
    warnings_list = []
    
    # Detect missing values
    missing_df = detect_missing_values(df)
    missing_count = len(missing_df)
    
    if missing_count > 0:
        warnings_list.append(f"Found {missing_count} missing values across {missing_df['variable_name'].nunique()} variables")
    
    # Detect invalid values
    invalid_df = detect_invalid_values(df, validation_rules)
    invalid_count = len(invalid_df)
    
    if invalid_count > 0:
        warnings_list.append(f"Found {invalid_count} invalid values across {invalid_df['variable_name'].nunique()} variables")
    
    # Calculate summary statistics
    total_cells = df.shape[0] * df.shape[1]
    total_issues = missing_count + invalid_count
    quality_percentage = ((total_cells - total_issues) / total_cells * 100) if total_cells > 0 else 0
    
    summary = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'total_cells': total_cells,
        'missing_value_count': missing_count,
        'invalid_value_count': invalid_count,
        'total_issues': total_issues,
        'data_quality_percentage': round(quality_percentage, 2),
        'affected_rows': len(set(list(missing_df['row_number']) + list(invalid_df['row_number']))) if total_issues > 0 else 0,
        'affected_columns': len(set(list(missing_df['variable_name']) + list(invalid_df['variable_name']))) if total_issues > 0 else 0
    }
    
    # Save report files if output path provided
    if output_path:
        if missing_count > 0:
            missing_file = f"{output_path}/data_quality_missing_values.csv"
            missing_df.to_csv(missing_file, index=False)
            warnings_list.append(f"Missing values report saved to: {missing_file}")
        
        if invalid_count > 0:
            invalid_file = f"{output_path}/data_quality_invalid_values.csv"
            invalid_df.to_csv(invalid_file, index=False)
            warnings_list.append(f"Invalid values report saved to: {invalid_file}")
        
        # Save summary report
        summary_file = f"{output_path}/data_quality_summary.txt"
        with open(summary_file, 'w') as f:
            f.write("DATA QUALITY REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Total Rows: {summary['total_rows']}\n")
            f.write(f"Total Columns: {summary['total_columns']}\n")
            f.write(f"Total Cells: {summary['total_cells']}\n\n")
            f.write(f"Missing Values: {summary['missing_value_count']}\n")
            f.write(f"Invalid Values: {summary['invalid_value_count']}\n")
            f.write(f"Total Issues: {summary['total_issues']}\n\n")
            f.write(f"Affected Rows: {summary['affected_rows']}\n")
            f.write(f"Affected Columns: {summary['affected_columns']}\n\n")
            f.write(f"Data Quality: {summary['data_quality_percentage']}%\n\n")
            
            if warnings_list:
                f.write("WARNINGS:\n")
                for warning in warnings_list:
                    f.write(f"- {warning}\n")
        
        warnings_list.append(f"Summary report saved to: {summary_file}")
    
    # Emit warnings to console
    for warning in warnings_list:
        warnings.warn(warning)
    
    return {
        'missing_values': missing_df,
        'invalid_values': invalid_df,
        'summary': summary,
        'warnings': warnings_list
    }
