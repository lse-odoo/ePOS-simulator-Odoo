from flask import Flask

app = Flask(__name__)

import epos_simulator_odoo.controllers.usage
import epos_simulator_odoo.controllers.receipts
import epos_simulator_odoo.controllers.test_receipts
import epos_simulator_odoo.controllers.options
