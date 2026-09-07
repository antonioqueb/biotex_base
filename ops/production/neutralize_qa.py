"""Apply after Odoo's native neutralization, before exposing QA to any HTTP request."""
import uuid
import os

assert env.cr.dbname == 'bioteczac'
params = env['ir.config_parameter'].sudo()
params.set_param('database.uuid', str(uuid.uuid4()))
params.set_param('database.is_neutralized', True)
params.set_param('bioteczac.environment', 'qa')
params.set_param('web.base.url', os.environ.get('BIOTECZAC_PUBLIC_BASE_URL', 'http://localhost:1401'))
params.set_param('web.base.url.freeze', True)
params.set_param('auth_signup.invitation_scope', 'b2b')
env['ir.cron'].search([]).write({'active': False})
env['ir.mail_server'].search([]).write({'active': False})
if 'fetchmail.server' in env: env['fetchmail.server'].search([]).write({'active': False})
if 'mail.mail' in env:
    env['mail.mail'].search([('state', 'in', ['outgoing', 'exception'])]).write({'state': 'cancel'})
if 'payment.provider' in env: env['payment.provider'].search([]).write({'state': 'disabled'})
if 'base.automation' in env: env['base.automation'].search([]).write({'active': False})
if 'sms.sms' in env:
    env['sms.sms'].search([('state', 'in', ['outgoing', 'error'])]).write({'state': 'canceled'})
for company in env['res.company'].search([]):
    values = {}
    for field in ('l10n_mx_edi_pac_username', 'l10n_mx_edi_pac_password'):
        if field in company._fields: values[field] = False
    if 'l10n_mx_edi_pac_test_env' in company._fields: values['l10n_mx_edi_pac_test_env'] = True
    if values: company.write(values)
# Private signing material is not copied into a usable QA credential store.
if 'l10n_mx_edi.certificate' in env:
    for certificate in env['l10n_mx_edi.certificate'].search([]):
        values = {key: False for key in ('key', 'password', 'active') if key in certificate._fields}
        if values: certificate.write(values)
if 'res.users.apikeys' in env: env['res.users.apikeys'].search([]).unlink()
# Human accounts belong to the production snapshot: preserve login, password
# hashes, active state, company/group permissions, TOTP and passkeys. The
# lifecycle verifies these against the snapshot before exposing QA. Integration
# API keys remain disabled above; browser sessions are cleared during restore.
env.cr.commit()
print('QA_NEUTRALIZED')
