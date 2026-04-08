#!/usr/bin/env python3
"""
Fonctions utilitaires pour le chat
"""

from typing import Any, Dict, List, Optional

from app.config import settings


def prepare_articles_for_chat(articles: Optional[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """
    Déduplique par article_id et ordonne pour le prompt : titre (sujet), chapitre, ordre du code.
    """
    if not articles:
        return []
    seen: set = set()
    out: List[Dict[str, Any]] = []
    for a in articles:
        aid = a.get("article_id")
        if aid is None or aid in seen:
            continue
        seen.add(aid)
        out.append(a)
    out.sort(
        key=lambda x: (
            x.get("id_sujet", 0),
            -1 if x.get("chapitre_num") is None else x.get("chapitre_num"),
            x.get("article_id", 0),
        )
    )
    return out


def article_refs_for_chat_response(articles: Optional[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """Métadonnées légères pour la réponse API (pas de contenu)."""
    if not articles:
        return []
    return [
        {
            "article_id": a.get("article_id"),
            "num_article": a.get("num_article"),
            "id_sujet": a.get("id_sujet"),
            "chapitre": a.get("chapitre"),
            "chapitre_num": a.get("chapitre_num"),
        }
        for a in articles
    ]


def create_system_prompt(context: Optional[str] = None, articles: Optional[list] = None) -> str:
    """
    Crée un prompt système pour l'assistant IA
    
    Args:
        context: Contexte additionnel à inclure dans le prompt
        articles: Articles à utiliser (idéalement passés par ``prepare_articles_for_chat`` pour ordre et dédoublonnage)
    
    Returns:
        Le prompt système formaté
    """
    base_prompt = """Tu es un assistant expert en gestion des ressources humaines et en droit du travail sénégalais.
Tu aides les utilisateurs à comprendre les pratiques RH, le droit du travail,
la gestion des primes, et la conformité légale.
Réponds TOUJOURS en français de manière claire et professionnelle.
    
IMPORTANT : Tu dois te baser UNIQUEMENT sur les articles du Code du travail fournis ci-dessous.
Si un article n'est pas fourni, indique que tu n'as pas cette information dans le texte du Code du travail fourni.
Ne donne JAMAIS d'informations générales qui ne sont pas basées sur les articles fournis."""
    
    if not articles:
        articles = []

    if articles:
        base_prompt += "\n\n=== ARTICLES DU CODE DU TRAVAIL À UTILISER ===\n"
        base_prompt += (
            "Les blocs « --- Chapitre … --- » regroupent la rubrique (sous-section) du titre concerné.\n"
        )
        last_chapitre: Optional[str] = None
        for i, article in enumerate(articles, 1):
            chap = article.get("chapitre")
            if chap and chap != last_chapitre:
                base_prompt += f"\n--- {chap} ---\n"
            last_chapitre = chap if chap else last_chapitre

            base_prompt += f"\nArticle {i} - {article.get('num_article', 'N/A')} ({article.get('source', 'Code du travail')})"
            if chap:
                base_prompt += f" [rubrique : {chap}]"
            base_prompt += ":\n"
            contenu = article.get("contenu", "") or ""
            cap = int(getattr(settings, "CHAT_MAX_CHARS_PER_ARTICLE", 4500))
            if len(contenu) > cap:
                note = (
                    "\n[... extrait tronqué pour la limite du modèle — texte intégral via GET /articles/{num_article} — "
                    "variable CHAT_MAX_CHARS_PER_ARTICLE.]\n"
                )
                contenu = contenu[: max(0, cap - len(note))] + note
            base_prompt += f"{contenu}\n"
        base_prompt += "\n=== FIN DES ARTICLES ===\n"
        base_prompt += "\nINSTRUCTION CRITIQUE : Réponds UNIQUEMENT en te basant sur les articles ci-dessus. "
        base_prompt += "Cite les numéros d'articles (L.xxx) lorsque c'est pertinent ; si un chapitre / rubrique est indiqué, tu peux t'en servir pour situer la réponse. "
        base_prompt += "Si la question ne peut pas être répondue avec ces articles, dis-le clairement."
    
    if context:
        base_prompt += f"\n\nContexte additionnel: {context}"
    
    return base_prompt

def format_chat_response(
    response: str,
    model: str,
    sources: Optional[List[Dict[str, Any]]] = None,
) -> dict:
    """
    Formate la réponse du chat
    
    Args:
        response: La réponse générée par le modèle
        model: Le modèle utilisé
        sources: Références aux articles utilisés dans le prompt (sans contenu ni contenu_norm)
    
    Returns:
        Un dictionnaire formaté avec la réponse
    """
    out: Dict[str, Any] = {"response": response, "model": model}
    if sources:
        out["sources"] = sources
    return out

def validate_message(message: str) -> tuple[bool, Optional[str]]:
    """
    Valide un message avant l'envoi
    
    Args:
        message: Le message à valider
    
    Returns:
        Un tuple (is_valid, error_message)
    """
    if not message or not message.strip():
        return False, "Le message ne peut pas être vide"
    
    if len(message) > 5000:
        return False, "Le message est trop long (maximum 5000 caractères)"
    
    return True, None
