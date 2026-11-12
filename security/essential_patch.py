"""CRM PRABASE: minimal, idempotent hardening after package extraction."""
from pathlib import Path

server = Path('crm/server.py')
source = server.read_text(encoding='utf-8')

needle = "        self.send_header('Referrer-Policy','no-referrer');self.send_header('X-Frame-Options','DENY')"
addition = "        self.send_header('Permissions-Policy','camera=(), microphone=(), geolocation=(), payment=()')\n        self.send_header('Cross-Origin-Resource-Policy','same-origin')\n        self.send_header('X-Permitted-Cross-Domain-Policies','none')"
if "Cross-Origin-Resource-Policy" not in source:
    if needle not in source:
        raise SystemExit('CRM security patch: required header anchor missing; abort build')
    source = source.replace(needle, needle + '\n' + addition, 1)

needle = "{'Set-Cookie':'session=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0'}"
replacement = "{'Set-Cookie':'session=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0'+('; Secure' if SECURE else '')}"
if replacement not in source:
    if needle not in source:
        raise SystemExit('CRM security patch: required logout anchor missing; abort build')
    source = source.replace(needle, replacement, 1)

server.write_text(source, encoding='utf-8')
print('CRM security baseline applied')
