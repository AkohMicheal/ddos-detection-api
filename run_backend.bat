@echo off
echo ===================================================
echo Starting DDoS Anomaly Detection Backend API Server
echo ===================================================
echo.
echo Step 1: Checking and installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install dependencies. Please ensure Python is added to your PATH.
    pause
    exit /b %errorlevel%
)
echo.
echo Step 2: Running FastAPI Server with Uvicorn...
echo Access the interactive API docs at: http://localhost:8000/docs
echo.
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
pause
