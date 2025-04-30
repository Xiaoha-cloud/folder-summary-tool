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
pip install -r requirements.txt
```

## Usage

### Basic Version
For small to medium-sized directories:
```bash
./folder_inspector.py /path/to/folder
```

### Async Version
For large directories with better performance:
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

## Example Output

```
Direct items in target_folder:
Total items: 4
Files: 2
Directories: 2
Symbolic links: 0

Analyzing subfolders:
- Empty subfolder found: empty_folder
- Subfolder 'data' contains 2 file(s)
```

With verbose mode:
```
Direct items in target_folder:
Total items: 4
Files: 2
Directories: 2
Symbolic links: 0

Analyzing subfolders:
- Empty subfolder found: empty_folder
- Subfolder 'data' contains 2 file(s)
  Details:
  - Files: 2
  - Directories: 0
  - Symbolic links: 0
```

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