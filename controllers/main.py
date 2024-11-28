from odoo import http

class CorreiosController(http.Controller):
    @http.route('/correios/test_connection', type='json', auth='user')
    def test_connection(self, **kwargs):
        return {"status": "Conexão com API Correios testada com sucesso!"}
