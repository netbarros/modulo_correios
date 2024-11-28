from odoo import http
from odoo.http import request
import requests

class CorreiosController(http.Controller):
    @http.route('/correios/test_connection', type='json', auth='user', methods=['POST'])
    def test_connection(self, **kwargs):
        """
        Testa a conexão com a API dos Correios.
        Retorna o status da conexão e mensagens associadas.
        """
        # Parâmetros padrão (simulação)
        correios_user = kwargs.get('correios_user')
        correios_password = kwargs.get('correios_password')
        correios_contract_code = kwargs.get('correios_contract_code')

        if not correios_user or not correios_password:
            return {
                "status": "error",
                "message": "Usuário e senha dos Correios são obrigatórios."
            }

        # Simulação de requisição para a API dos Correios
        url = 'https://api.correios.com.br/validar'
        payload = {
            'usuario': correios_user,
            'senha': correios_password,
            'contrato': correios_contract_code
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()

            # Verifica a resposta da API
            result = response.json()
            if result.get('status') == 'sucesso':
                return {
                    "status": "success",
                    "message": "Conexão com a API dos Correios validada com sucesso!",
                    "details": result
                }
            else:
                return {
                    "status": "error",
                    "message": "Erro na validação com os Correios.",
                    "details": result
                }
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": "Erro ao conectar com a API dos Correios.",
                "details": str(e)
            }
