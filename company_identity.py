"""Identity correction supplied by the customer on 2026-09-06.

Technical module names and historical company/partner IDs deliberately stay stable.
This migration never creates a company or runs the demonstration generator.
"""
import json
import logging

from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

COMPANY_IDENTITIES = (
    {
        'xmlid': 'base.main_company',
        'legacy_names': ('Biotex', 'BIOTEX'),
        'legacy_vat': 'SEB150217A8A',
        'state_code': 'ZAC',
        'values': {
            'name': 'SERVICIOS Y EQUIPOS EN BIOTECNOLOGIA DE ZACATECAS',
            'biotex_short_name': 'SEB Zacatecas', 'vat': 'SEB150217A8A',
            'street': 'Calle Llano de la Isabelica #3000',
            'street2': 'Interior 0, Fracc. Lomas de la Isabelica',
            'zip': '98099', 'city': 'Zacatecas',
        },
    },
    {
        'xmlid': 'biotex_base.company_valma',
        'legacy_names': ('Balma', 'BALMA', 'Valma', 'VALMA'),
        'legacy_vat': 'BAL180522CD2',
        'state_code': 'NLE',
        'values': {
            'name': 'INGENIERIA EN EQUIPOS MEDICOS VALMA',
            'biotex_short_name': 'VALMA', 'vat': 'IEM1809192W9',
            'street': 'Calle Celso Cepeda #5029',
            'street2': 'Col. Plutarco Elías Calles',
            'zip': '64108', 'city': 'Monterrey',
        },
    },
    {
        'xmlid': 'biotex_base.company_pro_omnimedic',
        'legacy_names': ('Pro', 'PRO', 'Pro Omnimedic', 'PRO OMNIMEDIC'),
        'legacy_vat': 'PRO200114EF3',
        'state_code': 'AGU',
        'values': {
            'name': 'PRO OMNIMEDIC',
            'biotex_short_name': 'PRO OMNIMEDIC', 'vat': 'POM210831IH5',
            'street': 'Av. Ignacio Zaragoza #730',
            'street2': 'Interior 9, Col. Valle de las Trojes',
            'zip': '20115', 'city': 'Aguascalientes',
        },
    },
)


def _normalized_vat(value):
    value = (value or '').replace(' ', '').upper()
    return value[2:] if value.startswith('MX') else value


def identity_plan(env):
    """Resolve every company before making any change; ambiguous identity aborts."""
    companies = env['res.company'].with_context(active_test=False).search([])
    mexico = env.ref('base.mx')
    plan = []
    resolved = set()
    for identity in COMPANY_IDENTITIES:
        vat = identity['values']['vat']
        target = env.ref(identity['xmlid'], raise_if_not_found=False)
        by_vat = companies.filtered(lambda company: _normalized_vat(company.vat) == vat)
        if len(by_vat) > 1 or (target and by_vat and target != by_vat):
            raise ValidationError('Identidad fiscal ambigua para %s; revise las empresas existentes.' % vat)
        if not target:
            target = by_vat or companies.filtered(
                lambda company: company.name in identity['legacy_names']
                and _normalized_vat(company.vat) == identity['legacy_vat'])
        allowed_vats = {vat, identity['legacy_vat']}
        if (not target or len(target) != 1 or target._name != 'res.company'
                or _normalized_vat(target.vat) not in allowed_vats or target.id in resolved):
            raise ValidationError('No se pudo identificar de forma inequívoca la empresa %s.' % vat)
        state = env['res.country.state'].search([
            ('country_id', '=', mexico.id), ('code', '=', identity['state_code'])])
        if len(state) != 1:
            raise ValidationError('Revise el estado fiscal mexicano %s.' % identity['state_code'])
        values = dict(identity['values'], country_id=mexico.id, state_id=state.id)
        # Optional localization: 601 is the explicit General de Ley Personas Morales regime.
        if 'l10n_mx_edi_fiscal_regime' in target._fields:
            values['l10n_mx_edi_fiscal_regime'] = '601'
        resolved.add(target.id)
        plan.append((identity['xmlid'], target, values))
    return plan


def apply_company_identities(env):
    plan = identity_plan(env)
    # Mexican localization recomputes this editable choice when a company address
    # becomes complete. Correcting the company must not change an existing order.
    fiscal_choices = {}
    fiscal_field = 'l10n_mx_edi_cfdi_to_public'
    if 'sale.order' in env and fiscal_field in env['sale.order']._fields:
        orders = env['sale.order'].search([('company_id', 'in', [c.id for _, c, _ in plan])])
        fiscal_choices = {order.id: order[fiscal_field] for order in orders}
    for xmlid, company, values in plan:
        before = {key: (company[key].id if company._fields[key].type == 'many2one'
                        else company[key]) for key in values}
        changes = {key: value for key, value in values.items() if before[key] != value}
        if changes:
            company.with_context(tracking_disable=True, mail_notrack=True).write(changes)
            _logger.info('COMPANY_IDENTITY %s', json.dumps({
                'company_id': company.id, 'partner_id': company.partner_id.id,
                'user_id': env.uid, 'before': before, 'after': values,
                'source': 'Customer correction 2026-09-06',
            }, ensure_ascii=False, sort_keys=True))
        partner = company.partner_id
        if ('l10n_mx_edi_fiscal_regime' in partner._fields
                and partner.l10n_mx_edi_fiscal_regime != '601'):
            partner.with_context(tracking_disable=True).write({'l10n_mx_edi_fiscal_regime': '601'})
        if not env.ref(xmlid, raise_if_not_found=False):
            module, name = xmlid.split('.', 1)
            env['ir.model.data'].create({
                'module': module, 'name': name, 'model': 'res.company',
                'res_id': company.id, 'noupdate': True,
            })
    if fiscal_choices:
        orders.flush_recordset([fiscal_field])
        for order in orders:
            if order[fiscal_field] != fiscal_choices[order.id]:
                order.with_context(tracking_disable=True).write({fiscal_field: fiscal_choices[order.id]})
                _logger.info('COMPANY_IDENTITY preserved fiscal choice on sale.order %s', order.id)
    return [company.id for _, company, _ in plan]
