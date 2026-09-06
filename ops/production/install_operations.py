#!/usr/bin/env python3
"""Install operator entrypoints and a daily encrypted backup on the dedicated host."""
import os
import subprocess
from pathlib import Path


def install():
    if os.geteuid() != 0:
        raise SystemExit('Run as root')
    manager = Path('/opt/bioteczac/runtime/manager.py')
    if not manager.exists():
        raise SystemExit('Production runtime is not installed')
    files = {
        '/usr/local/sbin/bioteczac': ('#!/bin/sh\nexec /usr/bin/python3 /opt/bioteczac/runtime/manager.py "$@"\n', 0o700),
        '/root/bioteczac_qa_manager.sh': ('#!/bin/sh\ncase "${1:-sync}" in\n sync|qa-refresh) exec /usr/local/sbin/bioteczac qa-refresh ;;\n *) echo "Uso: $0 [sync]" >&2; exit 2 ;;\nesac\n', 0o700),
        '/etc/systemd/system/bioteczac-backup.service': ('''[Unit]
Description=Bioteczac consistent encrypted database and filestore backup
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
User=root
UMask=0077
ExecStart=/usr/local/sbin/bioteczac backup
Nice=10
IOSchedulingClass=best-effort
IOSchedulingPriority=7
TimeoutStartSec=1h
''', 0o644),
        '/etc/systemd/system/bioteczac-backup.timer': ('''[Unit]
Description=Daily Bioteczac encrypted backup at 03:00 Monterrey time

[Timer]
OnCalendar=*-*-* 09:00:00 UTC
RandomizedDelaySec=300
Persistent=true

[Install]
WantedBy=timers.target
''', 0o644),
    }
    for filename, (content, mode) in files.items():
        path = Path(filename)
        path.write_text(content)
        path.chmod(mode)
    subprocess.run(['systemctl', 'daemon-reload'], check=True)
    subprocess.run(['systemctl', 'enable', '--now', 'bioteczac-backup.timer'], check=True)
    print('OPERATOR_COMMANDS_AND_BACKUP_TIMER_INSTALLED')


if __name__ == '__main__':
    install()
