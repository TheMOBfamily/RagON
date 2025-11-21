# Google Drive CRUD Plus

A Python library and CLI tool for Google Drive operations via GNOME gvfs (no API keys required!).

Provides CRUD operations, checksum verification, and search functionality for files on Google Drive mounted through Nautilus.

## Features

- ✅ **No API setup required** - Uses gvfs mount (already logged in via Nautilus)
- 📁 **Full CRUD operations** - Create, Read, Update, Delete files and folders
- 🔐 **Checksum support** - MD5, SHA1, SHA256, SHA512 hashing
- 🔍 **Powerful search** - By name, extension, size, content
- 🚀 **CLI wrapper script** - Can be called from anywhere (absolute paths)
- 📝 **Auto-logging** - All operations logged to `log/debug.log`
- 📦 **Modular design** - Each module < 150 LOC (SOLID principles)
- 🐍 **Isolated venv** - Self-contained Python environment

## Quick Start (CLI)

### 1. Setup Environment

```bash
# Set your Google Drive email (REQUIRED)
export GDRIVE_EMAIL="limpaul.fin@gmail.com"

# Optional: Set log level
export GDRIVE_LOG_LEVEL="DEBUG"  # Default: INFO
```

Add to `~/.bashrc` or `~/.zshrc` to persist:

```bash
echo 'export GDRIVE_EMAIL="limpaul.fin@gmail.com"' >> ~/.bashrc
source ~/.bashrc
```

### 2. Mount Google Drive in Nautilus

1. Open Nautilus file manager
2. Click "Other Locations" in sidebar
3. Find "Google Drive" and click to connect
4. Log in with your Google account

### 3. Use CLI Commands

```bash
# Navigate to tool directory
cd /home/fong/Projects/mini-rag/google-drive-crud-plus

# Or call from anywhere (use absolute path)
/home/fong/Projects/mini-rag/google-drive-crud-plus/Google-Drive-CRUD.sh list

# List files in root
./Google-Drive-CRUD.sh list

# List files in specific folder
./Google-Drive-CRUD.sh list "folder/subfolder"

# Search for PDF files
./Google-Drive-CRUD.sh pdfs

# Search for PDF files in specific folder
./Google-Drive-CRUD.sh pdfs "0ABc5fJDyNr1wUk9PVA/1n0RWhHyNgACVQtcqIilIe1roFjQTvkeB"

# Calculate checksum
./Google-Drive-CRUD.sh checksum "folder/file.pdf"

# Search files by pattern
./Google-Drive-CRUD.sh search "*python*"

# Upload file
./Google-Drive-CRUD.sh upload /tmp/test.pdf "folder/test.pdf"

# Download file
./Google-Drive-CRUD.sh download "folder/test.pdf" /tmp/test.pdf

# Delete file (with confirmation)
./Google-Drive-CRUD.sh delete "folder/test.pdf"

# Delete file (force, no confirmation)
./Google-Drive-CRUD.sh delete "folder/test.pdf" --force
```

### 4. View Logs

All operations are logged to `log/debug.log`:

```bash
# View logs
cat log/debug.log

# Tail logs (follow in real-time)
tail -f log/debug.log

# Search logs
grep "ERROR" log/debug.log
```

## Installation (For Python Development)

### Prerequisites

1. **Ubuntu with GNOME** (or any system with gvfs)
2. **Python 3.8+**
3. **Google Drive mounted in Nautilus**

### Setup Development Environment

```bash
cd google-drive-crud-plus

# Virtual environment already created in ./venv
# No manual setup needed - wrapper script handles it!

# If you want to use Python API directly:
source venv/bin/activate
pip install -e .
```

## Quick Start

### Basic CRUD Operations

```python
from src.config import GDriveConfig
from src.crud import GDriveCRUD

# Configure with your email
config = GDriveConfig(email="your@gmail.com")
crud = GDriveCRUD(config)

# List files
files = crud.list_files()
for file in files:
    print(file.name)

# Upload a file
crud.upload_file("local_file.pdf", "Drive/folder/file.pdf")

# Download a file
crud.download_file("Drive/folder/file.pdf", "local_copy.pdf")

# Delete a file
crud.delete_file("Drive/folder/file.pdf")
```

### Checksum Verification

```python
from src.config import GDriveConfig
from src.checksum import GDriveChecksum

config = GDriveConfig(email="your@gmail.com")
checksum = GDriveChecksum(config)

# Calculate MD5
md5_hash = checksum.md5("folder/file.pdf")
print(f"MD5: {md5_hash}")

# Calculate SHA256
sha256_hash = checksum.sha256("folder/file.pdf")
print(f"SHA256: {sha256_hash}")

# Verify file integrity
is_valid = checksum.verify("folder/file.pdf", expected_hash, algorithm="md5")
print(f"File valid: {is_valid}")

# Compare two files
are_same = checksum.compare_files("file1.pdf", "file2.pdf")
```

### Search Operations

