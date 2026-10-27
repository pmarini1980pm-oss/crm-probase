# CRM PROBASE

Aplicação CRM PRA•BASE — Casa & Construção.

Este repositório contém apenas código e configuração de implantação. Não incluir banco operacional, credenciais, `.env.local`, custos, margens ou dados reais de clientes.

## Execução no Render

Comando de início: `cd crm && python3 server.py`

Variáveis mínimas de implantação:

- `CRM_HOST=0.0.0.0`
- `PORT` fornecida pelo Render
- `CRM_ORIGIN=https://<servico>.onrender.com`
- `CRM_DB=/var/data/crm.sqlite3` quando houver disco persistente montado em `/var/data`
- `CRM_SETUP_TOKEN=<segredo de ativação inicial>`
- `WHATSAPP_SEND_ENABLED=false`
