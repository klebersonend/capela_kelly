# Capela Kelly - Portal de Capelania & Acolhimento Humano

Aplicação web moderna, segura e com tema claro dedicada ao trabalho de Capelania da Kelly Santana.

## Tecnologias
- **Backend:** Python 3 + Flask (Blueprints, Jinja2, Werkzeug)
- **Frontend:** HTML5, CSS3 Customizado, Bootstrap 5, jQuery, Bootstrap Icons
- **Banco de Dados:** PostgreSQL (Render Postgres) via `psycopg2`
- **Hospedagem:** Render Web Service + Render PostgreSQL

## Segurança Implementada
- Autenticação com hash criptográfico `scrypt`.
- Consultas SQL 100% parametrizadas contra SQL Injection.
- Proteção contra Cross-Site Request Forgery (CSRF).
- Proteção contra força bruta com Rate Limiting por IP.
- Headers de segurança HTTP (CSP, X-Content-Type-Options, X-Frame-Options, Referrer-Policy).
- Cookies de sessão seguros (`HttpOnly`, `SameSite=Lax`).

## Usuários Iniciais
- `end` (Administrador)
- `kelly` (Capelã)
