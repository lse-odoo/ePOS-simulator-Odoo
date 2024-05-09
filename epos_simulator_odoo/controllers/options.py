
from flask import render_template
from os import kill, getpid
from signal import SIGINT
from threading import Timer

from epos_simulator_odoo import app

@app.get("/options")
def options():
    return render_template("options.jinja")

@app.get('/shutdown')
def shutdown():
    Timer(.1, lambda: kill(getpid(), SIGINT)).start()
    return 'Server shutting down...'
