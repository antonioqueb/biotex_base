from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = 'res.company'

    biotex_is_default_buyer = fields.Boolean(
        string='Razón social compradora por defecto',
        help='Regla: se compra por defecto con Biotex; Balma/Pro solo por excepción documentada.')
    biotex_short_name = fields.Char(string='Nombre corto', help='Ej. BIOTEX, BALMA, PRO')
    biotex_remision_footer = fields.Html(string='Pie de remisión')

    @api.constrains('biotex_is_default_buyer')
    def _check_single_default_buyer(self):
        buyers = self.search([('biotex_is_default_buyer', '=', True)])
        if len(buyers) > 1:
            raise ValidationError('Solo una razón social puede ser la compradora por defecto.')

    @api.model
    def biotex_get_default_buyer(self):
        return self.search([('biotex_is_default_buyer', '=', True)], limit=1) or self.env.company
