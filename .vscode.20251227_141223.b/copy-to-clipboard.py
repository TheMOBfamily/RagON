#!/usr/bin/env python3
"""Copy file to system clipboard as URI (for Nautilus paste)."""
import subprocess
import sys
import os

if len(sys.argv) < 2:
    print("Usage: copy-to-clipboard.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]
os.environ['DISPLAY'] = ':0'

# Convert to file URI format
file_uri = f"file://{file_path}\n"

# Use start_new_session to detach from VSCode process group
# This prevents VSCode from killing xclip when task completes
p = subprocess.Popen(
    ['xclip', '-selection', 'clipboard', '-t', 'text/uri-list'],
    stdin=subprocess.PIPE,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    env=os.environ,
    start_new_session=True  # Critical: detach from parent process group
)
p.stdin.write(file_uri.encode())
p.stdin.close()
# Don't wait - let xclip run independently

print(f"✅ Copied file: {file_path}")