```python
from src.config import GDriveConfig
from src.search import GDriveSearch

config = GDriveConfig(email="your@gmail.com")
search = GDriveSearch(config)

# Search all PDFs
pdf_files = search.pdfs_only()

# Search by name pattern
python_files = search.by_name("*python*", case_sensitive=False)

# Search by size range (10MB to 100MB)
large_files = search.by_size(
    min_size=10 * 1024 * 1024,
    max_size=100 * 1024 * 1024,
)

# Search by extension
txt_files = search.by_extension(".txt")
```

## Project Structure

```
google-drive-crud-plus/
├── src/
│   ├── __init__.py         # Package exports
│   ├── config.py           # Configuration & path detection
│   ├── connection.py       # gvfs/gio connection management
│   ├── crud.py             # CRUD operations
│   ├── checksum.py         # Hash/checksum functions
│   ├── search.py           # Search functionality
│   └── utils.py            # Helper functions
├── examples/
│   ├── basic_crud.py       # CRUD examples
│   ├── checksum_demo.py    # Checksum examples
│   └── search_demo.py      # Search examples
├── tests/
│   └── test_crud.py        # Unit tests
├── README.md               # This file
├── requirements.txt        # Dependencies
└── setup.py                # Package setup
```

## Examples

Run the included examples:

```bash
# Basic CRUD operations
python examples/basic_crud.py

# Checksum calculation
python examples/checksum_demo.py

# Search operations
python examples/search_demo.py
```

**Important**: Update the `email` variable in each example with your Google Drive email.

## How It Works

This library uses **gvfs** (GNOME Virtual File System), which mounts your Google Drive at:

```
/run/user/$UID/gvfs/google-drive:host=gmail.com,user=your@gmail.com
```

When you log in via Nautilus, gvfs creates a FUSE filesystem that allows standard file operations (read, write, copy, delete) to work transparently with Google Drive.

**Advantages:**
- No OAuth setup
- No API quotas
- Works offline (with cached files)
- Integrates with system file manager

## API Reference

### GDriveConfig

```python
config = GDriveConfig(email="your@gmail.com")
config.get_full_path("folder/file.pdf")  # Get absolute path
```

### GDriveConnection

```python
conn = GDriveConnection(config)
conn.is_mounted()      # Check if mounted
conn.mount()           # Mount drive
conn.unmount()         # Unmount drive
conn.list_mounts()     # List all mounts
```

### GDriveCRUD

```python
crud = GDriveCRUD(config)
crud.create_folder("folder")                      # Create folder
crud.upload_file("local.pdf", "drive/file.pdf")   # Upload
crud.download_file("drive/file.pdf", "local.pdf") # Download
crud.read_file("drive/file.pdf")                  # Read content
crud.delete_file("drive/file.pdf")                # Delete
crud.list_files("folder")                         # List directory
crud.file_exists("drive/file.pdf")                # Check existence
```

### GDriveChecksum

```python
checksum = GDriveChecksum(config)
checksum.md5("file.pdf")                          # MD5 hash
checksum.sha256("file.pdf")                       # SHA256 hash
checksum.calculate("file.pdf", algorithm="sha1")  # Custom algorithm
checksum.verify("file.pdf", expected_hash)        # Verify hash
checksum.compare_files("file1.pdf", "file2.pdf")  # Compare files
```

### GDriveSearch

```python
search = GDriveSearch(config)
search.by_name("*pattern*")                       # Name pattern
search.by_extension(".pdf")                       # Extension
search.by_size(min_size=1024, max_size=1048576)   # Size range
search.pdfs_only()                                # All PDFs
search.walk("folder")                             # Walk directory tree
```

## Troubleshooting

### "Google Drive not mounted" error

Make sure you've connected Google Drive in Nautilus:
1. Open Nautilus file manager
2. Click "Other Locations" in sidebar
3. Find "Google Drive" and click to connect
4. Enter your Google credentials

### "Mount path not found" error

Check which Google accounts are mounted:

```bash
ls /run/user/$UID/gvfs/
```

Make sure the email in your config matches the mounted account.

### Permission errors

gvfs mounts use your user permissions. Make sure:
- You're logged into the correct Google account
- You have access to the files/folders you're trying to access

## Design Principles

This library follows clean code principles:

- **KISS** - Keep It Simple, Stupid
- **YAGNI** - You Aren't Gonna Need It
- **DRY** - Don't Repeat Yourself
- **SOLID** - Single responsibility, Open/Closed, etc.
- **Small modules** - Each file < 150 LOC
- **Type hints** - Full type annotation
- **No comments** - Self-documenting code

## Contributing

Contributions welcome! Please:
1. Follow existing code style
2. Keep modules under 150 LOC
3. Add type hints
4. Write tests for new features

## License

MIT License - Free to use and modify.

## Author

**Fong** - Created as part of the `mini-rag` project.

## Related Projects

- [mini-rag](https://github.com/yourusername/mini-rag) - RAG system for PDF documents
- [dkm-knowledgebase-mcp](https://github.com/yourusername/dkm-knowledgebase-mcp) - Knowledge base MCP server

## Acknowledgments

Built with insights from:
- Google Drive gvfs documentation
- Ubuntu Nautilus documentation
- Clean Code principles (Robert C. Martin)
- Systems Analysis and Design (Dennis, Wixom, Roth)
