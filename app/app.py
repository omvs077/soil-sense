"""Soil-Sense Application Runner (Redirects cleanly to streamlit_app.py)."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit_app

if __name__ == "__main__":
    streamlit_app.main()
