from odoo import models, fields, api, _
from odoo.exceptions import UserError

class CorreiosNotification(models.Model):
    _name = 'correios.notification'
    _description = 'Notificação de Rastreamento dos Correios'

    sale_order_id = fields.Many2one('sale.order', string="Pedido de Venda", required=True)
    tracking_code = fields.Char(string="Código de Rastreamento", required=True)
    email_sent = fields.Boolean(string="E-mail Enviado", default=False)

    def send_notification_email(self):
        """Envia um e-mail para o cliente com o código de rastreamento"""
        for notification in self:
            if not notification.sale_order_id.partner_id.email:
                raise UserError(_('O cliente associado ao pedido não possui um endereço de e-mail.'))

            mail_values = {
                'subject': _('Código de Rastreamento do Pedido #%s') % notification.sale_order_id.name,
                'body_html': _(
                    '<p>Olá %s,</p>'
                    '<p>O seu pedido #%s foi enviado pelos Correios.</p>'
                    '<p>O código de rastreamento é: <strong>%s</strong></p>'
                    '<p>Você pode rastreá-lo diretamente no site dos Correios.</p>'
                ) % (
                    notification.sale_order_id.partner_id.name,
                    notification.sale_order_id.name,
                    notification.tracking_code,
                ),
                'email_to': notification.sale_order_id.partner_id.email,
                'email_from': 'notifications@kikasolutions.com.br',  # Configure o e-mail do remetente corretamente
            }

            mail = self.env['mail.mail'].create(mail_values)
            mail.send()
            notification.email_sent = True
