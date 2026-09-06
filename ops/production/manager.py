#!/usr/bin/env python3
"""Root-only production/QA lifecycle. Every destructive operation is fixed to QA."""
import argparse
import configparser
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.request
import urllib.error
import http.cookiejar

ROOT = Path('/opt/bioteczac')
SOURCE = Path(__file__).resolve().parent
ENTERPRISE = ROOT / 'enterprise' / 'addons'
DATABASE = 'bioteczac'
APP_ROLE = 'bioteczac_app'
IMAGES = {
 'odoo': 'odoo@sha256:f99ffac95cb39a0924622ea4118481c95651d9c84187e5b30a21c2cc4419c7dd',
 'postgres': 'postgres@sha256:f1c3376c26f2609ab9f29f71f824103fe2fcd8ee0346485cb6122a4f93df6f94',
 'nginx': 'nginx@sha256:a9ae6f6d078d477e21323310498e5196cb2b7c0aedd9e07b7306612077227d7c',
}
ADDONS = ['biotex_base','biotex_catalog','biotex_contract','biotex_purchase','biotex_purchase_request',
          'biotex_payment_request','biotex_remision','biotex_intercompany','biotex_ux','chatter_always_bottom']
MODULES = ','.join(ADDONS + ['web_enterprise','account_accountant','l10n_mx_edi','l10n_mx_edi_sale',
                            'l10n_mx_reports','l10n_mx_xml_polizas','stock_barcode','sale_management'])


def run(args, *, input=None, output=None, capture=False, check=True):
    return subprocess.run([str(x) for x in args], input=input, text=True, check=check,
                          stdout=output if output else (subprocess.PIPE if capture else None),
                          stderr=subprocess.STDOUT if output else (subprocess.PIPE if capture else None))


def path(environment):
    assert environment in ('production', 'qa')
    return ROOT / environment


def compose(environment, *args, **kwargs):
    return run(['docker','compose','--project-directory',path(environment),
                '-p','bioteczac-' + environment,'-f',path(environment)/'compose.json', *args], **kwargs)


def db_container(environment):
    return 'bioteczac-' + environment + '-db'


def sql(environment, statement):
    return run(['docker','exec','-i',db_container(environment),'psql','-U','postgres','-d','postgres',
                '-At','-v','ON_ERROR_STOP=1'],input=statement,capture=True).stdout.strip()


def db_query(environment, statement):
    return run(['docker','exec','-i',db_container(environment),'psql','-U','postgres','-d',DATABASE,
                '-At','-v','ON_ERROR_STOP=1'],input=statement,capture=True).stdout.strip()


def write_private(target, text, mode=0o600):
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)
    target.chmod(mode)


def prepare(environment):
    target = path(environment)
    target.mkdir(parents=True, exist_ok=True); target.chmod(0o700)
    write_private(target/'.environment', environment + '\n')
    for name in ('data','pgdata','config','secrets','imports','logs','addons'):
        (target/name).mkdir(exist_ok=True)
    os.chown(target/'data',100,101); (target/'data').chmod(0o750)
    for key in ('postgres_password','app_password','manager_password','login_password'):
        secret = target/'secrets'/key
        if not secret.exists(): write_private(secret,'Aa1!' + secrets.token_urlsafe(48) + '\n',0o444)
    (target/'addons').chmod(0o755)
    (target/'imports').chmod(0o755)
    render(environment)


