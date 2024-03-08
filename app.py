from flask import Flask, render_template, request, Response

from receipt import ImageInfo, ReceiptQueue

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("usage.jinja")

@app.get("/receipts-frame")
def receipts_frame():
    """
    Return the last 50 receipts in the queue.
    """
    return render_template("receipts-subwindow.jinja", receipts_info=ReceiptQueue.get_receipts())

@app.get("/receipts")
def receipts():
    return render_template("receipts.jinja")


@app.post("/cgi-bin/epos/service.cgi")
def epos_print():
    """
    Simulate the ePOS print route. This is called by Odoo PoS customers when they print a receipt.
    It receives the receipt and adds it to the queue.
    """
    ReceiptQueue.add_receipt_to_queue(ImageInfo.ImageInfo(request.data))
    return Response(
        '<response xmlns="http://www.epson-pos.com/schemas/2011/03/epos-print" success="true" code="dummy-simulated-epos-printer" />',
        mimetype="text/xml",
        headers={"Access-Control-Allow-Origin": "*"}
    )

