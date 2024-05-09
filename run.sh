#!/bin/bash


if [ ! -d "venv" ]; then
  echo "ERROR: missing virtual environement. Please make sure that setup.sh was ran first."
  exit 1
fi

. venv/bin/activate

sleep 1 && python3 -m webbrowser https://127.0.0.1:5000 &
flask --app epos_simulator_odoo run --cert=adhoc
