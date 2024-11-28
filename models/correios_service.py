from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class CorreiosService(models.Model):
    _name = 'correios.service'
    _description = 'Serviços dos Correios'

    name = fields.Char(string='Nome do Serviço', required=True)
    code = fields.Char(string='Código do Serviço', required=True)
    description = fields.Text(string='Descrição')
    active = fields.Boolean(string='Ativo', default=True)
    delivery_carrier_ids = fields.One2many(
        'delivery.carrier', 'correios_service_id',
        string='Métodos de Entrega Relacionados'
    )

    @api.constrains('code')
    def _check_code_uniqueness(self):
        """Valida a unicidade e preenchimento do código do serviço"""
        for record in self:
            if not record.code:
                raise ValidationError(_('O código do serviço é obrigatório.'))
            if self.search_count([('code', '=', record.code)]) > 1:
                raise ValidationError(
                    _('O código "%s" já está associado a outro serviço dos Correios.') % record.code
                )

    @api.ondelete(at_uninstall=False)
    def _prevent_deletion_if_related(self):
        """Evita exclusão de serviços vinculados a métodos de entrega"""
        for record in self:
            if record.delivery_carrier_ids:
                raise ValidationError(
                    _('O serviço "%s" não pode ser excluído porque está relacionado a métodos de entrega.') % record.name
                )

    def name_get(self):
        """Customiza a exibição do nome do serviço"""
        result = []
        for record in self:
            name = f"[{record.code}] {record.name}"
            result.append((record.id, name))
        return result

