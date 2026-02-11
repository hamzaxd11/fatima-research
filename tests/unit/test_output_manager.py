"""
Unit tests for output_manager module

Tests basic functionality of output management functions.
"""

import os
import tempfile
import shutil
import pandas as pd
from pathlib import Path
from src.output_manager import (
    create_output_folder,
    save_dataframe,
    generate_file_inventory,
    get_timestamped_filename,
    save_text_file
)


def test_create_output_folder():
    """Test that output folder is created successfully."""
    with tempfile.TemporaryDirectory() as temp_dir:
        output_folder = create_output_folder(temp_dir)
        
        # Verify folder exists
        assert os.path.exists(output_folder), "Output folder was not created"
        assert os.path.isdir(output_folder), "Output path is not a directory"
        
        # Verify folder name contains timestamp pattern
        folder_name = os.path.basename(output_folder)
        assert folder_name.startswith("analysis_"), "Folder name doesn't start with 'analysis_'"
        
        print(f"✓ Output folder created: {output_folder}")


def test_save_dataframe():
    """Test saving DataFrame to CSV."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create sample DataFrame
        df = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        })
        
        # Save without timestamp
        file_path = save_dataframe(df, "test_data.csv", temp_dir, add_timestamp=False)
        
        # Verify file exists
        assert os.path.exists(file_path), "CSV file was not created"
        
        # Verify content
        loaded_df = pd.read_csv(file_path)
        assert len(loaded_df) == 3, "DataFrame row count mismatch"
        assert list(loaded_df.columns) == ['col1', 'col2'], "Column names mismatch"
        
        print(f"✓ DataFrame saved successfully: {file_path}")


def test_save_dataframe_with_timestamp():
    """Test saving DataFrame with timestamp to prevent overwrites."""
    with tempfile.TemporaryDirectory() as temp_dir:
        df = pd.DataFrame({'col1': [1, 2, 3]})
        
        # Save with timestamp
        file_path = save_dataframe(df, "test_data.csv", temp_dir, add_timestamp=True)
        
        # Verify file exists and has timestamp in name
        assert os.path.exists(file_path), "CSV file was not created"
        filename = os.path.basename(file_path)
        assert "test_data_" in filename, "Timestamp not added to filename"
        assert filename.endswith(".csv"), "File doesn't have .csv extension"
        
        print(f"✓ DataFrame saved with timestamp: {file_path}")


def test_generate_file_inventory():
    """Test file inventory generation."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create some test files
        Path(temp_dir, "file1.csv").write_text("test1")
        Path(temp_dir, "file2.png").write_text("test2")
        
        # Generate inventory
        file_descriptions = {
            "file1.csv": "Test CSV file",
            "file2.png": "Test PNG file"
        }
        inventory_path = generate_file_inventory(temp_dir, file_descriptions)
        
        # Verify inventory file exists
        assert os.path.exists(inventory_path), "Inventory file was not created"
        
        # Verify content
        with open(inventory_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "Analysis Output File Inventory" in content, "Missing inventory header"
        assert "file1.csv" in content, "file1.csv not listed in inventory"
        assert "file2.png" in content, "file2.png not listed in inventory"
        assert "Test CSV file" in content, "Description for file1.csv missing"
        
        print(f"✓ File inventory generated: {inventory_path}")


def test_get_timestamped_filename():
    """Test timestamped filename generation."""
    # Test with extension
    result = get_timestamped_filename("test.csv")
    assert result.startswith("test_"), "Filename doesn't start with base name"
    assert result.endswith(".csv"), "Extension not preserved"
    
    # Test without extension
    result = get_timestamped_filename("test")
    assert result.startswith("test_"), "Filename doesn't start with base name"
    
    print("✓ Timestamped filename generation works")


def test_save_text_file():
    """Test saving text content to file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        content = "This is a test report.\nLine 2.\nLine 3."
        
        # Save without timestamp
        file_path = save_text_file(content, "report.txt", temp_dir, add_timestamp=False)
        
        # Verify file exists
        assert os.path.exists(file_path), "Text file was not created"
        
        # Verify content
        with open(file_path, 'r', encoding='utf-8') as f:
            loaded_content = f.read()
        
        assert loaded_content == content, "File content doesn't match"
        
        print(f"✓ Text file saved successfully: {file_path}")


if __name__ == '__main__':
    print("Running output_manager tests...")
    print("=" * 80)
    
    test_create_output_folder()
    test_save_dataframe()
    test_save_dataframe_with_timestamp()
    test_generate_file_inventory()
    test_get_timestamped_filename()
    test_save_text_file()
    
    print("=" * 80)
    print("✓ All output_manager tests passed!")
