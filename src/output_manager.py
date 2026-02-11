"""
Output Management Module

This module handles all file output operations including:
- Creating output directories with timestamps
- Saving DataFrames to CSV files
- Managing file naming to prevent overwrites
- Generating file inventories

Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6
"""

import os
from datetime import datetime
from pathlib import Path
import pandas as pd
from typing import Optional


def create_output_folder(base_path: str = "output") -> str:
    """
    Create an output folder with timestamp to organize analysis results.
    
    If the base_path doesn't exist, it will be created. The function ensures
    the output directory exists before any files are written.
    
    Args:
        base_path: Base directory path for outputs (default: "output")
        
    Returns:
        str: Full path to the created output folder
        
    Raises:
        OSError: If directory creation fails due to permissions or disk issues
        
    Requirements: 8.1
    """
    # Create base path if it doesn't exist
    base_dir = Path(base_path)
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate timestamp for unique folder naming
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_folder = base_dir / f"analysis_{timestamp}"
    
    # Create the timestamped output folder
    output_folder.mkdir(parents=True, exist_ok=True)
    
    return str(output_folder)


def save_dataframe(df: pd.DataFrame, filename: str, output_folder: str, 
                   add_timestamp: bool = False) -> str:
    """
    Save a DataFrame to CSV format in the specified output folder.
    
    Args:
        df: DataFrame to save
        filename: Base filename (with or without .csv extension)
        output_folder: Directory where file should be saved
        add_timestamp: If True, append timestamp to filename to prevent overwrites
        
    Returns:
        str: Full path to the saved file
        
    Raises:
        OSError: If file write fails due to permissions or disk space
        
    Requirements: 8.2, 8.6
    """
    # Ensure filename has .csv extension
    if not filename.endswith('.csv'):
        filename = f"{filename}.csv"
    
    # Add timestamp suffix if requested to prevent overwriting
    if add_timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = filename.replace('.csv', '')
        filename = f"{base_name}_{timestamp}.csv"
    
    # Construct full file path
    output_path = Path(output_folder) / filename
    
    # Save DataFrame to CSV
    df.to_csv(output_path, index=False)
    
    return str(output_path)


def generate_file_inventory(output_folder: str, 
                           file_descriptions: Optional[dict] = None) -> str:
    """
    Generate an inventory document listing all files in the output folder.
    
    Creates a markdown file that lists all output files with their descriptions,
    making it easy for researchers to understand what each file contains.
    
    Args:
        output_folder: Directory containing output files
        file_descriptions: Optional dictionary mapping filenames to descriptions
        
    Returns:
        str: Path to the generated inventory file
        
    Requirements: 8.5
    """
    output_path = Path(output_folder)
    
    # Get all files in the output folder
    files = sorted([f for f in output_path.iterdir() if f.is_file()])
    
    # Create inventory content
    inventory_lines = [
        "# Analysis Output File Inventory",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Output Folder: {output_folder}",
        "",
        "## Files",
        ""
    ]
    
    # List each file with description if available
    for file_path in files:
        filename = file_path.name
        
        # Skip the inventory file itself
        if filename == "FILE_INVENTORY.md":
            continue
            
        # Get file size
        file_size = file_path.stat().st_size
        size_kb = file_size / 1024
        
        # Add file entry
        inventory_lines.append(f"### {filename}")
        inventory_lines.append(f"- **Size**: {size_kb:.2f} KB")
        
        # Add description if provided
        if file_descriptions and filename in file_descriptions:
            inventory_lines.append(f"- **Description**: {file_descriptions[filename]}")
        
        inventory_lines.append("")
    
    # Write inventory file
    inventory_path = output_path / "FILE_INVENTORY.md"
    with open(inventory_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(inventory_lines))
    
    return str(inventory_path)


def get_timestamped_filename(base_filename: str) -> str:
    """
    Generate a filename with timestamp suffix to prevent overwrites.
    
    Helper function to create unique filenames by appending timestamps.
    
    Args:
        base_filename: Original filename (with or without extension)
        
    Returns:
        str: Filename with timestamp suffix
        
    Requirements: 8.6
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Split filename and extension
    if '.' in base_filename:
        name_parts = base_filename.rsplit('.', 1)
        return f"{name_parts[0]}_{timestamp}.{name_parts[1]}"
    else:
        return f"{base_filename}_{timestamp}"


def save_text_file(content: str, filename: str, output_folder: str,
                   add_timestamp: bool = False) -> str:
    """
    Save text content to a file in the output folder.
    
    Useful for saving reports, logs, and other text-based outputs.
    
    Args:
        content: Text content to save
        filename: Base filename
        output_folder: Directory where file should be saved
        add_timestamp: If True, append timestamp to filename
        
    Returns:
        str: Full path to the saved file
        
    Requirements: 8.3, 8.4, 8.6
    """
    # Add timestamp suffix if requested
    if add_timestamp:
        filename = get_timestamped_filename(filename)
    
    # Construct full file path
    output_path = Path(output_folder) / filename
    
    # Write content to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return str(output_path)
