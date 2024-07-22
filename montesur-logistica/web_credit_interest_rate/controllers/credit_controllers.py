from odoo import http

class AllocationOfCreditAmount(http.Controller):
    #@http.route('/tasasvigentes', auth='public', website=True, sitemap=False)
    @http.route('/tasasvigentes', auth='public', website=True, sitemap=True)
    def interest_rate(self, **kw):
        interest_rates = http.request.env['x_tasas_vigentes'].search([])
        values = {
            'interest': interest_rates
        }
        return http.request.render('web_credit_interest_rate.interest_rate_template', values)