def render(environment):
    target = path(environment); qa = environment == 'qa'; port = 1401 if qa else 1400
    config = configparser.ConfigParser(interpolation=None)
    config['options'] = {
      'addons_path':'/mnt/enterprise,/mnt/extra-addons', 'data_dir':'/var/lib/odoo',
      'db_host':'db','db_port':'5432','db_user':APP_ROLE,'db_name':DATABASE,'dbfilter':'^bioteczac$',
      'list_db':'False','proxy_mode':'True','workers':'1' if qa else '4',
      'max_cron_threads':'0' if qa else '1','gevent_port':'8072','db_maxconn':'16',
      'limit_memory_soft':'805306368','limit_memory_hard':'1073741824',
      'limit_time_cpu':'120','limit_time_real':'240','limit_time_real_cron':'3600',
      'limit_request':'8192','log_level':'info',
      'smtp_server':'127.0.0.1','smtp_port':'9',
      'without_demo':'True', 'http_interface':'0.0.0.0',
    }
    with (target/'config'/'odoo.conf').open('w') as stream: config.write(stream)
    (target/'config'/'odoo.conf').chmod(0o444)
    nginx = '''worker_processes auto;
worker_rlimit_nofile 8192;
pid /tmp/nginx.pid;
error_log /dev/stderr warn;
events { worker_connections 2048; multi_accept on; }
http {
 include /etc/nginx/mime.types;
 default_type application/octet-stream;
 access_log /dev/stdout;
 server_tokens off;
 sendfile on;
 keepalive_timeout 65;
 client_body_temp_path /tmp/client_body;
 proxy_temp_path /tmp/proxy;
 fastcgi_temp_path /tmp/fastcgi;
 uwsgi_temp_path /tmp/uwsgi;
 scgi_temp_path /tmp/scgi;
 proxy_cache_path /tmp/cache levels=1:2 keys_zone=assets:16m max_size=256m inactive=7d;
 map $http_upgrade $connection_upgrade { default upgrade; '' close; }
 map $http_x_forwarded_proto $forwarded_proto { default $scheme; https https; }
 limit_req_zone $binary_remote_addr zone=login:10m rate=12r/m;
 upstream app { server odoo:8069; keepalive 16; }
 upstream bus { server odoo:8072; }
 gzip on; gzip_vary on; gzip_proxied any; gzip_min_length 1024;
 gzip_types text/css application/javascript application/json image/svg+xml;
 server {
  listen 8080;
  server_name _;
  client_max_body_size 50m;
  proxy_connect_timeout 15s; proxy_read_timeout 300s; proxy_send_timeout 300s;
  proxy_http_version 1.1;
  proxy_set_header Host $http_host;
  proxy_set_header X-Forwarded-Host $http_host;
  proxy_set_header X-Forwarded-Proto $forwarded_proto;
  proxy_set_header X-Forwarded-For $remote_addr;
  proxy_set_header X-Real-IP $remote_addr;
  add_header X-Content-Type-Options nosniff always;
  add_header Referrer-Policy strict-origin-when-cross-origin always;
  add_header X-Frame-Options SAMEORIGIN always;
  location ~* ^/(web/database|jsonrpc|xmlrpc/db|xmlrpc/2/db)(/|$) { return 403; }
  location = /web/login { limit_req zone=login burst=8 nodelay; proxy_pass http://app; }
  location = /web/session/authenticate { limit_req zone=login burst=8 nodelay; proxy_pass http://app; }
  location /websocket { proxy_pass http://bus; proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection $connection_upgrade;
    proxy_set_header Host $http_host;
    proxy_set_header X-Forwarded-Host $http_host;
    proxy_set_header X-Forwarded-Proto $forwarded_proto;
    proxy_set_header X-Forwarded-For $remote_addr;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_buffering off; proxy_read_timeout 3600s; }
  location ^~ /web/assets/debug/ { proxy_pass http://app; add_header Cache-Control no-store always; }
  location ~* ^/[^/]+/static/ { proxy_pass http://app; expires 7d; }
  location / { proxy_pass http://app; }
 }
}
'''
    # Only immutable module static files are cached; authenticated attachments are not cached.
    write_private(target/'config'/'nginx.conf',nginx,0o444)
    common = {'restart':'unless-stopped','security_opt':['no-new-privileges:true'],
              'logging':{'driver':'json-file','options':{'max-size':'10m','max-file':'5'}}}
    services = {
      'db': dict(common, image=IMAGES['postgres'],container_name=db_container(environment),
        environment={'POSTGRES_USER':'postgres','POSTGRES_DB':'postgres',
                     'POSTGRES_PASSWORD_FILE':'/run/secrets/postgres_password',
                     'POSTGRES_INITDB_ARGS':'--auth-host=scram-sha-256'},
        secrets=['postgres_password'], volumes=[str(target/'pgdata')+':/var/lib/postgresql/data'],
        networks=['backend'], mem_limit='1g' if qa else '2g',shm_size='256m',
        command=['postgres','-c','max_connections=128','-c','password_encryption=scram-sha-256',
                 '-c','shared_buffers='+('128MB' if qa else '512MB'),'-c','log_min_duration_statement=1000'],
        healthcheck={'test':['CMD-SHELL','pg_isready -U postgres -d postgres'],'interval':'5s','timeout':'3s','retries':30}),
      'odoo': dict(common,image=IMAGES['odoo'],container_name='bioteczac-'+environment+'-odoo',
        entrypoint=['python3','/runtime/start_odoo.py'], command=[], user='100:101',read_only=True,cap_drop=['ALL'],
        tmpfs=['/tmp:rw,nosuid,nodev,size=512m,mode=1777'],
        mem_limit='2g' if qa else '6g',pids_limit=256,
        depends_on={'db':{'condition':'service_healthy'}},networks=['backend','edge'],
        secrets=['app_password','manager_password','login_password'],
        volumes=[str(target/'config'/'odoo.conf')+':/etc/odoo/base.conf:ro',
                 str(target/'data')+':/var/lib/odoo',str(target/'addons')+':/mnt/extra-addons:ro',
                 str(ENTERPRISE)+':/mnt/enterprise:ro',str(ROOT/'runtime')+':/runtime:ro',
                 str(target/'imports')+':/imports:ro'],
        healthcheck={'test':['CMD','python3','-c',"import urllib.request; urllib.request.urlopen('http://127.0.0.1:8069/web/health',timeout=5)"],
                     'interval':'30s','timeout':'8s','retries':5,'start_period':'60s'}),
      'nginx':dict(common,image=IMAGES['nginx'],container_name='bioteczac-'+environment+'-nginx',
        user='101:101',entrypoint=['nginx','-g','daemon off;'],read_only=True,cap_drop=['ALL'],
        mem_limit='256m',pids_limit=64,tmpfs=['/tmp:rw,nosuid,nodev,size=384m,mode=1777'],
        networks=['edge','frontend'] if qa else ['edge'],ports=[f'127.0.0.1:{port}:8080'],depends_on=['odoo'],
        volumes=[str(target/'config'/'nginx.conf')+':/etc/nginx/nginx.conf:ro']),
    }
    spec={'services':services,'networks':{'backend':{'internal':True},'edge':{'internal':qa}},
          'secrets':{key:{'file':str(target/'secrets'/key)} for key in
                     ('postgres_password','app_password','manager_password','login_password')}}
    # Only the QA reverse proxy joins the published bridge. Odoo and PostgreSQL
    # remain on internal networks with no Internet or production route.
    if qa: spec['networks']['frontend'] = {}
    write_private(target/'compose.json',json.dumps(spec,indent=2)+'\n')


