@echo off
echo Starting AVIATRAX Backend Server...
echo Server will be available at: http://localhost:5000
echo API endpoints available at: http://localhost:5000/api
echo Press Ctrl+C to stop the server
echo ----------------------------------------

cd /d "%~dp0"

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Please create one first.
    echo Run: python -m venv venv
    echo Then: venv\Scripts\activate.bat
    pause
    exit /b 1
)

REM Install requirements if needed
echo Installing/updating requirements...
pip install -r requirements.txt

REM Start the server
echo Starting Flask server...
python start_server.py

pause
