"""Streamlit Community Cloud Entrypoint for Soil-Sense.

Allows 1-click cloud deployment without specifying custom nested paths.
"""

import sys
from pathlib import Path

# Ensure project root is at head of sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.app import main

if __name__ == "__main__":
    main()
