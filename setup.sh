#!/bin/bash

# Specify the Python version
PYTHON_VERSION="3.9.12"

# Create a virtual environment
python$PYTHON_VERSION -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip to the latest version
pip install --upgrade pip

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate

echo "Virtual environment created and dependencies installed."
