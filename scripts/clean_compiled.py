#!/usr/bin/env python3
"""
Clean up compiled Python and Cython files from the project.
This script removes all compiled files while keeping the original .pyx source files.
"""

import os
import shutil
from pathlib import Path

def is_compiled_file(filepath):
    """Check if a file is a compiled file that should be removed."""
    compiled_extensions = {
        # Python compiled files
        '.pyc', '.pyo', '.pyd', '.pyi', '.pyz', '.pywz',
        # Cython compiled files
        '.c', '.cpp', '.h', '.html', '.o', '.so', '.dll', 
        # Other compiled files
        '.exp', '.lib', '.pdb', '.obj'
    }
    return filepath.suffix.lower() in compiled_extensions or filepath.name == '__pycache__'

def clean_compiled_files(root_dir):
    """Recursively remove all compiled files and empty directories."""
    root_path = Path(root_dir).resolve()
    removed_files = 0
    removed_dirs = 0
    
    # Walk through the directory tree
    for current_dir, dirs, files in os.walk(root_path, topdown=False):
        current_path = Path(current_dir)
        
        # Remove compiled files
        for filename in files:
            filepath = current_path / filename
            if is_compiled_file(filepath):
                try:
                    filepath.unlink()
                    print(f"Removed file: {filepath.relative_to(root_path)}")
                    removed_files += 1
                except Exception as e:
                    print(f"Error removing {filepath}: {e}")
        
        # Remove empty __pycache__ directories
        for dirname in dirs:
            dirpath = current_path / dirname
            if dirpath.name == '__pycache__' or dirpath.name == 'build':
                try:
                    shutil.rmtree(dirpath)
                    print(f"Removed directory: {dirpath.relative_to(root_path)}")
                    removed_dirs += 1
                except Exception as e:
                    print(f"Error removing directory {dirpath}: {e}")
    
    # Remove build directory if it exists
    build_dir = root_path / 'build'
    if build_dir.exists():
        try:
            shutil.rmtree(build_dir)
            print(f"Removed build directory: {build_dir.relative_to(root_path)}")
            removed_dirs += 1
        except Exception as e:
            print(f"Error removing build directory: {e}")
    
    print(f"\nCleanup complete. Removed {removed_files} files and {removed_dirs} directories.")

if __name__ == "__main__":
    # Get the parent directory (cybacktrader root)
    cybacktrader_dir = Path(__file__).parent.parent
    print(f"Cleaning compiled files from: {cybacktrader_dir}")
    clean_compiled_files(cybacktrader_dir)
