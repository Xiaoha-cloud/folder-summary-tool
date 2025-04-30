#!/usr/bin/env python3

import argparse
import os
from pathlib import Path
from typing import Dict, List, Tuple


def get_item_type(path: Path) -> str:
    """
    Determine the type of a filesystem item.
    
    Args:
        path (Path): Path to the item
        
    Returns:
        str: Type of the item ('file', 'directory', 'symlink', or 'unknown')
    """
    if path.is_symlink():
        return "symlink"
    elif path.is_file():
        return "file"
    elif path.is_dir():
        return "directory"
    return "unknown"


def count_items_by_type(items: List[Path]) -> Dict[str, int]:
    """
    Count items by their type.
    
    Args:
        items (List[Path]): List of paths to count
        
    Returns:
        Dict[str, int]: Count of each item type
    """
    counts = {"file": 0, "directory": 0, "symlink": 0, "unknown": 0}
    for item in items:
        item_type = get_item_type(item)
        counts[item_type] += 1
    return counts


def inspect_directory(main_folder_path: str) -> None:
    """
    Inspect the contents of a given directory and print information about its structure.
    
    Args:
        main_folder_path (str): Path to the main folder to inspect
    """
    try:
        # Convert the input path to an absolute path
        main_path = Path(main_folder_path).resolve()
        
        if not main_path.exists():
            print(f"Error: The path {main_path} does not exist.")
            return
        
        if not main_path.is_dir():
            print(f"Error: {main_path} is not a directory.")
            return
        
        # Get all items in the main folder
        try:
            items = list(main_path.iterdir())
        except PermissionError:
            print(f"Error: Permission denied to read {main_path}")
            return
        
        # Count items by type in the main folder
        counts = count_items_by_type(items)
        
        # Print summary of main folder
        print(f"\nDirect items in {main_path.name}:")
        print(f"Total items: {len(items)}")
        print(f"Files: {counts['file']}")
        print(f"Directories: {counts['directory']}")
        if counts['symlink'] > 0:
            print(f"Symbolic links: {counts['symlink']}")
        if counts['unknown'] > 0:
            print(f"Unknown items: {counts['unknown']}")
        
        # Process subfolders
        print("\nAnalyzing subfolders:")
        for item in items:
            if item.is_dir():
                try:
                    # Get contents of the subfolder
                    subfolder_contents = list(item.iterdir())
                    
                    if not subfolder_contents:
                        print(f"- Empty subfolder found: {item.name}")
                    else:
                        # Count only files in the subfolder
                        file_count = sum(1 for x in subfolder_contents if x.is_file())
                        print(f"- Subfolder '{item.name}' contains {file_count} file(s)")
                except PermissionError:
                    print(f"- Warning: Permission denied to read subfolder '{item.name}'")
                except Exception as e:
                    print(f"- Warning: Error processing subfolder '{item.name}': {e}")

    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")


def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description="Inspect and report on directory structure and contents."
    )
    parser.add_argument(
        "path",
        help="Path to the main folder to inspect"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show more detailed information"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run the inspection
    inspect_directory(args.path)


if __name__ == "__main__":
    main() 