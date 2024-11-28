from odoo.tests.common import TransactionCase, tagged

@tagged('post_install', '-at_install')
class TestDeliveryCorreios(TransactionCase):
    """Testes para a integração com os Correios"""

    def setUp(self):
        super(TestDeliveryCorreios, self).setUp()
        # Configuração inicial do método de entrega Correios
        self.carrier = self.env['delivery.carrier'].create({
            'name': 'Correios',
            'delivery_type': 'correios',
            'correios_service_code': '04014',
            'correios_user': 'usuario_teste',
            'correios_password': 'senha_teste',
            'correios_sender_zip': '01001000',
        })

        # Pedido fictício para teste
        self.order = self.env['sale.order'].create({
            'partner_id': self.env.ref('base.res_partner_1').id,
        })

    def test_correios_rate_shipment(self):
        """Testa o cálculo de frete utilizando a API fictícia dos Correios"""
        result = self.carrier.correios_rate_shipment(self.order)
        self.assertTrue(result['success'], "O cálculo de frete falhou")
        self.assertGreater(result['price'], 0, "O valor do frete deve ser maior que zero")

    def test_validate_config(self):
        """Valida a configuração inicial dos Correios"""
        config = self.env['correios.config'].create({
            'correios_user': 'usuario_teste',
            'correios_password': 'senha_teste',
            'correios_sender_zip': '01001000',
        })
        config.validate_correios_connection()
        self.assertTrue(config.correios_validated, "A configuração dos Correios não foi validada com sucesso")
