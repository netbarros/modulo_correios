import requests
from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    correios_tracking_number = fields.Char(string='Número de Rastreamento')
    correios_last_status = fields.Char(string='Último Status', readonly=True)

    @api.model
    def _update_correios_tracking_status(self):
        """Atualiza status de rastreamento."""
        for picking in self.search([('correios_tracking_number', '!=', False)]):
            url = f'https://api.correios.com.br/rastreamento/{picking.correios_tracking_number}'
            response = requests.get(url)
            if response.status_code == 200:
                picking.correios_last_status = response.json().get('status')
