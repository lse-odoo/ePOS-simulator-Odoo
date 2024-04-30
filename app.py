from flask import Flask, render_template, request, Response
import os, signal, webbrowser

from receipt import ImageInfo, ReceiptQueue

app = Flask(__name__)

@app.route("/")
def home():
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

@app.get("/options")
def options():
    return render_template("options.jinja")

@app.get("/quit")
def quit():
    os.kill(os.getpid(), signal.SIGINT)
    return "Server Shutting down..."

@app.post("/cgi-bin/epos/service.cgi")
def epos_print():
    """
    Simulate the ePOS print route. This is called by Odoo PoS customers when they print a receipt.
    It receives the receipt and adds it to the queue.
    """
    receipt_data = request.data or bytes(request.form.get('\n        \n        <s:Envelope xmlns:s'), 'utf-8')
    ReceiptQueue.add_receipt_to_queue(ImageInfo.ImageInfo(receipt_data))
    return Response(
        '<response xmlns="http://www.epson-pos.com/schemas/2011/03/epos-print" success="true" code="dummy-simulated-epos-printer" />',
        mimetype="text/xml",
        headers={"Access-Control-Allow-Origin": "*"}
    )

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    
    parser.add_argument('--https', dest='https', action='store_true', help='Wherever the connection should be in HTTPS (default)', default=True)
    parser.add_argument('--http', dest='https', action='store_false', help='Wherever the connection should be in HTTP')

    args = parser.parse_args()
    is_https = args.https

    URL_SCHEMA = "https" if is_https else "http"
    SSL_CONTEXT = "adhoc" if is_https else None

    webbrowser.open(f"{URL_SCHEMA}://127.0.0.1:5000")
    app.run(ssl_context=SSL_CONTEXT)
