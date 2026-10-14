"""Streamlit Community Cloud Entrypoint for Soil-Sense."""

import sys
from pathlib import Path
import streamlit as st

# Configure wide layout as first command in the main script on EVERY run/refresh
try:
    st.set_page_config(
        page_title="Soil-Sense | Precision Soil Fertility ML",
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
except Exception:
    pass

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.dashboard import main

if __name__ == "__main__":
    main()
