from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {'tracking_disable': True})
    main = env.ref('base.main_company')
    main.write({'name': 'Servicios y Equipos en Biotecnología de Zacatecas, S.A. de C.V.', 'vat': 'SEB150217A8A'})
    for warehouse in env['stock.warehouse'].search([('biotex_is_delegation', '=', True), ('biotex_delegation_id', '=', False)]):
        delegation = env['biotex.delegation'].create({
            'name': warehouse.name, 'company_id': warehouse.company_id.id,
            'coordinator_id': warehouse.biotex_coordinator_id.id,
            'responsible_id': warehouse.biotex_responsible_id.id,
        })
        warehouse.biotex_delegation_id = delegation
    for user in env['res.users'].with_context(active_test=False).search([('biotex_warehouse_ids', '!=', False)]):
        user.biotex_delegation_ids = [(4, d.id) for d in user.biotex_warehouse_ids.biotex_delegation_id]
