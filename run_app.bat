@echo off
REM Soil-Sense Quick Launcher (Zero C: Drive Bloat)
echo ========================================================
echo   Launching Soil-Sense Agritech ML Platform...
echo ========================================================

REM Redirect pip and temp caches to D: to protect C: drive
set TEMP=D:\temp
set TMP=D:\temp

IF NOT EXIST ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found in .venv.
    echo Please run setup first.
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat

echo Starting Streamlit on http://localhost:8501 ...
streamlit run app/app.py
pause
