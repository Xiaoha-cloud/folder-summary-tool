#!/usr/bin/env python3

import argparse
import os
from pathlib import Path
from typing import Dict, List, Tuple
import sys


def handle_symlink(path: Path) -> str:
    """
    Handle symbolic link and return its target information.
    
    Args:
        path (Path): Path to the symlink
        
    Returns:
        str: Information about the symlink target
    """
    try:
        target = path.readlink()
        if target.exists():
            return f"-> {target} (exists)"
        return f"-> {target} (broken link)"
    except Exception as e:
        return f"-> (error reading link: {e})"


def get_item_type(path: Path) -> Tuple[str, str]:
    """
    Determine the type of a filesystem item.
    
    Args:
        path (Path): Path to the item
        
    Returns:
        Tuple[str, str]: (Type of the item, Additional information)
    """
    try:
        if path.is_symlink():
            return "symlink", handle_symlink(path)
        elif path.is_file():
            return "file", ""
        elif path.is_dir():
            return "directory", ""
        else:
            # Handle special files (devices, sockets, etc.)
            if path.exists():
                return "special", f"(special file type)"
            return "unknown", "(not accessible)"
    except Exception as e:
        return "error", f"(error: {e})"


def count_items_by_type(items: List[Path]) -> Dict[str, int]:
    """
    Count items by their type.
    
    Args:
        items (List[Path]): List of paths to count
        
    Returns:
        Dict[str, int]: Count of each item type
    """
    counts = {"file": 0, "directory": 0, "symlink": 0, "special": 0, "error": 0}
    for item in items:
        item_type, _ = get_item_type(item)
        counts[item_type] += 1
    return counts


def inspect_directory(main_folder_path: str, verbose: bool = False) -> None:
    """
    Inspect the contents of a given directory and print information about its structure.
    
    Args:
        main_folder_path (str): Path to the main folder to inspect
        verbose (bool): Whether to show detailed information
    """
    try:
        # Convert the input path to an absolute path and handle potential encoding issues
        try:
            main_path = Path(main_folder_path).resolve(strict=False)
        except Exception as e:
            print(f"Error: Invalid path or encoding: {e}")
            return

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
        except Exception as e:
            print(f"Error: Could not read directory contents: {e}")
            return
        
        # Count items by type in the main folder
        counts = count_items_by_type(items)
        
        # Print summary of main folder
        print(f"\nDirect items in {main_path.name}:")
        print(f"Total items: {len(items)}")
        print(f"Files: {counts['file']}")
        print(f"Directories: {counts['directory']}")
        print(f"Symbolic links: {counts['symlink']}")
        if counts['special'] > 0:
            print(f"Special files: {counts['special']}")
        if counts['error'] > 0:
            print(f"Inaccessible items: {counts['error']}")
        
        # Process subfolders
        print("\nAnalyzing subfolders:")
        for item in items:
            item_type, info = get_item_type(item)
            
            if item_type == "directory":
                try:
                    # Get contents of the subfolder
                    subfolder_contents = list(item.iterdir())
                    
                    if not subfolder_contents:
                        print(f"- Empty subfolder found: {item.name}")
                    else:
                        # Count only files in the subfolder
                        file_count = sum(1 for x in subfolder_contents if x.is_file())
                        print(f"- Subfolder '{item.name}' contains {file_count} file(s)")
                        
                        if verbose:
                            subfolder_counts = count_items_by_type(subfolder_contents)
                            print(f"  Details:")
                            print(f"  - Files: {subfolder_counts['file']}")
                            print(f"  - Directories: {subfolder_counts['directory']}")
                            print(f"  - Symbolic links: {subfolder_counts['symlink']}")
                            if subfolder_counts['special'] > 0:
                                print(f"  - Special files: {subfolder_counts['special']}")
                            
                except PermissionError:
                    print(f"- Warning: Permission denied to read subfolder '{item.name}'")
                except Exception as e:
                    print(f"- Warning: Error processing subfolder '{item.name}': {e}")
            elif verbose and item_type == "symlink":
                print(f"- Symbolic link '{item.name}' {info}")

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
    inspect_directory(args.path, args.verbose)


if __name__ == "__main__":
    main() 