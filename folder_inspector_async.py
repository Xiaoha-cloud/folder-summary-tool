#!/usr/bin/env python3

import argparse
import asyncio
import os
from pathlib import Path
from typing import Dict, List, Tuple
import sys
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


async def get_item_type(path: Path) -> Tuple[str, str]:
    """
    Determine the type of a filesystem item asynchronously.
    """
    loop = asyncio.get_event_loop()
    try:
        if await loop.run_in_executor(None, path.is_symlink):
            target = await loop.run_in_executor(None, path.readlink)
            exists = await loop.run_in_executor(None, target.exists)
            if exists:
                return "symlink", f"-> {target} (exists)"
            return "symlink", f"-> {target} (broken link)"
        elif await loop.run_in_executor(None, path.is_file):
            return "file", ""
        elif await loop.run_in_executor(None, path.is_dir):
            return "directory", ""
        else:
            if await loop.run_in_executor(None, path.exists):
                return "special", "(special file type)"
            return "unknown", "(not accessible)"
    except Exception as e:
        return "error", f"(error: {e})"


async def count_items_by_type(items: List[Path]) -> Dict[str, int]:
    """
    Count items by their type asynchronously.
    """
    counts = {"file": 0, "directory": 0, "symlink": 0, "special": 0, "error": 0}
    for item in items:
        item_type, _ = await get_item_type(item)
        counts[item_type] += 1
    return counts


async def process_subfolder(item: Path, verbose: bool, pbar: tqdm) -> Tuple[str, str, Dict[str, int]]:
    """
    Process a subfolder asynchronously.
    """
    try:
        subfolder_contents = list(item.iterdir())
        if not subfolder_contents:
            result = f"- Empty subfolder found: {item.name}"
            counts = {}
        else:
            file_count = sum(1 for x in subfolder_contents if x.is_file())
            result = f"- Subfolder '{item.name}' contains {file_count} file(s)"
            if verbose:
                counts = await count_items_by_type(subfolder_contents)
            else:
                counts = {}
        return "success", result, counts
    except PermissionError:
        return "error", f"- Warning: Permission denied to read subfolder '{item.name}'", {}
    except Exception as e:
        return "error", f"- Warning: Error processing subfolder '{item.name}': {e}", {}
    finally:
        pbar.update(1)


async def inspect_directory(main_folder_path: str, verbose: bool = False) -> None:
    """
    Inspect the contents of a given directory asynchronously.
    """
    try:
        # Convert the input path to an absolute path
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
        
        print("\nAnalyzing directory structure...")
        
        # Count items by type in the main folder
        counts = await count_items_by_type(items)
        
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
        
        # Process subfolders with progress bar
        directories = [item for item in items if item.is_dir()]
        if directories:
            print("\nAnalyzing subfolders:")
            with tqdm(total=len(directories), desc="Processing subfolders") as pbar:
                tasks = [process_subfolder(item, verbose, pbar) for item in directories]
                results = await asyncio.gather(*tasks)
                
                for status, result, counts in results:
                    print(result)
                    if verbose and status == "success" and counts:
                        print(f"  Details:")
                        print(f"  - Files: {counts.get('file', 0)}")
                        print(f"  - Directories: {counts.get('directory', 0)}")
                        print(f"  - Symbolic links: {counts.get('symlink', 0)}")
                        if counts.get('special', 0) > 0:
                            print(f"  - Special files: {counts['special']}")

    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Asynchronously inspect and report on directory structure and contents."
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
    
    args = parser.parse_args()
    
    # Run the async inspection
    asyncio.run(inspect_directory(args.path, args.verbose))


if __name__ == "__main__":
    main() 