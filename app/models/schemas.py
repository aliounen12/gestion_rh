#!/usr/bin/env python3
"""
Schémas Pydantic pour l'API de gestion des primes
"""

from pydantic import BaseModel
from typing import List, Optional, Dict

class Prime(BaseModel):
    """Schéma pour une prime"""
    type_prime: str  # Ex: "Prime de résultat", "Prime d'ancienneté", etc.
    motif: Optional[str] = None
    conformite: Dict[str, List[str]] = {
        "articles": [],
        "explications": []
    }

class PrimeResponse(BaseModel):
    """Schéma de réponse pour une prime créée"""
    message: str
    prime: Prime

class PrimesByTypeResponse(BaseModel):
    """Schéma de réponse pour les primes par type"""
    type_prime: str
    nombre_primes: int
    primes: List[Prime]

class TypesResponse(BaseModel):
    """Schéma de réponse pour les types de primes"""
    types_primes_disponibles: List[str]
    nombre_types: int
    types_supportes: List[str]

class ArticleResponse(BaseModel):
    """Schéma de réponse pour un article"""
    article: str
    contenu: str
    longueur: int

class SearchResponse(BaseModel):
    """Schéma de réponse pour la recherche d'articles"""
    mot_cle: str
    nombre_resultats: int
    articles_trouves: List[Dict]

class ConformiteResponse(BaseModel):
    """Schéma de réponse pour la documentation de conformité"""
    conformite: str
    source: str
    nombre_articles_charges: int
    articles_pertinents: List[Dict]
    types_primes_supportes: List[str]

class APIInfoResponse(BaseModel):
    """Schéma de réponse pour les informations de l'API"""
    message: str
    version: str
    description: str
    endpoints: Dict
    articles_charges: int

class TestResponse(BaseModel):
    """Schéma de réponse pour le test de l'API"""
    status: str
    message: str
    articles_charges: int
    primes_enregistrees: int
    types_supportes: List[str]

# Schémas pour OpenRouter
class OpenRouterChatRequest(BaseModel):
    """Schéma pour une requête de chat OpenRouter"""
    prompt: str
    system_prompt: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None

class OpenRouterChatResponse(BaseModel):
    """Schéma de réponse pour une requête de chat OpenRouter"""
    response: str
    model: str
    tokens_used: Optional[int] = None

class OpenRouterAnalyzePrimeRequest(BaseModel):
    """Schéma pour analyser une prime avec OpenRouter"""
    type_prime: str
    motif: Optional[str] = None
    articles_context: Optional[List[str]] = None

class OpenRouterAnalyzePrimeResponse(BaseModel):
    """Schéma de réponse pour l'analyse d'une prime"""
    type_prime: str
    analyse: str
    model: str

class OpenRouterExplainArticleRequest(BaseModel):
    """Schéma pour expliquer un article avec OpenRouter"""
    article_code: str
    question: Optional[str] = None

class OpenRouterExplainArticleResponse(BaseModel):
    """Schéma de réponse pour l'explication d'un article"""
    article_code: str
    explication: str
    model: str

class OpenRouterSearchExplainRequest(BaseModel):
    """Schéma pour rechercher et expliquer avec OpenRouter"""
    keyword: str

class OpenRouterSearchExplainResponse(BaseModel):
    """Schéma de réponse pour la recherche et explication"""
    keyword: str
    nombre_articles: int
    explication: str
    model: str

class OpenRouterModelsResponse(BaseModel):
    """Schéma de réponse pour les modèles disponibles"""
    models: List[str]
    default_model: str