def copy_code(environment, source_environment=None):
    target = path(environment)/'addons'
    previous_umask = os.umask(0o022)
    if source_environment:
        assert environment == 'qa' and source_environment == 'production'
        if target.exists(): shutil.rmtree(target)
        target.mkdir()
    for addon in ADDONS:
        folder = target/addon
        if not folder.exists():
            origin = path(source_environment)/'addons'/addon if source_environment else 'https://github.com/antonioqueb/'+addon+'.git'
            run(['git','clone','-q','--no-hardlinks',origin,folder])
        if not source_environment:
            run(['git','-C',folder,'fetch','-q','origin','main'])
            run(['git','-C',folder,'merge','--ff-only','origin/main'],capture=True)
        assert not run(['git','-C',folder,'status','--porcelain'],capture=True).stdout.strip()
        # Remove any credentials embedded in a local remote when QA is cloned.
        if source_environment: run(['git','-C',folder,'remote','set-url','origin','https://github.com/antonioqueb/'+addon+'.git'])
    manifests={addon:run(['git','-C',target/addon,'rev-parse','HEAD'],capture=True).stdout.strip() for addon in ADDONS}
    write_private(path(environment)/'release.json',json.dumps(manifests,indent=2)+'\n')
    os.umask(previous_umask)


def database_ready(environment):
    compose(environment,'up','-d','db')
    for attempt in range(40):
        try:
            if sql(environment,'SELECT 1;')=='1': return
        except subprocess.CalledProcessError: pass
        time.sleep(1)
    raise RuntimeError('PostgreSQL did not become ready')


