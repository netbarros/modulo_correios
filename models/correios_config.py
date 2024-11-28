from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests  # Certifique-se de incluir no requirements.txt

class CorreiosConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    correios_user = fields.Char(string='Usuário', required=True)
    correios_password = fields.Char(string='Senha', required=True)
    correios_contract_code = fields.Char(string='Código do Contrato')
    correios_sender_zip = fields.Char(string='CEP de Origem', required=True)

    correios_validated = fields.Boolean(string='Configuração Validada', readonly=True)

    @api.model
    def get_values(self):
        """Obtém valores armazenados no ir.config_parameter."""
        params = self.env['ir.config_parameter'].sudo()
        return {
            'correios_user': params.get_param('correios.user', default=''),
            'correios_password': params.get_param('correios.password', default=''),
            'correios_contract_code': params.get_param('correios.contract_code', default=''),
            'correios_sender_zip': params.get_param('correios.sender_zip', default=''),
            'correios_validated': params.get_param('correios.validated', default=False),
        }

    def set_values(self):
        """Salva os valores no ir.config_parameter."""
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('correios.user', self.correios_user)
        params.set_param('correios.password', self.correios_password)
        params.set_param('correios.contract_code', self.correios_contract_code)
        params.set_param('correios.sender_zip', self.correios_sender_zip)
        params.set_param('correios.validated', self.correios_validated)

    def validate_correios_connection(self):
        """Valida a conexão com a API dos Correios."""
        url = 'https://api.correios.com.br/validar'
        data = {
            'usuario': self.correios_user,
            'senha': self.correios_password,
            'contrato': self.correios_contract_code,
        }
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            if result.get('status') == 'sucesso':
                self.correios_validated = True
                self.set_values()  # Salva a validação como True
            else:
                raise UserError(_('Erro na validação: %s') % result.get('mensagem', 'Desconhecido'))
        except requests.exceptions.RequestException as e:
            raise UserError(_('Erro de conexão: %s') % str(e))

    @api.constrains('correios_user', 'correios_password', 'correios_sender_zip')
    def _check_required_fields(self):
        """Valida se os campos obrigatórios estão preenchidos."""
        if not self.correios_user or not self.correios_password or not self.correios_sender_zip:
            raise UserError(_('Os campos "Usuário", "Senha" e "CEP de Origem" são obrigatórios.'))

