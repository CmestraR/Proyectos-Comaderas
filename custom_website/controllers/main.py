from odoo import http
from odoo.http import request

class MyModuleController(http.Controller):

    @http.route('/my_module/get_city_data', type='json', auth='public', methods=['POST'], csrf=False)
    def get_city_data(self, city_name):
        if city_name:
            city = request.env['res.city'].sudo().search([('name', 'ilike', city_name)], limit=1)
            if city:
                return {'zipcode': city.zipcode, 'state_id': city.state_id.id}
        return {'error': 'City not found'}
