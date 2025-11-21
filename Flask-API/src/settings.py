"""RagON Settings - Centralized configuration from .env"""
from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from RagON root (parent of Flask-API)
RAGON_ROOT = Path(__file__).parent.parent.parent
ENV_PATH = RAGON_ROOT / ".env"
load_dotenv(ENV_PATH)

# Server settings
PORT = int(os.getenv("PORT", "1411"))
HOST = os.getenv("HOST", "0.0.0.0")

# Paths (no hardcoded defaults - must be set in .env)
DKM_PDF_PATH = os.getenv("DKM_PDF_PATH", "")
if not DKM_PDF_PATH:
    raise ValueError("DKM_PDF_PATH not set in .env")
