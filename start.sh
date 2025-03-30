#!/bin/bash

# Check if .venv directory exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Creating new environment..."

    # Create virtual environment
    python3 -m venv .venv

    # Activate virtual environment
    source .venv/bin/activate

    # Upgrade pip
    python -m pip install --upgrade pip

    # Install poetry
    echo "Installing poetry..."
    pip install poetry

    # Run poetry install
    echo "Installing dependencies with poetry..."
    poetry install

    echo "Setup complete!"
else
    echo "Virtual environment already exists."
    # Activate virtual environment
    source .venv/bin/activate
fi

# Run the bot
echo "Running bot.py..."
python bot.py

# Deactivation will happen automatically when the script ends