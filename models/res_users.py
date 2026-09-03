from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    biotex_warehouse_ids = fields.Many2many(
        'stock.warehouse', 'biotex_user_warehouse_rel', 'user_id', 'warehouse_id',
        string='Delegaciones asignadas',
        help='Delegaciones sobre las que el usuario puede solicitar, autorizar o recibir.')
    biotex_default_warehouse_id = fields.Many2one(
        'stock.warehouse', string='Delegación por defecto',
        compute='_compute_biotex_default_warehouse', store=True, readonly=False)

    @api.depends('biotex_warehouse_ids')
    def _compute_biotex_default_warehouse(self):
        for user in self:
            if not user.biotex_default_warehouse_id or user.biotex_default_warehouse_id not in user.biotex_warehouse_ids:
                user.biotex_default_warehouse_id = user.biotex_warehouse_ids[:1]

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + ['biotex_warehouse_ids', 'biotex_default_warehouse_id']
