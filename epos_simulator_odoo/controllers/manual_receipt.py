from flask import render_template, request

from epos_simulator_odoo import app
from epos_simulator_odoo.controllers.receipts import ImageInfo

@app.route("/receipt-manual", methods = ['GET', 'POST'])
def receipt_manual():
    previous_receipt_content = None
    receipt_info = None
    error = False
    if request.method == 'POST':
        form_content = request.form
        receipt_data = form_content.get('receipt_content')
        if receipt_data:
            previous_receipt_content = receipt_data
            try:
                receipt_data = bytes(receipt_data, 'utf-8')
                receipt_info = ImageInfo(receipt_data)
            except Exception as e:
                app.logger.warning("Error while processing the manual receipt", exc_info=e)
                error = str(e)
    return render_template(
        "manual-receipt.jinja",
        previous_receipt_content=previous_receipt_content,
        receipt_info=receipt_info,
        error=error
    )
