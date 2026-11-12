# Baseline essencial — CRM PRABASE (proposta de publicação)

**Status:** código preparado na branch `security/essential-baseline-2026-11`; **não implantado** em produção. A branch `main` e o serviço Render permanecem inalterados.

## Inventário do que já foi identificado no código
- Sessões protegidas por cookie `HttpOnly`, `SameSite=Strict`, CSRF e `Secure` quando HTTPS.
- Senhas PBKDF2-HMAC-SHA256 e MFA TOTP opcional.
- Autorização por perfil e escopo de cliente/oportunidade aplicada no backend.
- Política CSP, HSTS quando HTTPS, `no-store`, `nosniff` e `X-Frame-Options: DENY`.
- Integração externa com IA não implementada no servidor examinado; configuração de envio real por WhatsApp controlada separadamente.

## Proteções adicionadas nesta branch
1. `Permissions-Policy` desativa câmera, microfone, geolocalização e pagamento no contexto da aplicação.
2. `Cross-Origin-Resource-Policy: same-origin` e `X-Permitted-Cross-Domain-Policies: none` reforçam a política de recursos.
3. Cookie de logout recebe o atributo `Secure` quando o acesso é HTTPS, alinhado ao login.
4. Patch é idempotente e falha caso mude a estrutura do código; reduz risco de deploy silencioso sem proteção.

## Segurança de dados e IA — requisitos ainda pendentes
- Verificar a matriz de acesso de todos os perfis com dados sintéticos em homologação.
- Construir o gateway de autorização e minimização para PRIMO antes de integrar o modelo ou ferramentas externas.
- Proibir, por padrão, envio de dados pessoais/comerciais a modelos externos; introduzir política explícita de destinatários, finalidade, retenção, transferência e mascaramento.
- Criar DLP de saída e auditoria de exportação (sem habilitar bloqueios antes de testes).
- Auditar segredos no repositório e rotacionar o código de ativação anteriormente exposto, sem publicá-lo no GitHub.

## Bloqueador de produção
Serviço Render no plano gratuito com SQLite em armazenamento temporário. Um deploy/restart pode eliminar usuários, dados e sessões. **Não executar deploy até confirmar migração e cópia restaurável da base**, ou decisão explícita de descartar todos os dados existentes.
A produção não foi modificada por esta branch; auto-deploy permanece desabilitado.

## Validação local
A aplicação da alteração ao código-fonte de referência passou nos 14 testes de regressão em 12/11/2026. Não equivale a teste de homologação do pacote efetivamente executado no Render. Foram observados avisos `ResourceWarning` de conexões SQLite.

## Critérios de liberação
Backup verificável e restauração testada; homologação usando cópia sanitizada; testes de autorização por perfil; verificação de cabeçalhos e cookies; revisão humana da política DLP/IA; plano de reversão; autorização final de deploy.