def create_database(environment):
    password=(path(environment)/'secrets'/'app_password').read_text().strip()
    assert "'" not in password
    if not sql(environment,"SELECT 1 FROM pg_roles WHERE rolname='bioteczac_app';"):
        sql(environment,"SET log_min_duration_statement=-1; CREATE ROLE bioteczac_app LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION PASSWORD '%s';" % password)
    if not sql(environment,"SELECT 1 FROM pg_database WHERE datname='bioteczac';"):
        sql(environment,'CREATE DATABASE bioteczac OWNER bioteczac_app TEMPLATE template0;')
    sql(environment,'REVOKE CONNECT ON DATABASE postgres FROM PUBLIC; GRANT CONNECT ON DATABASE postgres TO bioteczac_app; REVOKE ALL ON DATABASE bioteczac FROM PUBLIC; GRANT CONNECT,TEMP ON DATABASE bioteczac TO bioteczac_app;')
    db_query(environment,'SET ROLE bioteczac_app; CREATE EXTENSION IF NOT EXISTS unaccent; CREATE EXTENSION IF NOT EXISTS pg_trgm; RESET ROLE;')


def shell(environment, script, logfile):
    with logfile.open('w') as stream:
        compose(environment,'run','-T','--rm','--no-deps','odoo','shell','--no-http','--workers=0','--max-cron-threads=0',
                input=script,output=stream)


def health(environment):
    port=1401 if environment=='qa' else 1400
    browser=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    for attempt in range(45):
        try:
            response=browser.open('http://127.0.0.1:%s/web/health' % port,timeout=5)
            if response.status == 200:
                login=browser.open('http://127.0.0.1:%s/web/login' % port,timeout=5)
                if login.status == 200 and b'name="login"' in login.read(): return
        except Exception: pass
        time.sleep(1)
    raise RuntimeError('Odoo login health check failed for ' + environment)


def setup():
    for environment in ('production','qa'): prepare(environment)
    if (db_running('production') and sql('production',"SELECT 1 FROM pg_database WHERE datname='bioteczac';")
        and db_query('production',"SELECT to_regclass('public.ir_config_parameter');")
        and db_query('production',"SELECT value FROM ir_config_parameter WHERE key='bioteczac.production_initialized';")):
        raise RuntimeError('Production is already initialized. setup never resets it.')
    copy_code('production')
    database_ready('production'); create_database('production')
    # PostgreSQL creates the single database through its local administrative
    # socket. The application role never needs database-creation privileges.
    sql('production','ALTER ROLE bioteczac_app NOCREATEDB NOSUPERUSER NOCREATEROLE NOREPLICATION;')
    with (path('production')/'logs'/'initialize.log').open('w') as stream:
        compose('production','run','-T','--rm','--no-deps','odoo','-i',MODULES,'--without-demo=True',
                '--stop-after-init','--no-http','--workers=0','--max-cron-threads=0','--load-language=es_MX',output=stream)
    shell('production',(ROOT/'runtime'/'bootstrap_odoo.py').read_text(),path('production')/'logs'/'bootstrap.log')
    compose('production','up','-d','odoo','nginx'); health('production')
    verify('production')
    print('PRODUCTION_INITIALIZED')


def db_running(environment):
    return run(['docker','inspect','--format','{{.State.Running}}',db_container(environment)],capture=True,check=False).stdout.strip()=='true'


def encryption_setup():
    key=ROOT/'secrets'/'backup.agekey'; public=ROOT/'secrets'/'backup-recipient.txt'
    if not shutil.which('age'): raise RuntimeError('Install age before creating backups')
    if not key.exists():
        key.parent.mkdir(parents=True,exist_ok=True);key.parent.chmod(0o700)
        run(['age-keygen','-o',key],capture=True);key.chmod(0o600)
        write_private(public,run(['age-keygen','-y',key],capture=True).stdout)
    return key,public.read_text().strip()


CORE_TABLES = ('product_template', 'product_product', 'product_category', 'biotex_division',
 'biotex_group', 'biotex_classifier', 'biotex_brand', 'biotex_specialty', 'biotex_equipment',
 'biotex_mt_subclass', 'biotex_generic', 'biotex_family_classifier_rel',
 'biotex_product_specialty_rel', 'biotex_product_equipment_rel', 'sale_order', 'purchase_order',
 'account_move', 'account_move_line', 'account_payment', 'stock_quant', 'stock_move',
 'biotex_contract', 'biotex_remision', 'biotex_remision_mask')


