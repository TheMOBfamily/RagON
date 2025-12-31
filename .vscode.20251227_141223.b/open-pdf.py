#!/usr/bin/env python3
"""Open PDF file with Evince."""
import subprocess
import sys
import os

if len(sys.argv) < 2:
    print("Usage: open-pdf.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]
os.environ['DISPLAY'] = ':0'

# Use setsid -f to fully detach from process group
subprocess.run(
    ['setsid', '-f', 'evince', file_path],
    env=os.environ,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

print(f"✅ Opened PDF: {file_path}")
