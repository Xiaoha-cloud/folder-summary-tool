#!/usr/bin/env python3

import argparse
import os
from pathlib import Path


def inspect_directory(main_folder_path: str) -> None:
    """
    Inspect the contents of a given directory and print information about its structure.
    
    Args:
        main_folder_path (str): Path to the main folder to inspect
    """
    # Convert the input path to an absolute path
    main_path = Path(main_folder_path).resolve()
    
    if not main_path.exists():
        print(f"Error: The path {main_path} does not exist.")
        return
    
    if not main_path.is_dir():
        print(f"Error: {main_path} is not a directory.")
        return
    
    # Get all items in the main folder
    items = list(main_path.iterdir())
    
    # Count direct items in the main folder
    print(f"\nDirect items in {main_path.name}:")
    print(f"Total items: {len(items)}")
    
    # Process subfolders
    print("\nAnalyzing subfolders:")
    for item in items:
        if item.is_dir():
            # Get contents of the subfolder
            subfolder_contents = list(item.iterdir())
            
            if not subfolder_contents:
                print(f"- Empty subfolder found: {item.name}")
            else:
                # Count only files in the subfolder
                file_count = sum(1 for x in subfolder_contents if x.is_file())
                print(f"- Subfolder '{item.name}' contains {file_count} file(s)")


def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description="Inspect and report on directory structure and contents."
    )
    parser.add_argument(
        "path",
        help="Path to the main folder to inspect"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run the inspection
    inspect_directory(args.path)


if __name__ == "__main__":
    main() 