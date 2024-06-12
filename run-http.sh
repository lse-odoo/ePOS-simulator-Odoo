#!/bin/bash


if [ ! -d "venv" ]; then
  echo "ERROR: missing virtual environement. Please make sure that setup.sh was ran first."
  notify-send -a "EPOS Simulator Odoo" -u critical -i error "Run Error" "$1"
  exit 1
fi

. venv/bin/activate

sleep 1 && python3 -m webbrowser http://127.0.0.1:5000 &
flask --app epos_simulator_odoo run
