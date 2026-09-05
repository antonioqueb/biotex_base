from odoo import fields, models


class Delegation(models.Model):
    _name = 'biotex.delegation'
    _description = 'Delegación comercial'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, tracking=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    coordinator_id = fields.Many2one('res.users', tracking=True)
    responsible_id = fields.Many2one('res.users', tracking=True)
    warehouse_ids = fields.One2many('stock.warehouse', 'biotex_delegation_id')
    hospital_ids = fields.Many2many('res.partner', string='Hospitales atendidos')


class Warehouse(models.Model):
    _inherit = 'stock.warehouse'

    biotex_delegation_id = fields.Many2one('biotex.delegation', string='Delegación comercial', index=True)


class Users(models.Model):
    _inherit = 'res.users'

    biotex_delegation_ids = fields.Many2many('biotex.delegation', string='Delegaciones comerciales autorizadas')
