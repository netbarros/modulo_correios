# models/correios_service.py
from odoo import models, fields

class CorreiosService(models.Model):
    _name = 'correios.service'
    _description = 'Serviços dos Correios'

    name = fields.Char(string='Nome do Serviço', required=True)
    code = fields.Char(string='Código do Serviço', required=True)
    description = fields.Text(string='Descrição')
