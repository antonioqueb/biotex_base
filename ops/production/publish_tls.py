#!/usr/bin/env python3
"""Certbot hook: publish TLS separately to each explicitly enabled proxy."""
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
    # The certificate identifies the server IP; each environment has its own listener.
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
        digest = hashlib.sha256((lineage/'cert.pem').read_bytes()).hexdigest()[:24]
        targets = ['production']
        if (ROOT/'qa'/'public-access.json').exists():targets.append('qa')
        for environment in targets:
            settings = ROOT/environment/'public-access.json'
            if settings.exists() and json.loads(settings.read_text())['ip'] != ip:
                raise SystemExit('Certificate does not match an enabled environment')
        for environment in targets:
            publish_environment(environment,lineage,digest)


def publish_environment(environment,lineage,digest):
    tls = ROOT/environment/'tls'
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
    container = 'bioteczac-'+environment+'-nginx'
    running = command('docker','inspect','--format','{{.State.Running}}',container).strip()==b'true'
    try:
        if running and (ROOT/environment/'public-access.json').exists():
            command('docker','exec',container,'nginx','-t')
            command('docker','exec',container,'nginx','-s','reload')
    except Exception:
        if previous:
            pending.symlink_to(previous);pending.replace(current)
        raise
    print('TLS_PUBLISHED',environment,digest)


if __name__ == '__main__':
    main()
