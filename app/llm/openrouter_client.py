#!/usr/bin/env python3
"""
Client OpenRouter pour les interactions avec les modèles LLM
"""

import requests
from typing import Optional
from app.config import settings

class OpenRouterClient:
    """Client pour l'API OpenRouter"""
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.api_url = settings.OPENROUTER_API_URL
        self.default_model = settings.OPENROUTER_MODEL
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
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": model or self.default_model,
            "messages": messages,
            "max_tokens": self.max_tokens,
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
            
            response.raise_for_status()
            
            data = response.json()
            
            # Vérifier que la réponse contient les données attendues
            if "choices" not in data or len(data["choices"]) == 0:
                raise ValueError("Réponse OpenRouter invalide: aucune choice trouvée")
            
            return data["choices"][0]["message"]["content"]
        
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise ValueError(
                    f"Erreur d'authentification (401): Vérifiez que votre clé API OpenRouter est valide et active. "
                    f"Assurez-vous que la clé dans le fichier .env est correcte."
                )
            raise ValueError(f"Erreur HTTP lors de l'appel à OpenRouter: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Erreur lors de l'appel à OpenRouter: {str(e)}")
