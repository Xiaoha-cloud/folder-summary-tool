# Folder Summary Tool

A Python tool for analyzing and summarizing folder contents.

## Description

This tool helps you analyze and summarize the contents of folders. It provides information about:
- Total number of items in the main folder
- Empty subfolders
- Number of files in non-empty subfolders

## Installation

No additional dependencies required. Just clone the repository:

```bash
git clone https://github.com/Xiaoha-cloud/folder-summary-tool.git
cd folder-summary-tool
```

## Usage

Run the script with a path to the folder you want to analyze:

```bash
./folder_inspector.py /path/to/folder
```

Example output:
```
Direct items in target_folder:
Total items: 4

Analyzing subfolders:
- Empty subfolder found: empty_folder
- Subfolder 'data' contains 2 file(s)
```

## Features

- Counts direct items in the main folder
- Identifies empty subfolders
- Counts files in non-empty subfolders
- Works with relative or absolute paths
- Uses only standard Python libraries

## License

MIT 