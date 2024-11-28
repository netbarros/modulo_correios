import requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    correios_tracking_number = fields.Char(string='Número de Rastreamento')
    correios_last_status = fields.Text(string='Último Status', readonly=True)
    correios_last_update = fields.Datetime(string='Última Atualização', readonly=True)

    @api.model
    def _update_correios_tracking_status(self):
        """Atualiza o status de rastreamento dos envios."""
        pickings = self.search([('correios_tracking_number', '!=', False)])
        if not pickings:
            return

        for picking in pickings:
            try:
                # URL fictícia; ajuste para a real
                url = f'https://api.correios.com.br/rastreamento/{picking.correios_tracking_number}'
                response = requests.get(url, timeout=10)  # Timeout para evitar bloqueios
                response.raise_for_status()  # Levanta exceção se status_code != 200

                data = response.json()
                picking.write({
                    'correios_last_status': data.get('status', _('Status não disponível')),
                    'correios_last_update': fields.Datetime.now(),
                })
                picking.message_post(
                    body=_("Status de rastreamento atualizado: %s" % data.get('status', _('Status não disponível')))
                )
            except requests.exceptions.RequestException as e:
                # Registro de falha no rastreamento
                picking.message_post(
                    body=_("Falha ao atualizar o status de rastreamento para o número %s: %s") %
                         (picking.correios_tracking_number, str(e))
                )
                continue

    @api.model
    def schedule_correios_tracking_update(self):
        """Agenda a atualização de rastreamento automaticamente."""
        self._update_correios_tracking_status()
