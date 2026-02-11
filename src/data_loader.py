"""
Data loading module for SPSS file processing.

This module provides functions to load SPSS .sav files, validate data structure,
and generate data summaries for the menstrual hygiene analysis system.
"""

import os
from typing import Tuple, List, Dict, Any
import pandas as pd
import pyreadstat


def load_spss_file(file_path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Load an SPSS .sav file and return the data with metadata.
    
    Args:
        file_path: Path to the SPSS .sav file
        
    Returns:
        Tuple containing:
        - DataFrame with the loaded data
        - Dictionary with metadata (column labels, value labels, etc.)
        
    Raises:
        FileNotFoundError: If the file does not exist
        PermissionError: If the file cannot be accessed due to permissions
        Exception: For other read errors (corrupted file, invalid format, etc.)
    """
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"SPSS file not found at path: {file_path}\n"
            f"Please check that the file exists and the path is correct."
        )
    
    # Check if file is readable
    if not os.access(file_path, os.R_OK):
        raise PermissionError(
            f"Permission denied: Cannot read file at path: {file_path}\n"
            f"Please check file permissions."
        )
    
    try:
        # Load SPSS file using pyreadstat
        df, meta = pyreadstat.read_sav(file_path)
        
        # Create metadata dictionary
        metadata = {
            'column_labels': meta.column_names_to_labels if hasattr(meta, 'column_names_to_labels') else {},
            'value_labels': meta.variable_value_labels if hasattr(meta, 'variable_value_labels') else {},
            'column_names': meta.column_names if hasattr(meta, 'column_names') else list(df.columns),
            'number_rows': meta.number_rows if hasattr(meta, 'number_rows') else len(df),
            'number_columns': meta.number_columns if hasattr(meta, 'number_columns') else len(df.columns)
        }
        
        return df, metadata
        
    except PermissionError:
        raise PermissionError(
            f"Permission denied: Cannot read file at path: {file_path}\n"
            f"Please check file permissions."
        )
    except Exception as e:
        # Handle corrupted files, invalid formats, and other read errors
        raise Exception(
            f"Error reading SPSS file at path: {file_path}\n"
            f"Error type: {type(e).__name__}\n"
            f"Error details: {str(e)}\n"
            f"The file may be corrupted or in an invalid format."
        )


def validate_required_columns(df: pd.DataFrame, required_cols: List[str]) -> List[str]:
    """
    Validate that all required columns are present in the DataFrame.
    
    Args:
        df: DataFrame to validate
        required_cols: List of required column names
        
    Returns:
        List of missing column names (empty list if all columns present)
    """
    if df is None or df.empty:
        return required_cols
    
    # Get actual columns in the DataFrame
    actual_cols = set(df.columns)
    required_set = set(required_cols)
    
    # Find missing columns
    missing_cols = list(required_set - actual_cols)
    
    return sorted(missing_cols)


def generate_data_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate a summary of the loaded dataset.
    
    Args:
        df: DataFrame to summarize
        
    Returns:
        Dictionary containing:
        - row_count: Total number of rows
        - column_count: Total number of columns
        - column_names: List of all column names
        - data_types: Dictionary mapping column names to data types
        - missing_value_counts: Dictionary mapping column names to count of missing values
    """
    if df is None or df.empty:
        return {
            'row_count': 0,
            'column_count': 0,
            'column_names': [],
            'data_types': {},
            'missing_value_counts': {}
        }
    
    # Generate summary information
    summary = {
        'row_count': len(df),
        'column_count': len(df.columns),
        'column_names': list(df.columns),
        'data_types': {col: str(dtype) for col, dtype in df.dtypes.items()},
        'missing_value_counts': {col: int(df[col].isna().sum()) for col in df.columns}
    }
    
    return summary
