@echo off
REM Create virtual environment if it doesn't exist
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to create virtual environment
        pause
        exit /b %ERRORLEVEL%
    )
)

REM Activate virtual environment and install requirements
call .venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment
    pause
    exit /b %ERRORLEVEL%
)

echo Installing required packages...
pip install --upgrade pip
pip install openai python-dotenv
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install required packages
    pause
    exit /b %ERRORLEVEL%
)

echo Starting the chatbot...
python openai_chatbot.py

pause
