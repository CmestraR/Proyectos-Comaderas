from odoo import models, fields, api
import qrcode
import base64
from io import BytesIO

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Generar Codigos QR'

    x_studio_enlace_de_pago = fields.Char('QR Code')
    x_studio_qr_de_pago = fields.Binary(string="QR Image", attachment=True)

    def generate_qr_code_button(self):
        for record in self:
            if record.x_studio_enlace_de_pago:
                # Generar Codigo QR de pagos
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(record.x_studio_enlace_de_pago)
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white")

                temp = BytesIO()
                img.save(temp, format="PNG")
                temp.seek(0)

                record.x_studio_qr_de_pago = base64.b64encode(temp.getvalue())
