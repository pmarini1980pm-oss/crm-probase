from pathlib import Path

server = Path('crm/server.py')
text = server.read_text()
if "CRM_SETUP_TOKEN" not in text or "setup_token" not in text:
    old = "        allowed_keys(data,['name','email','password','code'])"
    new = "        allowed_keys(data,['name','email','password','code','setup_token'])"
    if old in text:
        text = text.replace(old, new, 1)
    old = "            if db.execute('SELECT COUNT(*) FROM users').fetchone()[0]:raise PermissionError('Administrador já configurado.')\n            if self.client_address[0] not in ('127.0.0.1','::1') or SECURE:raise PermissionError('Configuração inicial somente no computador local.')\n            if len(password)<12:raise ValueError('Use uma senha com pelo menos 12 caracteres.')"
    new = "            if db.execute('SELECT COUNT(*) FROM users').fetchone()[0]:raise PermissionError('Administrador já configurado.')\n            setup_token=os.environ.get('CRM_SETUP_TOKEN','')\n            local_setup=self.client_address[0] in ('127.0.0.1','::1') and not SECURE\n            token_ok=bool(setup_token) and hmac.compare_digest(str(data.get('setup_token','')),setup_token)\n            if not local_setup and not token_ok:raise PermissionError('Código de ativação inválido.')\n            if len(password)<12:raise ValueError('Use uma senha com pelo menos 12 caracteres.')"
    if old not in text:
        raise SystemExit('patch server setup: padrão não encontrado')
    text = text.replace(old, new, 1)

watch_marker = '# DEMO_SEED_WATCHER_V1'
if watch_marker not in text:
    prefix = '''# DEMO_SEED_WATCHER_V1\nimport threading as _demo_threading\nimport time as _demo_time\nfrom seed_demo import seed_if_possible as _demo_seed_if_possible\n\ndef _demo_seed_watch():\n    while True:\n        try:\n            _ok, _status = _demo_seed_if_possible()\n            print('DEMO_SEED', _ok, _status, flush=True)\n            if _ok:\n                return\n        except Exception as _exc:\n            print('DEMO_SEED_ERROR', repr(_exc), flush=True)\n        _demo_time.sleep(5)\n\n_demo_threading.Thread(target=_demo_seed_watch, daemon=True, name='demo-seed').start()\n\n'''
    text = prefix + text

server.write_text(text)

app = Path('crm/static/app.js')
text = app.read_text()
if "setup_token" not in text:
    old = "${setup?field('Seu nome','name','','text',true):''}${field('E-mail','email','','email',true)}"
    new = "${setup?field('Seu nome','name','','text',true)+field('Código de ativação','setup_token','','password',true,'Fornecido pelo responsável pela publicação.'):''}${field('E-mail','email','','email',true)}"
    if old not in text:
        raise SystemExit('patch frontend setup: padrão não encontrado')
    app.write_text(text.replace(old, new, 1))

logo_deploy = Path('crm/static/logo-deploy.png')
logo = Path('crm/static/logo.png')
if logo_deploy.exists():
    logo.write_bytes(logo_deploy.read_bytes())

print('Preparação de publicação concluída.')
