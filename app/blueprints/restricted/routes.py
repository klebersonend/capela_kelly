from functools import wraps
from flask import Blueprint, render_template, session, redirect, url_for, flash

restricted_bp = Blueprint("restricted", __name__, url_prefix="/app")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Acesso restrito. Por favor, faça login para continuar.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

@restricted_bp.route("/dashboard")
@login_required
def dashboard():
    # Informações completas e profissionais sobre a atuação da Capelã Kelly Santana
    capela_profile = {
        "nome": "Kelly Santana",
        "titulo": "Capelã Militar | Assistente da Coordenação Estadual (PMs de Cristo)",
        "linkedin": "https://www.linkedin.com/in/kelly-cristina-s-274b0488/",
        "resumo": "Assistente da Coordenação Estadual da Capelania na Associação PMs de Cristo e Capelã especializada em suporte emocional, espiritual e humano para as Forças de Segurança Pública (PMESP), famílias e ambiente hospitalar. Atuação destacada em gerenciamento de crises, elaboração de luto em ocorrências de alto impacto, escuta empática confidencial e formação com apoio de programas do CAES (Centro de Altos Estudos de Segurança).",
        "areas_atuacao": [
            {
                "titulo": "Capelania Militar & Policial",
                "icone": "bi-shield-shaded",
                "descricao": "Apoio humanitário, espiritual e preventivo aos policiais militares da ativa e veteranos da PMESP, além do acolhimento a seus familiares."
            },
            {
                "titulo": "Gestão de Crises e Luto na Segurança",
                "icone": "bi-heart-pulse",
                "descricao": "Acompanhamento compassivo em ocorrências críticas, suporte aos batalhões e acolhimento direto às famílias enlutadas."
            },
            {
                "titulo": "Capelania Hospitalar",
                "icone": "bi-hospital",
                "descricao": "Visitas a leitos, UTIs e enfermarias. Suporte a enfermos e suporte a equipes médicas sob estresse extremo."
            },
            {
                "titulo": "Escuta Ativa e Aconselhamento",
                "icone": "bi-chat-heart",
                "descricao": "Atendimento individual confidencial focado na saúde mental, restauração emocional e fortalecimento pessoal."
            }
        ],
        "principais_competencias": [
            "Assistência Estadual de Capelania (PMs de Cristo)",
            "Suporte à Segurança Pública & PMESP",
            "Gestão de Crises e Apoio ao Luto Crítico",
            "Especialização em Gestão de Segurança Pública (CAES)",
            "Ética, Sigilo Absoluto e Confidencialidade",
            "Escuta Terapêutica e Comunicação Compassiva"
        ],
        "registros_recentes": [
            {"data": "03/09/2026", "tipo": "Capelania Militar", "local": "Batalhão PMESP / Encontro Regional", "status": "Concluído", "detalhe": "Alinhamento com a coordenação de capelania e acolhimento."},
            {"data": "28/08/2026", "tipo": "Atendimento Hospitalar", "local": "Centro Hospitalar da PM (HPM)", "status": "Concluído", "detalhe": "Apoio e oração com familiar de policial internado."},
            {"data": "20/08/2026", "tipo": "Escuta Confidencial", "local": "Gabinete PMs de Cristo", "status": "Concluído", "detalhe": "Sessão de acolhimento e suporte em momento de transição."}
        ]
    }

    return render_template("dashboard.html", user=session, profile=capela_profile)
