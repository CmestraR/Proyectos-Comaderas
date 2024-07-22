from odoo import models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'WhatsApp Sale Order'

    def whatsapp_sale_order(self):
        url = 'https://web.whatsapp.com/send?phone='
        mobile = self.partner_id.mobile
        if not mobile:
            raise ValidationError(_('Por favor verifique el número del cliente.'))

        so_message = 'Hola%20*' + self.partner_id.name.replace(' ', '*%20*') + ',*%0a'
        so_message += '%0aTu%20cotización%20*' + self.name + '*%20ha%20sido%20generada%20con%20los%20siguientes%20detalles:%0a%0a'
        currency = self.pricelist_id.currency_id.symbol
        sol_message = ''
        sequence = 0
        for soline in self.order_line:
            sequence += 1
            sol_message += '===============%20' + '*' + str(sequence) + '*' + '%20===============%0a'
            name = soline.name.replace(' ', '%20')
            sol_message += '*Producto*%20*:*%20' + name + '%0a'
            sol_message += '*Cantidad%20Ordenada*%20*:*%20' + str(soline.product_uom_qty) + '%0a'
            sol_message += '*Precio%20Unitario*%20*:*%20' + currency + str(soline.price_unit) + '%0a'
            if soline.tax_id:
                msg = '*Impuestos*%20*:*%20'
                taxes = ", ".join(soline.tax_id.mapped('name'))
                sol_message += msg + taxes + '%0a'
                sol_message += '*Subtotal*%20*:*%20' + currency + str(soline.price_subtotal) + '%20' + '%0a%0a'
        so_message += sol_message
        so_message += '================================'
        so_message += '%0a*Subtotal%20sin%20Impuestos*%20*:*%20' + currency + str(self.amount_untaxed) + '%0a'
        so_message += msg + currency + str(self.amount_tax) + '%0a'
        so_message += '*================================*'
        so_message += '%0a*Total%20a%20pagar*%20*:*%20*' + currency + str(self.amount_total) + '*%0a'
        so_message += '*================================*%0a%0a'
        so_message += 'Ahora puedes pagar a través de nuestro link de pagos:' + '%0a' 
        url_dinamica = self.x_studio_enlace_de_pago.replace("&", "%26")
        so_message += url_dinamica + '%0a'
        so_message += '%0a' + 'Saludos,' + '%0a'
        so_message += '%0a*Asesor de Ventas*%20*:*%20*' + str(self.user_id.name) + '*%0a'
        so_message += self.company_id.name + '%0a'
        
        url += str(mobile) + "&text=" + so_message
        return {'type': 'ir.actions.act_url',
                'name': "WhatsApp Sale Order",
                'target': 'new',
                'url': url}