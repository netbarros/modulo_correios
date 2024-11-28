from odoo import models, fields, api, _
from odoo.exceptions import UserError

class CorreiosConfig(models.TransientModel):
    _name = 'correios.config'
    _inherit = 'res.config.settings'

    correios_user = fields.Char(string='Usuário', required=True)
    correios_password = fields.Char(string='Senha', required=True)
    correios_contract_code = fields.Char(string='Código do Contrato')
    correios_sender_zip = fields.Char(string='CEP de Origem', required=True)

    correios_validated = fields.Boolean(string='Configuração Validada', readonly=True)

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
            if response.status_code == 200 and response.json().get('status') == 'sucesso':
                self.correios_validated = True
            else:
                raise UserError(_('Erro na validação: Verifique as credenciais.'))
        except Exception as e:
            raise UserError(_('Erro de conexão: %s') % str(e))
