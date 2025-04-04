
@echo off

REM Check if .venv directory exists
if not exist ".venv" (
    echo Virtual environment not found. Creating new environment...

    REM Create virtual environment
    python -m venv .venv

    REM Activate virtual environment
    call .venv\Scripts\activate.bat

    REM Upgrade pip
    python -m pip install --upgrade pip

    REM Install poetry
    echo Installing poetry...
    pip install poetry

    REM Run poetry install
    echo Installing dependencies with poetry...
    poetry install

    echo Setup complete!
) else (
    echo Virtual environment already exists.
    REM Activate virtual environment
    call .venv\Scripts\activate.bat
)

REM Run the bot
echo Running bot.py...
python bot.py