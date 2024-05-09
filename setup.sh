#!/bin/bash

if [ -d ".venv" ]; then
  echo "ERROR: Already setup. Please remove the venv directory if you want to re-run setup.sh"
  exit 1
fi

if ! hash python3; then
    echo "ERROR: python3 is not installed"
    exit 1
fi

pythonversion=$(python3 --version 2>&1 | grep -Po '(?<=Python )(.+)')
if [[ "$pythonversion" < "3.8" ]]; then # TODO: fix will consider 3.10 < 3.8 (as string comparison)
    echo "ERROR: Python version 3.8 or higher is required current: $pythonversion"
    exit 1
fi

echo "Creating virtual environment..."
python3 -m venv venv
. venv/bin/activate

echo "Upgrading pip..."
python3 -m pip install --upgrade pip

echo "Installing requirements..."
python3 -m pip install -r requirements.txt

echo "Installing epos_simulator_odoo package..."
python3 -m pip install -e .

echo
echo "Setup complete!"