def controls(environment):
    result = {}
    for table in CORE_TABLES:
        if not db_query(environment, "SELECT to_regclass('public.%s');" % table): continue
        query = ("SELECT count(*),coalesce(bit_xor(('x'||substr(md5(row_to_json(t)::text),1,16))::bit(64)::bigint),0),"
                 "coalesce(bit_xor(('x'||substr(md5(row_to_json(t)::text),17,16))::bit(64)::bigint),0) FROM %s t;" % table)
        result[table] = db_query(environment, query)
    return result


def snapshot():
    encryption_setup()
    directory=Path(tempfile.mkdtemp(prefix='snapshot-',dir=ROOT/'work'))
    compose('production','stop','nginx','odoo')
    try:
        with (directory/'database.dump').open('wb') as out:
            subprocess.run(['docker','exec',db_container('production'),'pg_dump','-U','postgres','-Fc','-d',DATABASE],stdout=out,check=True)
        store=path('production')/'data'/'filestore'/DATABASE
        if store.exists(): shutil.copytree(store,directory/'filestore')
        else: (directory/'filestore').mkdir()
        shutil.copy(path('production')/'release.json',directory/'release.json')
        shutil.copy(path('production')/'compose.json',directory/'compose.json')
        shutil.copytree(path('production')/'config',directory/'config')
        write_private(directory/'controls.json',json.dumps(controls('production'),sort_keys=True)+'\n')
        write_private(directory/'snapshot.json',json.dumps({'database':DATABASE,'source':'production',
            'cutoff_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
            'database_uuid':db_query('production',"SELECT value FROM ir_config_parameter WHERE key='database.uuid';")},indent=2)+'\n')
    finally:
        compose('production','up','-d','odoo','nginx')
    health('production')
    with (directory/'database.dump').open('rb') as source:
        subprocess.run(['docker','exec','-i',db_container('production'),'pg_restore','--list'],stdin=source,stdout=subprocess.DEVNULL,check=True)
    return directory


def encrypt_snapshot(directory):
    key,recipient=encryption_setup()
    stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    dest=ROOT/'backups'/('production-'+stamp+'.tar.age')
    archive=subprocess.Popen(['tar','-C',str(directory),'-cf','-','.'],stdout=subprocess.PIPE)
    try:
        subprocess.run(['age','-r',recipient,'-o',str(dest)],stdin=archive.stdout,check=True)
        archive.stdout.close()
        assert archive.wait()==0
    finally:
        if archive.poll() is None: archive.terminate()
    digest_state=hashlib.sha256()
    with dest.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''): digest_state.update(chunk)
    digest=digest_state.hexdigest()
    write_private(dest.with_suffix(dest.suffix+'.sha256'),digest+'  '+dest.name+'\n')
    print('ENCRYPTED_BACKUP',dest)
    return dest


def backup():
    directory=snapshot()
    try: return encrypt_snapshot(directory)
    finally: shutil.rmtree(directory)


