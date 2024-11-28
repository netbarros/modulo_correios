from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests


class DeliveryCorreios(models.Model):
    _inherit = 'delivery.carrier'

    # Campos do modelo
    correios_service_code = fields.Selection(
        selection=[
            ('04014', 'SEDEX'),
            ('04510', 'PAC'),
            ('04782', 'SEDEX 10'),
            ('04804', 'SEDEX Hoje'),
        ],
        string="Serviço dos Correios",
        required=True,
        help="Selecione o tipo de serviço dos Correios para este método de envio."
    )
    correios_user = fields.Char(string="Usuário dos Correios", required=True)
    correios_password = fields.Char(string="Senha dos Correios", required=True)
    correios_contract_code = fields.Char(string="Código do Contrato", required=True)
    correios_sender_zip = fields.Char(string="CEP de Origem", required=True)

    @api.model
    def correios_rate_shipment(self, order):
        """Calcula a tarifa de envio utilizando a API dos Correios."""
        # Validar os dados necessários
        if not self.correios_user or not self.correios_password:
            raise UserError(_('Configure o usuário e a senha dos Correios antes de usar este método.'))

        # Preparar os parâmetros para a API
        url = 'https://api.correios.com.br/frete'
        payload = {
            'cepOrigem': self.correios_sender_zip,
            'cepDestino': order.partner_shipping_id.zip,
            'peso': sum(line.product_id.weight * line.product_uom_qty for line in order.order_line),
            'formato': 1,  # Caixa/Pacote
            'comprimento': 30,  # Valores fictícios (deve ser configurável)
            'altura': 15,
            'largura': 20,
            'diametro': 0,
            'servico': self.correios_service_code,
            'usuario': self.correios_user,
            'senha': self.correios_password,
        }

        # Chamada à API e tratamento de exceções
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            return {
                'success': True,
                'price': result.get('valor', 0.0),
                'error_message': False,
                'warning_message': False,
            }
        except requests.exceptions.HTTPError as e:
            return {
                'success': False,
                'price': 0.0,
                'error_message': _('Erro HTTP: %s') % str(e),
                'warning_message': False,
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'price': 0.0,
                'error_message': _('Erro ao conectar com os Correios: %s') % str(e),
                'warning_message': False,
            }

    def correios_send_shipping(self, pickings):
        """Gera as etiquetas de envio dos Correios."""
        for picking in pickings:
            # Validar os dados do envio
            if not picking.partner_id.zip:
                raise UserError(_('O endereço do cliente deve incluir um CEP válido.'))

            # Dados para a API
            url = 'https://api.correios.com.br/postagem'
            payload = {
                'cepOrigem': self.correios_sender_zip,
                'cepDestino': picking.partner_id.zip,
                'peso': picking.weight,
                'formato': 1,  # Caixa/Pacote
                'servico': self.correios_service_code,
                'usuario': self.correios_user,
                'senha': self.correios_password,
            }

            # Chamada à API e tratamento de exceções
            try:
                response = requests.post(url, json=payload)
                response.raise_for_status()
                result = response.json()
                picking.carrier_tracking_ref = result.get('tracking_code')
                picking.message_post(body=_('Etiqueta gerada com sucesso: %s') % result.get('tracking_code'))
            except requests.exceptions.HTTPError as e:
                raise UserError(_('Erro HTTP ao gerar etiqueta: %s') % str(e))
            except requests.exceptions.RequestException as e:
                raise UserError(_('Erro ao conectar com os Correios: %s') % str(e))

        return True
