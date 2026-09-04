import os
from datetime import timedelta
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configurações de Segurança
    secret_key = os.environ.get("SECRET_KEY", "c89f2a945d8b7461c28fa1993478bf104ea29d779633e9b119283472")
    app.config["SECRET_KEY"] = secret_key
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=4)
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    
    # Se em produção ou no Render, força cookies seguros HTTPS
    is_prod = os.environ.get("FLASK_ENV") == "production" or os.environ.get("RENDER") == "true" or os.environ.get("SESSION_COOKIE_SECURE", "false").lower() == "true"
    app.config["SESSION_COOKIE_SECURE"] = is_prod

    # Registro de Blueprints
    from app.blueprints.public.routes import public_bp
    from app.blueprints.auth.routes import auth_bp
    from app.blueprints.restricted.routes import restricted_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(restricted_bp)

    # Auto-inicialização segura das tabelas e usuários na inicialização do serviço
    if os.environ.get("DATABASE_URL"):
        try:
            from app.init_db import init_database
            init_database()
            app.logger.info("Banco de dados verificado e inicializado com sucesso.")
        except Exception as e:
            app.logger.warning(f"Inicialização do banco em background pendente: {e}")

    # Headers de Segurança HTTP (OWASP Best Practices)
    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://code.jquery.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net; "
            "img-src 'self' data: https:;"
        )
        if is_prod:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

    return app
