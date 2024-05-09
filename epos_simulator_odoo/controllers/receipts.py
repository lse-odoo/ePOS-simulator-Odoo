

import base64
from collections import deque
import datetime
from flask import render_template, request, Response
import functools
from io import BytesIO
import re
from typing import List
from PIL import Image

from epos_simulator_odoo import app

_receipt_queue = deque(maxlen=50)


class ImageInfo():
    def __init__(self, receipt_payload: bytes, test: bool=False) -> None:
        self.receive_time = datetime.datetime.now()
        self.image = self._extract_image_from_payload(receipt_payload)
        self.test = test

    def _extract_image_from_payload(self, receipt_payload: bytes) -> Image:
        # TODO: do with 1 regex (as the order is always the same)
        width = int(re.search(b'width="(\d+)"', receipt_payload).group(1))
        height = int(re.search(b'height="(\d+)"', receipt_payload).group(1))

        image_content_base_64 = re.search(b'<image .*?>(.*)</image>', receipt_payload).group(1)
        # TODO: maybe image_content_base_64 can be used to show the image in the browser directly ?

        # Reconvert the received data by something we can interpret
        decoded_string = base64.b64decode(image_content_base_64)
        binary_img = ''.join(format(byte, '08b') for byte in decoded_string)
        data = bytes([255 if b == '0' else 0 for b in binary_img])

        # TODO: check if mode 1 can be used instead of 'L'
        #  https://pillow.readthedocs.io/en/stable/handbook/concepts.html#modes
        return Image.frombytes('L', (width, height), data)

    @functools.cached_property
    def image_base_64(self):
        buff = BytesIO()
        self.image.save(buff, format="JPEG")
        return base64.b64encode(buff.getvalue()).decode('utf-8')

def _add_receipt_to_queue(image_info: ImageInfo) -> None:
    _receipt_queue.append(image_info)

def _get_receipts() -> List[ImageInfo]:
    return list(_receipt_queue)[::-1]

@app.get("/receipts-frame")
def receipts_frame():
    """Return the last 50 receipts in the queue."""
    return render_template("receipts-subwindow.jinja", receipts_info=_get_receipts())

@app.get("/receipts")
def receipts():
    return render_template("receipts.jinja")

@app.post("/cgi-bin/epos/service.cgi")
def epos_print():
    """
    Simulate the ePOS print route. This is called by Odoo PoS customers when they print a receipt.
    It receives the receipt and adds it to the queue.
    """
    receipt_data = request.data or bytes(request.form.get('\n        \n        <s:Envelope xmlns:s'), 'utf-8')
    _add_receipt_to_queue(ImageInfo(receipt_data))
    return Response(
        '<response xmlns="http://www.epson-pos.com/schemas/2011/03/epos-print" success="true" code="dummy-simulated-epos-printer" />',
        mimetype="text/xml",
        headers={"Access-Control-Allow-Origin": "*"}
    )
