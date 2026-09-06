#!/usr/bin/env python3
"""Rename the existing stopped Odoo database and filestore, with reversible recovery.

Run only on the deployment host after backup, addon upgrade and data controls.
No source code or database is transferred or recreated by this command.
"""
import argparse
import configparser
import json
import pathlib
import subprocess


def sql(statement):
    return subprocess.check_output([
        'docker', 'exec', 'biotex-db-1', 'psql', '-U', 'odoo', '-d', 'postgres',
        '-At', '-v', 'ON_ERROR_STOP=1', '-c', statement,
    ], text=True).strip()


def rename_instance(old, new, filestore_root, config_path, evidence):
    # Whitelist names before interpolation as SQL identifiers/literals.
    for name in (old, new):
        if not name or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789_' for c in name):
            raise ValueError('Invalid database identifier')
    root = pathlib.Path(filestore_root)
    config = pathlib.Path(config_path)
    old_store, new_store = root / old, root / new
    assert old_store.is_dir() and not new_store.exists(), 'Unexpected filestore state'
    oid = sql("SELECT oid FROM pg_database WHERE datname='%s'" % old)
    assert oid and not sql("SELECT oid FROM pg_database WHERE datname='%s'" % new), 'Unexpected database state'
    active = sql("SELECT count(*) FROM pg_stat_activity WHERE datname='%s'" % old)
    assert active == '0', 'Stop all Odoo connections before renaming the database'
    original_config = config.read_bytes()
    parser = configparser.ConfigParser()
    parser.read_string(original_config.decode())
    # Refuse an unrelated instance configuration, while accepting an unset database.
    configured = parser['options'].get('db_name', '').strip()
    assert configured in ('', 'False', old), 'Configuration belongs to another database'
    database_renamed = False
    store_renamed = False
    try:
        sql('ALTER DATABASE "%s" ALLOW_CONNECTIONS false' % old)
        sql('ALTER DATABASE "%s" RENAME TO "%s"' % (old, new))
        database_renamed = True
        old_store.rename(new_store)
        store_renamed = True
        parser['options']['db_name'] = new
        parser['options']['dbfilter'] = '^%s$' % new
        # Keep the same inode: the configuration file is bind-mounted by Docker.
        with config.open('w') as stream:
            parser.write(stream)
        sql('ALTER DATABASE "%s" ALLOW_CONNECTIONS true' % new)
        assert sql("SELECT oid FROM pg_database WHERE datname='%s'" % new) == oid
        assert not sql("SELECT oid FROM pg_database WHERE datname='%s'" % old)
    except Exception:
        config.write_bytes(original_config)
        if store_renamed:
            new_store.rename(old_store)
        if database_renamed:
            sql('ALTER DATABASE "%s" RENAME TO "%s"' % (new, old))
        sql('ALTER DATABASE "%s" ALLOW_CONNECTIONS true' % old)
        raise
    result = {'previous_database': old, 'database': new, 'preserved_oid': int(oid),
              'filestore': str(new_store), 'configuration': str(config)}
    pathlib.Path(evidence).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--old', required=True)
    parser.add_argument('--new', required=True)
    parser.add_argument('--filestore-root', required=True)
    parser.add_argument('--config', required=True)
    parser.add_argument('--evidence', required=True)
    args = parser.parse_args()
    rename_instance(args.old, args.new, args.filestore_root, args.config, args.evidence)
