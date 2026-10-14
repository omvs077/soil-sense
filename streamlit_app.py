"""Streamlit Community Cloud Entrypoint for Soil-Sense.

Allows 1-click cloud deployment without specifying custom nested paths.
"""

import sys
from pathlib import Path

# Ensure project root and app directory are on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
APP_DIR = PROJECT_ROOT / "app"

for p in [str(PROJECT_ROOT), str(APP_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from app.app import main
except (ImportError, KeyError):
    import app
    main = app.main

if __name__ == "__main__":
    main()
