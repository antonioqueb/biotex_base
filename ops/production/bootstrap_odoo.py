"""Run with Odoo shell, on the freshly initialized production database only."""
import json
from pathlib import Path
from odoo import Command
from odoo.addons.biotex_base.company_identity import COMPANY_IDENTITIES, apply_company_identities
from odoo.addons.biotex_catalog.tools.import_remap import import_catalog

assert env.cr.dbname == 'bioteczac'
assert not env['ir.config_parameter'].get_param('bioteczac.production_initialized')
assert not env['ir.module.module'].search_count([('name', '=', 'biotex_demo'), ('state', '=', 'installed')])
assert not env['account.move'].search_count([])
assert not env['stock.move'].search_count([])
main = env.ref('base.main_company')
mxn = env.ref('base.MXN')
main.write({'currency_id': mxn.id, 'logo': False})
for identity in COMPANY_IDENTITIES[1:]:
    assert not env['res.company'].search([('vat', '=', identity['values']['vat'])])
    env['res.company'].create(dict(identity['values'], country_id=env.ref('base.mx').id,
                                   currency_id=mxn.id, logo=False))
apply_company_identities(env)
companies = env['res.company'].search([])
assert len(companies) == 3
for company in companies:
    company.partner_id.write({'phone': False, 'email': False, 'website': False})
    env['account.chart.template'].with_company(company).try_loading('mx', company, install_demo=False)
    if 'l10n_mx_edi_pac_test_env' in company._fields:
        company.l10n_mx_edi_pac_test_env = False
    # Odoo requires a warehouse for stock operations, but its real physical site is pending.
    for warehouse in env['stock.warehouse'].search([('company_id', '=', company.id)]):
        warehouse.write({'name': 'Almacén por configurar - ' + company.biotex_short_name,
                         'biotex_is_delegation': False, 'biotex_is_central': False, 'active': False})
    # Do not inherit a fictitious footer, phone, logo or bank account.
    company.biotex_remision_footer = False
admin = env.ref('base.user_admin').with_context(no_reset_password=True, tracking_disable=True,
                                              mail_create_nosubscribe=True)
admin.write({'login': 'soporte@alphacap.com', 'name': 'Soporte AlphaCap',
             'email': 'soporte@alphacap.com', 'company_id': main.id,
             'company_ids': [Command.set(companies.ids)], 'lang': 'es_MX',
             'tz': 'America/Monterrey', 'password': Path('/run/secrets/login_password').read_text().strip(),
             'group_ids': [Command.link(env.ref('biotex_base.group_biotex_direction').id),
                           Command.link(env.ref('biotex_catalog.group_catalog_classifier').id)]})
# Keep Odoo's technical users (bot/public/template) but no other interactive account.
for user in env['res.users'].with_context(active_test=False).search([('id', 'not in', [1, admin.id])]):
    user.write({'active': False})
params = env['ir.config_parameter'].sudo()
params.set_param('auth_signup.invitation_scope', 'b2b')
params.set_param('web.base.url', 'http://localhost:1400')
params.set_param('web.base.url.freeze', True)
params.set_param('database.is_neutralized', False)
params.set_param('bioteczac.environment', 'production')
# No external services have been authorized/configured at production cutover.
if 'digest.digest' in env: env['digest.digest'].search([]).write({'state': 'deactivated'})
if 'ir.mail_server' in env: env['ir.mail_server'].search([]).write({'active': False})
result = import_catalog(env, '/imports/Modelo_Clasificacion_v2_Remapeo.xlsx', operational_prices=False)
assert not env['biotex.delegation'].search_count([])
assert not env['account.move'].search_count([])
assert not env['stock.quant'].search_count([('quantity', '!=', 0)])
params.set_param('bioteczac.production_initialized', True)
env.cr.commit()
print('BOOTSTRAP_OK ' + json.dumps(result, sort_keys=True))
