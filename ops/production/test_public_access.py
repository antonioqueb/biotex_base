"""Configuration security checks; no database or running containers required."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import manager


class PublicAccessTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.root_patch = patch.object(manager, 'ROOT', self.root)
        self.root_patch.start(); self.addCleanup(self.root_patch.stop)
        for environment in ('production', 'qa'):
            (self.root/environment/'config').mkdir(parents=True)

    def test_public_ip_exposes_tls_while_preserving_loopback_origin(self):
        (self.root/'production/public-access.json').write_text(json.dumps({'ip':'2.24.78.58'}))
        manager.render('production')
        config = json.loads((self.root/'production/compose.json').read_text())
        ports = config['services']['nginx']['ports']
        self.assertIn('2.24.78.58:1400:8443', ports)
        self.assertIn('127.0.0.1:1400:8080', ports)
        self.assertNotIn('ports',config['services']['db'])
        self.assertNotIn('ports',config['services']['odoo'])
        nginx = (self.root/'production/config/nginx.conf').read_text()
        self.assertIn('listen 8443 ssl;',nginx)
        self.assertIn('https://2.24.78.58:1400$request_uri',nginx)
        self.assertEqual(nginx.count('xmlrpc/2/db'),2)

    def test_qa_never_publishes_production_endpoint_or_certificate(self):
        (self.root/'qa/public-access.json').write_text(json.dumps({'ip':'2.24.78.58'}))
        manager.render('qa')
        nginx = json.loads((self.root/'qa/compose.json').read_text())['services']['nginx']
        self.assertEqual(nginx['ports'],['127.0.0.1:1401:8080'])
        self.assertFalse(any('/run/tls' in volume for volume in nginx['volumes']))

    def test_nonpublic_address_is_rejected(self):
        (self.root/'production/public-access.json').write_text(json.dumps({'ip':'127.0.0.1'}))
        with self.assertRaises(ValueError):manager.render('production')


if __name__ == '__main__':
    unittest.main()