def qa_refresh():
    prepare('qa'); database_ready('qa')
    assert (path('qa')/'.environment').read_text().strip()=='qa'
    assert sql('production','SELECT system_identifier FROM pg_control_system();') != sql('qa','SELECT system_identifier FROM pg_control_system();')
    directory=snapshot()
    try:
        archive=encrypt_snapshot(directory)
        # Restore from the encrypted archive, verifying the actual recovery path.
        restored=Path(tempfile.mkdtemp(prefix='restore-',dir=ROOT/'work'))
        key,_=encryption_setup()
        decrypt=subprocess.Popen(['age','-d','-i',str(key),str(archive)],stdout=subprocess.PIPE)
        subprocess.run(['tar','-C',str(restored),'-xf','-'],stdin=decrypt.stdout,check=True)
        decrypt.stdout.close(); assert decrypt.wait()==0
        compose('qa','stop','nginx','odoo')
        sql('qa','DROP DATABASE IF EXISTS bioteczac WITH (FORCE);')
        create_database('qa')
        with (restored/'database.dump').open('rb') as source:
            subprocess.run(['docker','exec','-i',db_container('qa'),'pg_restore','-U','postgres','--role',APP_ROLE,
                            '--no-owner','--no-acl','--exit-on-error','-d',DATABASE],stdin=source,check=True)
        target=path('qa')/'data'/'filestore'/DATABASE
        assert target.resolve()==ROOT/'qa'/'data'/'filestore'/'bioteczac'
        if target.exists(): shutil.rmtree(target)
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copytree(restored/'filestore',target)
        for folder,dirs,files in os.walk(path('qa')/'data'):
            os.chown(folder,100,101)
            for name in files: os.chown(Path(folder)/name,100,101)
        sessions=path('qa')/'data'/'sessions'
        if sessions.exists(): shutil.rmtree(sessions)
        copy_code('qa','production')
        with (path('qa')/'logs'/'neutralize.log').open('w') as stream:
            compose('qa','run','-T','--rm','--no-deps','odoo','neutralize','-d',DATABASE,output=stream)
        shell('qa',(ROOT/'runtime'/'neutralize_qa.py').read_text(),path('qa')/'logs'/'neutralize-extra.log')
        assert controls('qa') == json.loads((restored/'controls.json').read_text()), 'QA business data differs from its production snapshot'
        source_uuid=json.loads((restored/'snapshot.json').read_text())['database_uuid']
        assert source_uuid != db_query('qa',"SELECT value FROM ir_config_parameter WHERE key='database.uuid';")
        assert db_query('qa',"SELECT count(*) FROM ir_cron WHERE active;") == '0'
        compose('qa','up','-d','odoo','nginx'); health('qa'); verify('qa')
        shutil.copy(restored/'snapshot.json',path('qa')/'last-refresh.json')
        print('QA_REFRESH_OK')
    finally:
        shutil.rmtree(directory)
        if 'restored' in locals(): shutil.rmtree(restored)


def verify(environment):
    databases=sql(environment,"SELECT datname FROM pg_database WHERE NOT datistemplate AND datname<>'postgres' ORDER BY datname;")
    assert databases==DATABASE, databases
    assert sql(environment,"SELECT rolcreatedb OR rolsuper OR rolcreaterole OR rolreplication FROM pg_roles WHERE rolname='bioteczac_app';")=='f'
    data=json.loads(db_query(environment,"SELECT value FROM ir_config_parameter WHERE key='bioteczac.catalog_import_report';"))
    assert int(db_query(environment,"SELECT count(*) FROM res_company;"))==3
    assert db_query(environment,"SELECT count(*) FROM res_users WHERE active AND id<>1 AND login<>'soporte@alphacap.com';")=='0'
    assert db_query(environment,"SELECT count(*) FROM ir_module_module WHERE name='biotex_demo' AND state='installed';")=='0'
    files=db_query(environment,"SELECT store_fname,checksum FROM ir_attachment WHERE store_fname IS NOT NULL;").splitlines()
    root=path(environment)/'data'/'filestore'/DATABASE
    for row in files:
        name,checksum=row.split('|')
        assert hashlib.sha1((root/name).read_bytes()).hexdigest()==checksum
    port=1401 if environment=='qa' else 1400
    for route in ('/web/database/manager','/web/database/list','/jsonrpc'):
        try: urllib.request.urlopen('http://127.0.0.1:%s%s'%(port,route));raise AssertionError('Manager route exposed')
        except urllib.error.HTTPError as error: assert error.code==403
    result={'environment':environment,'database':DATABASE,'catalog':data,'attachment_files':len(files),'manager_blocked':True}
    write_private(path(environment)/'verification.json',json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


def main():
    if os.geteuid()!=0: raise SystemExit('Run as root or through sudo')
    os.umask(0o077)
    ROOT.mkdir(exist_ok=True);ROOT.chmod(0o700)
    for name in ('work','backups','secrets','runtime'): (ROOT/name).mkdir(exist_ok=True)
    (ROOT/'runtime').chmod(0o755)
    command=sys.argv[1] if len(sys.argv)>1 else 'status'
    with (ROOT/'maintenance.lock').open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        if command=='setup': setup()
        elif command in ('qa-refresh','sync'): qa_refresh()
        elif command=='backup': backup()
        elif command=='verify':
            for environment in ('production','qa'): verify(environment)
        elif command=='status':
            for environment in ('production','qa'):
                if (path(environment)/'compose.json').exists(): compose(environment,'ps')
        else: raise SystemExit('Usage: bioteczac {setup|qa-refresh|sync|backup|verify|status}')


if __name__=='__main__': main()
