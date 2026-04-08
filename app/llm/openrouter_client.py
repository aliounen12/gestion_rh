#!/usr/bin/env python3
"""
Client OpenRouter pour les interactions avec les modèles LLM
"""

import json
import requests
from typing import Optional, Tuple
from app.config import settings


# Valeurs typiques envoyées par erreur (Swagger « string », .env placeholder, etc.)
_INVALID_MODEL_PLACEHOLDERS = frozenset(
    {
        "",
        "string",
        "null",
        "none",
        "undefined",
        "model",
        "default",
        "optional",
        "your-model-here",
    }
)


def _is_valid_openrouter_model_id(model_id: str) -> bool:
    if not model_id or not isinstance(model_id, str):
        return False
    m = model_id.strip()
    if not m:
        return False
    if m.lower() in _INVALID_MODEL_PLACEHOLDERS:
        return False
    # OpenRouter attend un slug du type fournisseur/modèle
    if "/" not in m:
        return False
    return True


def resolve_openrouter_model(requested: Optional[str], configured_default: str) -> str:
    """
    Choisit un modèle utilisable pour l'API OpenRouter.
    Ignore les placeholders (ex. \"string\") et les IDs sans « / ».
    """
    fallback = getattr(
        settings, "OPENROUTER_MODEL_FALLBACK", "openai/gpt-4o-mini"
    )
    req = (requested or "").strip() if requested else ""
    cfg = (configured_default or "").strip() if configured_default else ""

    if _is_valid_openrouter_model_id(req):
        return req
    if _is_valid_openrouter_model_id(cfg):
        return cfg
    if _is_valid_openrouter_model_id(fallback):
        return fallback.strip()
    return "openai/gpt-4o-mini"


def _approx_tokens(text: str) -> int:
    return max(0, len(text) // 4)


def _openrouter_error_body(response: requests.Response) -> str:
    raw = (response.text or "").strip()
    try:
        data = response.json()
        err = data.get("error")
        if isinstance(err, dict) and err.get("message"):
            return str(err["message"])
        if isinstance(err, str):
            return err
    except (json.JSONDecodeError, ValueError, TypeError):
        pass
    return raw[:4000] if raw else "(corps de réponse vide)"


def _clamp_prompt_chars(
    system_prompt: Optional[str], user_prompt: str
) -> Tuple[Optional[str], str]:
    """
    Réduit le prompt système si nécessaire pour rester sous OPENROUTER_MAX_TOTAL_PROMPT_CHARS.
    """
    max_total = int(getattr(settings, "OPENROUTER_MAX_TOTAL_PROMPT_CHARS", 85000))
    sys = system_prompt or ""
    user = user_prompt or ""
    overhead = 100
    if len(sys) + len(user) + overhead <= max_total:
        return system_prompt, user

    user_cap = min(len(user), max_total // 4)
    user_fit = user[:user_cap] if len(user) > user_cap else user
    if len(user) > user_cap:
        user_fit = user_fit[:-80] + "\n[... message utilisateur tronqué ...]\n"

    room = max_total - len(user_fit) - overhead
    if room < 500:
        return (
            "[Erreur: impossible de tenir le prompt dans la limite configurée.]",
            user_fit,
        )
    if len(sys) <= room:
        return (sys if system_prompt else None, user_fit)

    suffix = "\n\n[... prompt système tronqué — réduire CHAT_MAX_ARTICLES / CHAT_MAX_CHARS_PER_ARTICLE ou augmenter OPENROUTER_MAX_TOTAL_PROMPT_CHARS.]\n"
    take = max(0, room - len(suffix))
    return (sys[:take] + suffix, user_fit)


class OpenRouterClient:
    """Client pour l'API OpenRouter"""
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.api_url = settings.OPENROUTER_API_URL
        self.default_model = resolve_openrouter_model(
            None, settings.OPENROUTER_MODEL
        )
        self.max_tokens = settings.OPENROUTER_MAX_TOKENS
        self.temperature = settings.OPENROUTER_TEMPERATURE
    
    def chat_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Effectue une requête de chat completion
        
        Args:
            prompt: Le message de l'utilisateur
            system_prompt: Le prompt système (optionnel)
            model: Le modèle à utiliser (optionnel)
            temperature: La température pour la génération (optionnel)
        
        Returns:
            La réponse générée par le modèle
        """
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY n'est pas configurée")

        system_prompt, prompt = _clamp_prompt_chars(system_prompt, prompt)

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        input_budget = int(getattr(settings, "OPENROUTER_INPUT_TOKEN_BUDGET", 12000))
        input_approx = _approx_tokens(system_prompt or "") + _approx_tokens(prompt)
        # Laisser de la marge : input + max_tokens ne doit pas dépasser la fenêtre du modèle
        safe_max_out = max(256, input_budget - input_approx - 256)
        max_tokens = min(self.max_tokens, safe_max_out)

        model_id = resolve_openrouter_model(model, self.default_model)

        payload = {
            "model": model_id,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature if temperature is not None else self.temperature
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/aliounen12/gestion_rh",  # Optionnel mais recommandé
            "X-Title": "ChatRH API"  # Optionnel mais recommandé
        }
        
        try:
            # Timeout réduit pour Vercel (10s gratuit, 60s pro)
            # On utilise 8s pour laisser une marge
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=8
            )
            
            # Vérifier le statut de la réponse
            if response.status_code == 401:
                error_detail = response.text
                raise ValueError(
                    f"Erreur d'authentification (401): Vérifiez que votre clé API OpenRouter est valide. "
                    f"Détail: {error_detail}"
                )

            if response.status_code == 400:
                raise ValueError(
                    "Requête refusée par OpenRouter (400). "
                    + _openrouter_error_body(response)
                )

            response.raise_for_status()
            
            data = response.json()
            
            # Vérifier que la réponse contient les données attendues
            if "choices" not in data or len(data["choices"]) == 0:
                raise ValueError("Réponse OpenRouter invalide: aucune choice trouvée")
            
            return data["choices"][0]["message"]["content"]
        
        except requests.exceptions.HTTPError as e:
            resp = e.response
            if resp is not None and resp.status_code == 401:
                raise ValueError(
                    f"Erreur d'authentification (401): Vérifiez que votre clé API OpenRouter est valide et active. "
                    f"Assurez-vous que la clé dans le fichier .env est correcte."
                )
            if resp is not None and resp.status_code == 400:
                raise ValueError(
                    "Requête refusée par OpenRouter (400). "
                    + _openrouter_error_body(resp)
                )
            detail = ""
            if resp is not None:
                detail = _openrouter_error_body(resp)
            raise ValueError(
                f"Erreur HTTP lors de l'appel à OpenRouter: {str(e)}"
                + (f" — {detail}" if detail else "")
            )
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Erreur lors de l'appel à OpenRouter: {str(e)}")
