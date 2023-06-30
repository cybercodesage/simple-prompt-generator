#!/bin/bash

# Check if the virtual environment directory exists
if [ ! -d "./spggui" ]; then
    # Create the virtual environment
    python -m venv spggui
fi

# Activate the virtual environment
source spggui/bin/activate

# Install the requirements
pip install -r requirements.txt

echo "Virtual environment created and requirements installed."