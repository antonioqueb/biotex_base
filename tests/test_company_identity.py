from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged

from ..company_identity import COMPANY_IDENTITIES, apply_company_identities, identity_plan


@tagged('post_install', '-at_install')
class TestCompanyIdentity(TransactionCase):
    """Migration tests on the restored customer database; all fixtures roll back."""

    def test_upgrade_persists_complete_fiscal_identity(self):
        # Do not call the helper: verify what the actual module upgrade committed.
        for _, company, values in identity_plan(self.env):
            for key, expected in values.items():
                actual = company[key]
                if company._fields[key].type == 'many2one':
                    actual = actual.id
                self.assertEqual(actual, expected, '%s: %s' % (company.id, key))
            if 'l10n_mx_edi_fiscal_regime' in company.partner_id._fields:
                self.assertEqual(company.partner_id.l10n_mx_edi_fiscal_regime, '601')

    def test_identity_and_native_partner_are_updated_in_place(self):
        plan = identity_plan(self.env)
        identifiers = [(company.id, company.partner_id.id) for _, company, _ in plan]
        company_ids = sorted(self.env['res.company'].search([]).ids)
        banks = self.env['res.partner.bank'].search([]).read(['partner_id', 'acc_number'])
        warehouses = self.env['stock.warehouse'].search([]).read(['company_id', 'partner_id'])
        for identity, (_, company, _) in zip(COMPANY_IDENTITIES, plan):
            company.with_context(no_vat_validation=True, tracking_disable=True).write({
                'name': identity['legacy_names'][0], 'vat': identity['legacy_vat'],
                'zip': False, 'street': 'Domicilio anterior de prueba',
            })
        apply_company_identities(self.env)
        self.assertEqual(company_ids, sorted(self.env['res.company'].search([]).ids))
        self.assertEqual(identifiers, [(company.id, company.partner_id.id) for _, company, _ in identity_plan(self.env)])
        for _, company, values in identity_plan(self.env):
            self.assertEqual(company.partner_id.name, values['name'])
            self.assertEqual(company.partner_id.vat, values['vat'])
            self.assertEqual(company.zip, values['zip'])
            self.assertEqual(company.state_id.id, values['state_id'])
        self.assertEqual(banks, self.env['res.partner.bank'].search([]).read(['partner_id', 'acc_number']))
        self.assertEqual(warehouses, self.env['stock.warehouse'].search([]).read(['company_id', 'partner_id']))

    def test_repeated_migration_makes_no_additional_writes(self):
        apply_company_identities(self.env)
        companies = self.env['res.company'].browse([c.id for _, c, _ in identity_plan(self.env)])
        before = companies.read(['write_date', 'partner_id'])
        messages = self.env['mail.message'].search_count([])
        apply_company_identities(self.env)
        self.assertEqual(before, companies.read(['write_date', 'partner_id']))
        self.assertEqual(messages, self.env['mail.message'].search_count([]))

    def test_company_address_preserves_existing_sale_fiscal_choice(self):
        field = 'l10n_mx_edi_cfdi_to_public'
        if 'sale.order' not in self.env or field not in self.env['sale.order']._fields:
            self.skipTest('Mexican sale localization is not installed')
        main = identity_plan(self.env)[0][1]
        orders = self.env['sale.order'].search([('company_id', '=', main.id)])
        self.assertTrue(orders, 'Restored customer orders are required for this regression')
        main.with_context(tracking_disable=True).zip = False
        orders.with_context(tracking_disable=True).write({field: True})
        orders.flush_recordset([field])
        apply_company_identities(self.env)
        orders.flush_recordset([field])
        self.assertTrue(all(orders.mapped(field)))
        self.assertEqual(main.zip, '98099')

    def test_duplicate_rfc_aborts_before_any_company_changes(self):
        plan = identity_plan(self.env)
        main, valma = plan[0][1], plan[1][1]
        main.with_context(tracking_disable=True).name = 'Nombre previo por conservar'
        valma.with_context(no_vat_validation=True, tracking_disable=True).vat = main.vat
        with self.assertRaises(ValidationError):
            apply_company_identities(self.env)
        self.assertEqual(main.name, 'Nombre previo por conservar')

    def test_company_xmlid_with_unrelated_rfc_is_not_overwritten(self):
        valma = identity_plan(self.env)[1][1]
        valma.with_context(no_vat_validation=True, tracking_disable=True).vat = 'XAXX010101000'
        with self.assertRaises(ValidationError):
            apply_company_identities(self.env)
        self.assertEqual(valma.vat, 'XAXX010101000')
