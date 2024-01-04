# #!/bin/bash

# Specify the Python version
PYTHON_VERSION="3.9.12"

# Create a virtual environment
python3 -m venv venv
echo "Virtual environment created."

# Activate the virtual environment
source venv/bin/activate
echo "Virtual environment activated."

# Upgrade pip to the latest version
pip install --upgrade pip
echo "Pip upgraded."

# Install dependencies from requirements.txt
pip install --no-cache-dir -r requirements.txt
echo "Dependencies installed."

echo "Script completed."
