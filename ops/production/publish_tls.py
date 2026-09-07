#!/usr/bin/env python3
"""Certbot deploy hook: publish a verified certificate for the production proxy only."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path('/opt/bioteczac')
LINEAGE = Path('/etc/letsencrypt/live/bioteczac-ip')


def command(*args):
    return subprocess.check_output(args, stderr=subprocess.STDOUT)


def main():
    if os.geteuid() != 0:
        raise SystemExit('Run as root')
    lineage = Path(os.environ.get('RENEWED_LINEAGE', str(LINEAGE)))
    if lineage != LINEAGE:
        raise SystemExit('Unexpected certificate lineage')
    # The endpoint is an explicit operator setting; QA never reads it.
    ip = json.loads((ROOT/'public-ip-request.json').read_text())['ip']
    command('openssl','x509','-in',str(lineage/'cert.pem'),'-noout','-checkip',ip)
    command('openssl','x509','-in',str(lineage/'cert.pem'),'-noout','-checkend','86400')
    command('openssl','verify','-purpose','sslserver','-untrusted',str(lineage/'chain.pem'),str(lineage/'cert.pem'))
    certificate_key = command('openssl','x509','-in',str(lineage/'cert.pem'),'-pubkey','-noout')
    private_key = command('openssl','pkey','-in',str(lineage/'privkey.pem'),'-pubout')
    if certificate_key != private_key:
        raise SystemExit('Certificate/private key mismatch')
    with (ROOT/'maintenance.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        tls = ROOT/'production'/'tls'
        digest = hashlib.sha256((lineage/'cert.pem').read_bytes()).hexdigest()[:24]
        release = tls/'releases'/digest
        release.mkdir(parents=True,exist_ok=True)
        for directory in (tls,tls/'releases',release):
            os.chown(directory,101,101);directory.chmod(0o700)
        for filename in ('fullchain.pem','privkey.pem'):
            destination = release/filename
            destination.write_bytes((lineage/filename).read_bytes())
            os.chown(destination,101,101);destination.chmod(0o600)
        current = tls/'current'
        previous = os.readlink(current) if current.is_symlink() else None
        pending = tls/'pending'
        if pending.is_symlink():pending.unlink()
        pending.symlink_to('releases/'+digest)
        pending.replace(current)
        running = command('docker','inspect','--format','{{.State.Running}}','bioteczac-production-nginx').strip()==b'true'
        try:
            if running and (ROOT/'production'/'public-access.json').exists():
                command('docker','exec','bioteczac-production-nginx','nginx','-t')
                command('docker','exec','bioteczac-production-nginx','nginx','-s','reload')
        except Exception:
            if previous:
                pending.symlink_to(previous);pending.replace(current)
            raise
        print('PRODUCTION_TLS_PUBLISHED',digest)


if __name__ == '__main__':
    main()
