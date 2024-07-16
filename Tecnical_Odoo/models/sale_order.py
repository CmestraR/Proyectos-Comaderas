from odoo import models, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    def action_show_hello_world(self):
        raise UserError("Hola Mundo")

