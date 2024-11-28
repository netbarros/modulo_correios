from odoo.tests.common import TransactionCase

class TestDeliveryCorreios(TransactionCase):

    def setUp(self):
        super(TestDeliveryCorreios, self).setUp()
        self.carrier = self.env['delivery.carrier'].create({
            'name': 'Correios',
            'delivery_type': 'correios',
        })

    def test_correios_rate_shipment(self):
        """Testa o cálculo de frete"""
        order = self.env['sale.order'].create({
            'partner_id': self.env.ref('base.res_partner_1').id,
        })
        result = self.carrier.correios_rate_shipment(order)
        self.assertTrue(result)

    def test_validate_config(self):
        """Valida a configuração inicial"""
        config = self.env['correios.config'].create({
            'correios_user': 'usuario_teste',
            'correios_password': 'senha_teste',
            'correios_sender_zip': '01001000',
        })
        config.validate_correios_connection()
        self.assertTrue(config.correios_validated)
