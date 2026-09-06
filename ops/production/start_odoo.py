#!/usr/bin/env python3
"""Materialize secrets only in a private tmpfs config; never put them in argv."""
import configparser
import os
import pathlib
import sys

config = configparser.ConfigParser(interpolation=None)
config.read('/etc/odoo/base.conf')
for key, filename in [('db_password', 'app_password'), ('admin_passwd', 'manager_password')]:
    config['options'][key] = pathlib.Path('/run/secrets/' + filename).read_text().strip()
path = pathlib.Path('/tmp/runtime-odoo.conf')
fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
with os.fdopen(fd, 'w') as stream:
    config.write(stream)
args = sys.argv[1:]
if args and args[0] == 'odoo':
    args.pop(0)
command = args.pop(0) if args and args[0] in ('shell', 'neutralize') else None
argv = ['odoo'] + ([command] if command else []) + ['-c', str(path)] + args
os.execvp('odoo', argv)
