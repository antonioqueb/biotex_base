from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    biotex_partner_type = fields.Selection([
        ('institution', 'Institución pública'),
        ('private', 'Cliente privado'),
        ('supplier', 'Proveedor'),
        ('other', 'Otro'),
    ], string='Tipo de contacto', default='other')
    biotex_institution_code = fields.Char(string='Clave institución', help='IMSS, ISSSTE, SEDENA, BIENESTAR, SSA-XX')
    biotex_accepted_brand_ids = fields.Many2many(
        'res.partner.category', 'biotex_partner_brand_tag_rel', 'partner_id', 'tag_id',
        string='Restricciones de marca (etiquetas)',
        help='Algunos hospitales solo aceptan ciertas marcas (ej. Hudson / Intersurgical).')
