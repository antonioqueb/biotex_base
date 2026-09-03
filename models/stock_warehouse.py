from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StockWarehouse(models.Model):
    """Una delegación = un almacén (R24)."""
    _inherit = 'stock.warehouse'

    biotex_is_delegation = fields.Boolean(string='Es delegación', default=True)
    biotex_is_central = fields.Boolean(
        string='Almacén central (inventario contable)',
        help='Zacatecas concentra el inventario contable; las demás delegaciones reciben por venta interna.')
    biotex_state_name = fields.Char(string='Estado / región')
    biotex_responsible_id = fields.Many2one(
        'res.users', string='Almacenista / vendedor',
        help='Captura solicitudes de compra y recibe mercancía.')
    biotex_coordinator_id = fields.Many2one(
        'res.users', string='Coordinador',
        help='Autoriza el sustento (contrato / emergente / privado) de cada solicitud.')
    biotex_covered_zones = fields.Char(
        string='Zonas que surte', help='Ej. Yucatán surte Campeche y Quintana Roo.')
    biotex_whatsapp_group = fields.Char(string='Grupo WhatsApp')
    biotex_notes = fields.Text(string='Notas operativas')

    @api.constrains('biotex_is_central', 'company_id')
    def _check_single_central(self):
        for wh in self.filtered('biotex_is_central'):
            others = self.search([('biotex_is_central', '=', True), ('id', '!=', wh.id)])
            if others:
                raise ValidationError(
                    'Solo puede existir un almacén central (actualmente: %s).' % ', '.join(others.mapped('name')))

    def biotex_get_notify_partners(self):
        """Partners a notificar por cambios de estatus en la delegación (R45)."""
        self.ensure_one()
        users = self.biotex_responsible_id | self.biotex_coordinator_id
        return users.mapped('partner_id')
