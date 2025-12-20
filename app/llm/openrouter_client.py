#!/usr/bin/env python3
"""
Client OpenRouter pour l'intégration de modèles LLM dans l'API
"""

import requests
from typing import Optional, Dict, List
from app.config import settings

class OpenRouterClient:
    """Client pour interagir avec l'API OpenRouter"""
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.api_url = settings.OPENROUTER_API_URL
        self.default_model = settings.OPENROUTER_MODEL
        self.max_tokens = settings.OPENROUTER_MAX_TOKENS
        self.temperature = settings.OPENROUTER_TEMPERATURE
    
    def _make_request(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Dict:
        """
        Effectue une requête à l'API OpenRouter
        
        Args:
            messages: Liste de messages au format [{"role": "user", "content": "..."}]
            model: Modèle à utiliser (par défaut: celui de la config)
            temperature: Température pour la génération (par défaut: celui de la config)
            max_tokens: Nombre maximum de tokens (par défaut: celui de la config)
        
        Returns:
            Réponse de l'API OpenRouter
        """
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY n'est pas configurée. Veuillez la définir dans votre fichier .env")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/your-repo",  # Optionnel: URL de votre projet
            "X-Title": "Gestion RH API"  # Optionnel: Nom de votre application
        }
        
        payload = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature if temperature is not None else self.temperature,
            "max_tokens": max_tokens or self.max_tokens
        }
        
        try:
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur lors de l'appel à OpenRouter: {str(e)}")
    
    def chat_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Effectue une complétion de chat simple
        
        Args:
            prompt: Le message de l'utilisateur
            system_prompt: Prompt système optionnel
            model: Modèle à utiliser
            temperature: Température pour la génération
            max_tokens: Nombre maximum de tokens
        
        Returns:
            Le contenu de la réponse générée
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self._make_request(messages, model, temperature, max_tokens)
        
        # Extraire le contenu de la réponse
        if "choices" in response and len(response["choices"]) > 0:
            return response["choices"][0]["message"]["content"]
        else:
            raise Exception("Réponse invalide de l'API OpenRouter")
    
    def analyze_prime(
        self,
        type_prime: str,
        motif: Optional[str] = None,
        articles_context: Optional[List[str]] = None
    ) -> str:
        """
        Analyse une prime avec l'IA pour générer des explications intelligentes
        
        Args:
            type_prime: Type de prime à analyser
            motif: Motif de la prime (optionnel)
            articles_context: Liste des articles pertinents (optionnel)
        
        Returns:
            Analyse générée par l'IA
        """
        system_prompt = """Tu es un expert en droit du travail sénégalais spécialisé dans la gestion des primes.
Tu dois fournir des analyses claires, précises et conformes au Code du travail du Sénégal.
Réponds toujours en français."""
        
        context = f"Type de prime: {type_prime}"
        if motif:
            context += f"\nMotif: {motif}"
        if articles_context:
            context += f"\nArticles pertinents: {', '.join(articles_context)}"
        
        prompt = f"""Analyse cette prime selon le Code du travail sénégalais:
{context}

Fournis une analyse détaillée incluant:
1. La conformité légale de ce type de prime
2. Les conditions d'attribution recommandées
3. Les points d'attention importants
4. Les bonnes pratiques"""
        
        return self.chat_completion(prompt, system_prompt=system_prompt)
    
    def generate_explanation(
        self,
        article_code: str,
        article_content: str,
        question: Optional[str] = None
    ) -> str:
        """
        Génère une explication simplifiée d'un article du Code du travail
        
        Args:
            article_code: Code de l'article
            article_content: Contenu de l'article
            question: Question spécifique à répondre (optionnel)
        
        Returns:
            Explication générée par l'IA
        """
        system_prompt = """Tu es un expert en droit du travail sénégalais.
Tu dois expliquer les articles du Code du travail de manière claire et accessible.
Réponds toujours en français."""
        
        prompt = f"""Article {article_code} du Code du travail sénégalais:
{article_content}
"""
        
        if question:
            prompt += f"\nQuestion spécifique: {question}"
        else:
            prompt += "\nExplique cet article de manière claire et concise, en mettant en évidence les points importants pour la gestion des primes."
        
        return self.chat_completion(prompt, system_prompt=system_prompt)
    
    def search_and_explain(
        self,
        keyword: str,
        articles_found: List[Dict]
    ) -> str:
        """
        Recherche et explique les articles trouvés pour un mot-clé
        
        Args:
            keyword: Mot-clé recherché
            articles_found: Liste des articles trouvés
        
        Returns:
            Explication synthétique générée par l'IA
        """
        system_prompt = """Tu es un expert en droit du travail sénégalais.
Tu dois synthétiser et expliquer les articles pertinents trouvés lors d'une recherche.
Réponds toujours en français."""
        
        articles_text = ""
        for i, article in enumerate(articles_found[:5], 1):  # Limiter à 5 articles
            articles_text += f"\n{i}. {article.get('article', 'N/A')}: {article.get('extrait', '')[:200]}...\n"
        
        prompt = f"""Recherche effectuée pour le mot-clé: "{keyword}"

Articles trouvés:
{articles_text}

Synthétise ces articles et explique leur pertinence par rapport au mot-clé recherché.
Fournis une explication claire et structurée."""
        
        return self.chat_completion(prompt, system_prompt=system_prompt, max_tokens=1500)
    
    def get_available_models(self) -> List[str]:
        """
        Récupère la liste des modèles disponibles (nécessite un appel API supplémentaire)
        Note: Cette fonction nécessite une clé API valide
        
        Returns:
            Liste des modèles disponibles
        """
        # Modèles populaires sur OpenRouter
        popular_models = [
            "openai/gpt-4",
            "openai/gpt-4-turbo",
            "openai/gpt-3.5-turbo",
            "anthropic/claude-3-opus",
            "anthropic/claude-3-sonnet",
            "anthropic/claude-3-haiku",
            "google/gemini-pro",
            "meta-llama/llama-2-70b-chat",
            "mistralai/mistral-medium"
        ]
        
        return popular_models

# Instance globale du client
openrouter_client = OpenRouterClient()
