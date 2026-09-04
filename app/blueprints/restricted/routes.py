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
    # Informações completas e profissionais sobre a atuação da Capelã Kelly Cristina
    capela_profile = {
        "nome": "Kelly Cristina",
        "titulo": "Capelã & Especialista em Cuidado Integral e Acolhimento Humano",
        "linkedin": "https://www.linkedin.com/in/kelly-cristina-s-274b0488/",
        "resumo": "Profissional dedicada à capelania com vasta experiência em suporte emocional, acolhimento em momentos de crise, escuta empática e assistência hospitalar/humanitária. Foco na restauração da dignidade humana, alívio do sofrimento psicológico/espiritual e fortalecimento de pacientes, famílias e equipes multidisciplinares.",
        "areas_atuacao": [
            {
                "titulo": "Capelania Hospitalar",
                "icone": "bi-hospital",
                "descricao": "Visitas e acompanhamento de pacientes internados, suporte a familiares em UTIs, enfermarias e apoio a equipes de saúde sob estresse emocional."
            },
            {
                "titulo": "Acolhimento ao Luto e Crises",
                "icone": "bi-heart-pulse",
                "descricao": "Intervenção compassiva em perdas repentinas, processos de luto e suporte durante notícias difíceis."
            },
            {
                "titulo": "Escuta Ativa e Empática",
                "icone": "bi-ear",
                "descricao": "Atendimentos individuais confidenciais para alívio de angústia, solidão e suporte ao bem-estar emocional e espiritual."
            },
            {
                "titulo": "Capelania Comunitária e Social",
                "icone": "bi-people",
                "descricao": "Ações solidárias, apoio a comunidades vulneráveis, rodas de conversa e suporte a grupos em momentos de vulnerabilidade social."
            }
        ],
        "principais_competencias": [
            "Escuta Terapêutica e Empatia Avançada",
            "Gestão de Crises e Apoio ao Luto",
            "Ética e Confidencialidade Hospitalar",
            "Comunicação Não-Violenta e Humanização",
            "Suporte Espiritual Inter-religioso e Inclusivo",
            "Integração com Equipes Multidisciplinares de Saúde"
        ],
        "registros_recentes": [
            {"data": "03/09/2026", "tipo": "Atendimento Hospitalar", "local": "Ala de Cuidados Intensivos", "status": "Concluído", "detalhe": "Acompanhamento e suporte emocional a familiar."},
            {"data": "28/08/2026", "tipo": "Escuta Empática", "local": "Gabinete de Atendimento", "status": "Concluído", "detalhe": "Sessão de acolhimento e suporte em momento de transição."},
            {"data": "20/08/2026", "tipo": "Roda de Conversa", "local": "Centro Comunitário", "status": "Concluído", "detalhe": "Mediação sobre saúde mental e acolhimento familiar."}
        ]
    }

    return render_template("dashboard.html", user=session, profile=capela_profile)
