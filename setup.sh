#!/bin/bash

function exit_on_error {
  echo "ERROR: $1"
  notify-send -a "EPOS Simulator Odoo" -u critical -i error "Setup Error" "$1"
  exit 1
}

if [ -d "venv" ]; then
  exit_on_error "Already setup. Please remove the venv directory if you want to re-run setup.sh"
fi

if ! hash python3; then
    exit_on_error "python3 is not installed"
fi

pythonminorversion=$(python3 -c 'import sys; print(sys.version_info[1])')
if (( $pythonminorversion < 8 )); then 
    exit_on_error "Python version 3.8 or higher is required current: $(python3 --version)"
fi

echo "Creating virtual environment..."
python3 -m venv venv

if [ ! -d venv]; then
  exit_on_error "The virtual environment was not created successfully"
fi

. venv/bin/activate

echo "Upgrading pip..."
python3 -m pip install --upgrade pip

echo "Installing requirements..."
python3 -m pip install -r requirements.txt

echo "Installing epos_simulator_odoo package..."
python3 -m pip install -e .

echo
echo "Setup complete!"
