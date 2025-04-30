# Folder Summary Tool

A Python tool for analyzing and summarizing folder contents, with robust error handling and performance optimizations.

## Description

This tool helps you analyze and summarize the contents of folders. It provides detailed information about:
- Total number of items in the main folder
- Empty subfolders
- Number of files in non-empty subfolders
- Special file types and symbolic links
- Detailed error reporting

## Features

### Robust Error Handling
- **Permission Issues**: Gracefully handles permission errors for both main folder and subfolders
- **Path Handling**: 
  - Supports both relative and absolute paths
  - Handles symbolic links with target information
  - Manages special characters in paths
- **File System Compatibility**:
  - Cross-platform path handling
  - Support for special file types (devices, sockets, etc.)
  - Proper encoding handling
- **Performance Optimizations**:
  - Asynchronous processing for large directories
  - Progress bar for long operations
  - Memory-efficient processing
- **Edge Cases**:
  - Empty folder detection
  - Circular symlink handling
  - Special character support
  - Long path handling

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Xiaoha-cloud/folder-summary-tool.git
cd folder-summary-tool
```

2. Install dependencies:
```bash
# For basic version (no additional dependencies required)
# For async version with progress bar:
pip install -r requirements.txt
```

## Usage

### Basic Version
For small to medium-sized directories. No additional dependencies required:
```bash
./folder_inspector.py /path/to/folder
```

### Async Version
For large directories with better performance. Requires additional dependencies (see Installation):
```bash
./folder_inspector_async.py /path/to/folder
```

### Verbose Mode
To see detailed information about each subfolder:
```bash
./folder_inspector.py /path/to/folder -v
# or
./folder_inspector_async.py /path/to/folder -v
```

### Example Directory Structure
To test the script, you can create a directory with the following structure:
```
test_folder/
├── file1.txt
├── file2.txt
├── empty_folder/
└── data/
    ├── file3.txt
    └── file4.txt
```

You can create this structure using:
```bash
mkdir -p test_folder/empty_folder test_folder/data
touch test_folder/file1.txt test_folder/file2.txt
touch test_folder/data/file3.txt test_folder/data/file4.txt
```

Then run the script:
```bash
./folder_inspector.py test_folder
```

Expected output:
```
Direct items in test_folder:
Total items: 4
Files: 2
Directories: 2
Symbolic links: 0

Analyzing subfolders:
- Empty subfolder found: empty_folder
- Subfolder 'data' contains 2 file(s)
```

## Test Results

### Test Directory Structure
The test directory (`test_folder`) contains:
```
test_folder/
├── file1.txt
├── file2.txt
├── empty_folder/
└── data_folder/
    ├── file3.txt
    └── file4.txt
```

### Test Results

#### Basic Version (folder_inspector.py)
```
Direct items in test_folder:
Total items: 4
Files: 2
Directories: 2
Symbolic links: 0

Analyzing subfolders:
- Subfolder 'data_folder' contains 2 file(s)
- Empty subfolder found: empty_folder
```

#### Async Version (folder_inspector_async.py)
```
Analyzing directory structure...

Direct items in test_folder:
Total items: 4
Files: 2
Directories: 2
Symbolic links: 0

Analyzing subfolders:
- Subfolder 'data_folder' contains 2 file(s)
- Empty subfolder found: empty_folder
```

Both versions successfully:
1. Counted the total number of items in the main folder (4 items)
2. Identified the empty subfolder (empty_folder)
3. Counted files in the non-empty subfolder (data_folder contains 2 files)
4. Correctly identified the two text files in the main folder

## Version Comparison

| Feature | Basic Version | Async Version |
|---------|--------------|---------------|
| Dependencies | None | tqdm |
| Progress Bar | No | Yes |
| Performance | Good for small directories | Better for large directories |
| Memory Usage | Standard | Optimized |
| Installation | No setup required | Requires pip install |

## Implementation Details

### Error Handling
- **Permission Errors**: The tool catches and reports permission errors at both folder and subfolder levels
- **Path Resolution**: Uses `Path.resolve(strict=False)` to handle invalid paths gracefully
- **Exception Handling**: Comprehensive try-except blocks to catch and report various filesystem errors

### Path Processing
- **Cross-Platform**: Uses `pathlib.Path` for consistent path handling across operating systems
- **Symbolic Links**: Detects and reports broken links, with target information
- **Special Characters**: Handles paths with special characters through proper encoding

### File System Features
- **Path Separators**: Automatically handles different path separators (`/` vs `\`)
- **Special Files**: Identifies and reports special file types (devices, sockets, etc.)
- **Encoding**: Handles filesystem encoding issues through proper error catching

### Performance
- **Async Processing**: Uses `asyncio` for concurrent processing of subfolders
- **Progress Tracking**: Implements progress bars for long operations
- **Memory Efficiency**: Processes directories incrementally to minimize memory usage

### Edge Cases
- **Empty Folders**: Explicitly detects and reports empty subfolders
- **Circular Links**: Handles circular symbolic links through proper error catching
- **Special Characters**: Supports filenames with special characters
- **Long Paths**: Handles paths exceeding system limits through proper error handling

## License

MIT 