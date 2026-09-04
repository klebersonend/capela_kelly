import time
import secrets
from collections import defaultdict
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.security import check_password_hash
from app.db import get_db_cursor

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Estrutura em memória para proteção contra força bruta (Rate limiting por IP)
# max 5 tentativas a cada 60 segundos
login_attempts = defaultdict(list)
MAX_ATTEMPTS = 5
ATTEMPT_WINDOW_SECONDS = 60

def is_rate_limited(ip_address: str) -> bool:
    now = time.time()
    # Limpa tentativas antigas
    login_attempts[ip_address] = [t for t in login_attempts[ip_address] if now - t < ATTEMPT_WINDOW_SECONDS]
    return len(login_attempts[ip_address]) >= MAX_ATTEMPTS

def record_failed_attempt(ip_address: str):
    login_attempts[ip_address].append(time.time())

def clear_attempts(ip_address: str):
    if ip_address in login_attempts:
        del login_attempts[ip_address]

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Se já autenticado, redireciona para a área restrita
    if session.get("user_id"):
        return redirect(url_for("restricted.dashboard"))

    client_ip = request.remote_addr or "unknown"

    if request.method == "POST":
        # Validação de CSRF Token
        submitted_token = request.form.get("csrf_token")
        session_token = session.get("csrf_token")
        if not session_token or not submitted_token or not secrets.compare_digest(submitted_token, session_token):
            flash("Sessão ou token inválido. Por favor, tente novamente.", "danger")
            return render_template("login.html")

        # Verificação de rate limiting
        if is_rate_limited(client_ip):
            flash("Muitas tentativas incorretas. Por favor, aguarde 1 minuto.", "warning")
            return render_template("login.html")

        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        if not username or not password:
            flash("Por favor, preencha o usuário e a senha.", "warning")
            return render_template("login.html")

        try:
            with get_db_cursor(commit=True) as cursor:
                # Consulta estritamente parametrizada contra SQL Injection
                cursor.execute(
                    "SELECT id, username, password_hash, nome_completo, perfil FROM usuarios WHERE username = %s;",
                    (username,)
                )
                user = cursor.fetchone()

                if user and check_password_hash(user["password_hash"], password):
                    # Login com sucesso
                    session.clear()  # Previne session fixation
                    session["user_id"] = user["id"]
                    session["username"] = user["username"]
                    session["nome_completo"] = user["nome_completo"]
                    session["perfil"] = user["perfil"]
                    session["csrf_token"] = secrets.token_hex(32)
                    session.permanent = True

                    # Atualiza último acesso
                    cursor.execute(
                        "UPDATE usuarios SET ultimo_acesso = CURRENT_TIMESTAMP WHERE id = %s;",
                        (user["id"],)
                    )
                    clear_attempts(client_ip)
                    flash(f"Bem-vindo(a), {user['nome_completo']}!", "success")
                    return redirect(url_for("restricted.dashboard"))
                else:
                    record_failed_attempt(client_ip)
                    # Mensagem genérica segura (não revela se o usuário existe)
                    flash("Credenciais inválidas. Verifique o usuário e a senha.", "danger")
        except Exception as e:
            current_app.logger.error(f"Erro ao autenticar usuário: {e}")
            flash("Ocorreu um erro no servidor ao processar o login. Tente novamente.", "danger")

    # Gera CSRF token para o formulário GET
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Você encerrou sua sessão com segurança.", "info")
    return redirect(url_for("public.index"))
