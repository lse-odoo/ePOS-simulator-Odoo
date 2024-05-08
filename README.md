# ePOS-simulator-Odoo
EPoS simulator to use in Odoo. Will intercept PoS receipts to show their content

## Installation

Create a virtualenv and activate it:
```sh
$ python3 -m venv .venv
$ . .venv/bin/activate
```

Install `epos_simulator_odoo`:
```sh
$ pip install -e .
```

## Run
```sh
$ flask --app flaskr run --cert=adhoc
```
