from flask import render_template

from epos_simulator_odoo import app

@app.route("/")
def home():
    return render_template("usage.jinja")
