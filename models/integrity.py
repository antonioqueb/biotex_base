"""Shared transaction guards. No client-supplied context can authorize a transition."""
import math
from odoo.exceptions import AccessError, UserError
from odoo.tools import SQL


_TRANSITION = object()


def lock_records(records):
    if not records:
        return
    records.check_access('write')
    records.flush_recordset()
    records.env.cr.execute(SQL(
        'SELECT id FROM %s WHERE id IN %s ORDER BY id FOR UPDATE',
        SQL.identifier(records._table), tuple(records.ids),
    ))
    records.invalidate_recordset()


def require_group(records, *groups):
    records.check_access('write')
    if not records.env.su and not any(records.env.user.has_group(g) for g in groups):
        raise AccessError('Su función no tiene permiso para confirmar esta operación.')


def transition(records, values):
    """Private Python capability; never exported as a public ORM method."""
    return records.with_context(_biotex_transition=_TRANSITION).write(values)


def is_transition(records):
    return records.env.context.get('_biotex_transition') is _TRANSITION


def guard_write(records, values, protected=(), frozen=(), editable=('draft',)):
    if is_transition(records):
        return
    if set(values) & set(protected):
        raise UserError('Use la acción correspondiente; no se permite cambiar directamente el estado o la autorización.')
    if set(values) & set(frozen):
        lock_records(records)
        if any(r.state not in editable for r in records):
            raise UserError('El documento confirmado conserva sus datos. Registre una corrección relacionada.')


def guard_create(values_list, protected=(), initial_state='draft'):
    for values in values_list:
        if (values.get('state', initial_state) != initial_state
                or any(values.get(key) for key in protected)):
            raise UserError('Los documentos nuevos deben comenzar sin ejecución ni autorización.')


def convert_qty(quantity, source, target):
    if not source or not target or not math.isfinite(quantity):
        raise UserError('Indique una cantidad finita y unidades válidas.')
    def root(unit):
        while unit.relative_uom_id:
            unit = unit.relative_uom_id
        return unit
    if root(source) != root(target):
        raise UserError('Las unidades no tienen una conversión compatible validada.')
    return source._compute_quantity(quantity, target, round=False)
