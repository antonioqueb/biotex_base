from odoo import api, fields, models
from odoo.exceptions import UserError
from .integrity import guard_create, guard_write, lock_records, require_group, transition


class OperationalException(models.Model):
    _name = 'biotex.exception'
    _description = 'Autorización de excepción operativa'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Motivo', required=True, tracking=True)
    kind = fields.Selection([
        ('regularization', 'Entrega pendiente de regularizar'),
        ('substitution', 'Sustitución'), ('intercompany', 'Operación entre empresas'),
        ('excess', 'Cantidad adicional'), ('closure', 'Cierre con faltante'),
        ('stock', 'Incidencia de inventario'), ('document', 'Excepción documental'),
    ], required=True, tracking=True)
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    state = fields.Selection([('draft', 'Borrador'), ('approved', 'Aprobada'), ('revoked', 'Revocada')],
                             default='draft', tracking=True, copy=False)
    effect = fields.Text(string='Efecto permitido y límites', required=True, tracking=True)
    attachment_ids = fields.Many2many('ir.attachment', string='Soporte original', copy=False)
    approved_by_id = fields.Many2one('res.users', readonly=True, copy=False)
    approved_on = fields.Datetime(readonly=True, copy=False)
    date_end = fields.Date(string='Válida hasta')

    @api.model_create_multi
    def create(self, vals_list):
        guard_create(vals_list, ('approved_by_id', 'approved_on'))
        return super().create(vals_list)

    def write(self, vals):
        guard_write(self, vals, ('state', 'approved_by_id', 'approved_on'),
                    ('name', 'kind', 'company_id', 'effect', 'attachment_ids', 'date_end'))
        return super().write(vals)

    def unlink(self):
        if any(r.state != 'draft' for r in self):
            raise UserError('Conserve el historial de las autorizaciones.')
        return super().unlink()

    def action_approve(self):
        require_group(self, 'biotex_base.group_biotex_direction')
        lock_records(self)
        for rec in self:
            if rec.state == 'approved':
                continue
            if rec.state != 'draft' or not rec.attachment_ids:
                raise UserError('La autorización requiere borrador y soporte original.')
            transition(rec, {'state': 'approved', 'approved_by_id': self.env.uid, 'approved_on': fields.Datetime.now()})

    def action_revoke(self):
        require_group(self, 'biotex_base.group_biotex_direction')
        lock_records(self)
        transition(self, {'state': 'revoked'})

    def _check_valid(self, company, kind):
        self.ensure_one()
        self.check_access('read')
        if (self.state != 'approved' or self.company_id != company or self.kind != kind
                or (self.date_end and self.date_end < fields.Date.context_today(self))):
            raise UserError('Se necesita una autorización vigente para este efecto y empresa.')
