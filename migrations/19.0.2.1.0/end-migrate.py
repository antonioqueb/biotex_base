from odoo import SUPERUSER_ID, api
from odoo.addons.biotex_base.company_identity import apply_company_identities


def migrate(cr, version):
    apply_company_identities(api.Environment(cr, SUPERUSER_ID, {}))
