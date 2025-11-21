#!/usr/bin/env python
"""
Utility functions for console output and helpers

Author: AI Assistant
Date: 2025-10-26
LOC: ~25 (< 100)
"""
from __future__ import annotations
from rich.console import Console
from .config import (
    COLOR_INFO, COLOR_SUCCESS, COLOR_WARNING, COLOR_ERROR, COLOR_HEADER
)

# Global console instance
console = Console()


def print_header(title: str):
    """Print formatted header"""
    console.print(f"\n[bold {COLOR_HEADER}]{title}[/bold {COLOR_HEADER}]")


def print_info(msg: str):
    """Print info message"""
    console.print(f"[{COLOR_INFO}]{msg}[/{COLOR_INFO}]")


def print_success(msg: str):
    """Print success message"""
    console.print(f"[{COLOR_SUCCESS}]{msg}[/{COLOR_SUCCESS}]")


def print_warning(msg: str):
    """Print warning message"""
    console.print(f"[{COLOR_WARNING}]{msg}[/{COLOR_WARNING}]")


def print_error(msg: str):
    """Print error message"""
    console.print(f"[{COLOR_ERROR}]{msg}[/{COLOR_ERROR}]")
