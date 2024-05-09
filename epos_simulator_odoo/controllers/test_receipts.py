
from flask import Response
from pathlib import Path
from random import choice

from epos_simulator_odoo import app
from epos_simulator_odoo.controllers.receipts import ImageInfo, _add_receipt_to_queue

@app.get("/test-receipt")
def add_test_receipt():
    receipt_list = Path('epos_simulator_odoo/controllers/receipts_fake/').glob('*.xml')
    with open(choice(tuple(receipt_list)), 'rb') as f:
        _add_receipt_to_queue(ImageInfo(f.read(),  test=True))
    return Response('Test receipt added sucessfully', status=200)
