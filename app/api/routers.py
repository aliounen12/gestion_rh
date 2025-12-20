#!/usr/bin/env python3
"""
Routers FastAPI pour l'API de gestion des primes
"""

from fastapi import APIRouter, HTTPException
from typing import List
from app.models import (
    Prime, PrimeResponse, PrimesByTypeResponse, TypesResponse,
    ArticleResponse, SearchResponse, ConformiteResponse, APIInfoResponse, TestResponse,
    OpenRouterChatRequest, OpenRouterChatResponse,
    OpenRouterAnalyzePrimeRequest, OpenRouterAnalyzePrimeResponse,
    OpenRouterExplainArticleRequest, OpenRouterExplainArticleResponse,
    OpenRouterSearchExplainRequest, OpenRouterSearchExplainResponse,
    OpenRouterModelsResponse
)
from app.db import (
    code_articles, primes_db,
    find_relevant_articles, generate_explanations_from_articles,
    add_prime_to_db, get_prime_by_id, get_all_primes, get_primes_by_type,
    get_available_prime_types, get_article_by_code, search_articles_by_keyword,
    get_articles_count
)

# Création des routers
api_router = APIRouter()
primes_router = APIRouter(prefix="/primes", tags=["primes"])
articles_router = APIRouter(prefix="/articles", tags=["articles"])
search_router = APIRouter(prefix="/search", tags=["search"])
openrouter_router = APIRouter(prefix="/openrouter", tags=["openrouter"])

# Routes principales
@api_router.get("/", response_model=APIInfoResponse)
def root():
    """Endpoint racine avec informations sur l'API"""
    return APIInfoResponse(
        message="API de Gestion des Primes - Code du travail Sénégalais",
        version="4.0.0",
        description="API avec base de données PostgreSQL pour la gestion des primes avec conformité légale et intégration OpenRouter IA",
        endpoints={
            "documentation": "/docs",
            "primes_all": "/primes/",
            "prime_by_id": "/primes/{prime_id}",
            "primes_by_type": "/primes/par-type/{type_prime}",
            "types_disponibles": "/types-primes/",
            "prime_exemple": "/primes/exemple",
            "conformite": "/conformite/primes",
            "articles": "/articles/{article_code}",
            "recherche": "/search/articles?keyword=mot-clé",
            "openrouter_chat": "/openrouter/chat",
            "openrouter_analyze": "/openrouter/analyze-prime",
            "openrouter_explain": "/openrouter/explain-article",
            "openrouter_search": "/openrouter/search-explain",
            "openrouter_models": "/openrouter/models",
            "enhanced_prime": "/openrouter/enhanced-prime"
        },
        articles_charges=len(code_articles)
    )

@api_router.get("/test", response_model=TestResponse)
def test_api():
    """Endpoint de test pour vérifier le fonctionnement de l'API"""
    return TestResponse(
        status="OK",
        message="API fonctionnelle avec PostgreSQL",
        articles_charges=len(code_articles),
        primes_enregistrees=len(primes_db),
        types_supportes=[
            "Prime de rendement",
            "Prime d'ancienneté", 
            "Prime de risque",
            "Prime de résultat",
            "Prime d'assiduité",
            "Prime de fin d'année",
            "Prime de transport"
        ]
    )

# Routes pour les primes
@primes_router.post("/", response_model=Prime, status_code=201)
def creer_prime(prime: Prime):
    """
    Création d'une nouvelle prime avec contrôle de conformité
    
    Articles applicables (Code du travail Sénégalais) :
    - Art. L.123 : Liberté de fixation des primes par l'employeur
    - Art. L.125 : Modalités de versement et transparence
    - Art. D.127 : Conditions d'attribution non discriminatoires
    """
    # Détermination des articles et explications basées sur le CSV
    articles = find_relevant_articles(prime.type_prime)
    explications = generate_explanations_from_articles(articles)
    
    prime.conformite = {
        "articles": articles,
        "explications": explications
    }
    
    add_prime_to_db(prime.dict())
    return prime

@primes_router.get("/", response_model=List[Prime])
def get_all_primes_endpoint():
    """
    Obtenir toutes les primes avec leurs références de conformité
    """
    return get_all_primes()

@primes_router.get("/{prime_id}", response_model=Prime)
def get_prime_by_id_endpoint(prime_id: int):
    """
    Obtenir une prime spécifique par son ID
    
    Articles applicables (Code du travail Sénégalais) :
    - Art. L.132 : Droit d'accès aux informations salariales
    - Art. L.134 : Obligation de transparence sur les éléments de rémunération
    """
    prime = get_prime_by_id(prime_id)
    if prime is None:
        raise HTTPException(
            status_code=404,
            detail=f"Prime avec l'ID {prime_id} non trouvée",
            headers={"X-Error-Code": "PRIME_404"}
        )
    return prime

@primes_router.get("/par-type/{type_prime}", response_model=PrimesByTypeResponse)
def get_primes_by_type_endpoint(type_prime: str):
    """
    Récupérer toutes les primes d'un type spécifique
    
    Exemple: GET /primes/par-type/Prime de rendement
    """
    # Décoder l'URL (remplacer %20 par des espaces)
    type_prime_decoded = type_prime.replace('%20', ' ')
    
    primes_du_type = get_primes_by_type(type_prime_decoded)
    
    if not primes_du_type:
        # Afficher les types disponibles pour aider l'utilisateur
        available_types = get_available_prime_types()
        raise HTTPException(
            status_code=404,
            detail={
                "message": f"Aucune prime trouvée pour le type '{type_prime_decoded}'",
                "type_demande": type_prime_decoded,
                "types_disponibles": available_types,
                "suggestion": "Créez d'abord une prime de ce type ou utilisez un type existant"
            },
            headers={"X-Error-Code": "PRIME_TYPE_404"}
        )
    
    return PrimesByTypeResponse(
        type_prime=type_prime_decoded,
        nombre_primes=len(primes_du_type),
        primes=primes_du_type
    )

@primes_router.post("/exemple", response_model=PrimeResponse)
def creer_prime_exemple(type_prime: str = "Prime de rendement", motif: str = "Exemple de prime"):
    """
    Créer une prime d'exemple avec le type et motif spécifiés
    """
    prime = Prime(type_prime=type_prime, motif=motif)
    
    # Détermination des articles et explications basées sur le CSV
    articles = find_relevant_articles(prime.type_prime)
    explications = generate_explanations_from_articles(articles)
    
    prime.conformite = {
        "articles": articles,
        "explications": explications
    }
    
    add_prime_to_db(prime.dict())
    return PrimeResponse(
        message="Prime d'exemple créée avec succès",
        prime=prime
    )

@primes_router.post("/creer-exemples", response_model=dict)
def creer_primes_exemples():
    """
    Créer plusieurs primes d'exemple pour tester l'API
    """
    types_primes_exemples = [
        ("Prime de rendement", "Prime pour excellentes performances"),
        ("Prime de risque", "Prime pour travail en conditions dangereuses"),
        ("Prime d'ancienneté", "Prime pour 5 ans d'ancienneté"),
        ("Prime de résultat", "Prime pour objectifs atteints"),
        ("Prime d'assiduité", "Prime pour parfaite assiduité"),
        ("Prime de fin d'année", "Prime de fin d'année 2024"),
        ("Prime de transport", "Prime pour frais de transport")
    ]
    
    primes_creees = []
    
    for type_prime, motif in types_primes_exemples:
        prime = Prime(type_prime=type_prime, motif=motif)
        
        # Détermination des articles et explications
        articles = find_relevant_articles(prime.type_prime)
        explications = generate_explanations_from_articles(articles)
        
        prime.conformite = {
            "articles": articles,
            "explications": explications
        }
        
        add_prime_to_db(prime.dict())
        primes_creees.append({
            "type_prime": type_prime,
            "motif": motif,
            "articles_conformite": len(articles)
        })
    
    return {
        "message": f"{len(primes_creees)} primes d'exemple créées avec succès",
        "primes_creees": primes_creees,
        "total_primes": len(get_all_primes())
    }

# Routes pour les types de primes
@api_router.get("/types-primes/", response_model=TypesResponse)
def get_available_prime_types_endpoint():
    """
    Récupérer tous les types de primes disponibles
    """
    types_primes = get_available_prime_types()
    
    return TypesResponse(
        types_primes_disponibles=types_primes,
        nombre_types=len(types_primes),
        types_supportes=[
            "Prime de rendement",
            "Prime d'ancienneté", 
            "Prime de risque",
            "Prime de résultat",
            "Prime d'assiduité",
            "Prime de fin d'année",
            "Prime de transport"
        ]
    )

# Routes pour la conformité
@api_router.get("/conformite/primes", response_model=ConformiteResponse)
def documentation_conformite():
    """
    Endpoint de documentation légale basé sur les articles du CSV
    
    Articles du Code du travail Sénégalais chargés depuis articles_structures.csv
    """
    # Obtenir quelques articles pertinents pour la documentation
    key_articles = ["Art.L.2", "Art.L.3", "Art.L.30", "Art.L.31", "Art.L.35", "Art.L.42", "Art.L.47"]
    
    articles_pertinents = []
    for article_code in key_articles:
        content = get_article_by_code(article_code)
        if content:
            # Extraire un résumé du contenu
            summary = content[:200] + "..." if len(content) > 200 else content
            articles_pertinents.append({
                "article": article_code,
                "resume": summary.replace(',,', '').strip()
            })
    
    return ConformiteResponse(
        conformite="Cette API respecte les dispositions du Code du travail Sénégalais relatives aux primes",
        source="Articles chargés depuis PostgreSQL - table public.articles",
        nombre_articles_charges=len(code_articles),
        articles_pertinents=articles_pertinents,
        types_primes_supportes=[
            "Prime de rendement",
            "Prime d'ancienneté", 
            "Prime de risque",
            "Prime de résultat",
            "Prime d'assiduité",
            "Prime de fin d'année",
            "Prime de transport"
        ]
    )

# Routes pour les articles
@articles_router.get("/{article_code}", response_model=ArticleResponse)
def get_article_endpoint(article_code: str):
    """
    Obtenir le contenu d'un article spécifique du Code du travail
    
    Exemple: GET /articles/Art.L.2
    """
    content = get_article_by_code(article_code)
    if content is None:
        raise HTTPException(
            status_code=404,
            detail=f"Article {article_code} non trouvé",
            headers={"X-Error-Code": "ARTICLE_404"}
        )
    
    return ArticleResponse(
        article=article_code,
        contenu=content,
        longueur=len(content)
    )

# Routes pour la recherche
@search_router.get("/articles", response_model=SearchResponse)
def search_articles_endpoint(keyword: str = ""):
    """
    Rechercher des articles par mot-clé dans le contenu
    
    Exemple: GET /search/articles?keyword=travailleur
    """
    if not keyword:
        return SearchResponse(
            mot_cle="",
            nombre_resultats=0,
            articles_trouves=[{
                "message": "Veuillez fournir un mot-clé pour la recherche",
                "exemple": "/search/articles?keyword=travailleur"
            }]
        )
    
    results = search_articles_by_keyword(keyword)
    
    return SearchResponse(
        mot_cle=keyword,
        nombre_resultats=len(results),
        articles_trouves=results
    )

# Routes pour OpenRouter
@openrouter_router.post("/chat", response_model=OpenRouterChatResponse)
def openrouter_chat(request: OpenRouterChatRequest):
    """
    Endpoint générique pour interagir avec OpenRouter
    
    Permet d'envoyer n'importe quelle requête à OpenRouter avec un prompt personnalisé.
    """
    try:
        from app.llm import openrouter_client
        from app.config import settings
        
        response = openrouter_client.chat_completion(
            prompt=request.prompt,
            system_prompt=request.system_prompt,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        return OpenRouterChatResponse(
            response=response,
            model=request.model or settings.OPENROUTER_MODEL
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur OpenRouter: {str(e)}")

@openrouter_router.post("/analyze-prime", response_model=OpenRouterAnalyzePrimeResponse)
def openrouter_analyze_prime(request: OpenRouterAnalyzePrimeRequest):
    """
    Analyse une prime avec l'IA OpenRouter pour générer des explications intelligentes
    
    Utilise l'IA pour analyser la conformité légale et fournir des recommandations.
    """
    try:
        from app.llm import openrouter_client
        from app.config import settings
        
        analyse = openrouter_client.analyze_prime(
            type_prime=request.type_prime,
            motif=request.motif,
            articles_context=request.articles_context
        )
        
        return OpenRouterAnalyzePrimeResponse(
            type_prime=request.type_prime,
            analyse=analyse,
            model=settings.OPENROUTER_MODEL
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur OpenRouter: {str(e)}")

@openrouter_router.post("/explain-article", response_model=OpenRouterExplainArticleResponse)
def openrouter_explain_article(request: OpenRouterExplainArticleRequest):
    """
    Génère une explication simplifiée d'un article du Code du travail avec l'IA
    
    Utilise l'IA pour expliquer un article de manière claire et accessible.
    """
    try:
        from app.llm import openrouter_client
        from app.config import settings
        
        # Récupérer le contenu de l'article
        article_content = get_article_by_code(request.article_code)
        if not article_content:
            raise HTTPException(
                status_code=404,
                detail=f"Article {request.article_code} non trouvé"
            )
        
        explication = openrouter_client.generate_explanation(
            article_code=request.article_code,
            article_content=article_content,
            question=request.question
        )
        
        return OpenRouterExplainArticleResponse(
            article_code=request.article_code,
            explication=explication,
            model=settings.OPENROUTER_MODEL
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur OpenRouter: {str(e)}")

@openrouter_router.post("/search-explain", response_model=OpenRouterSearchExplainResponse)
def openrouter_search_explain(request: OpenRouterSearchExplainRequest):
    """
    Recherche des articles par mot-clé et génère une explication synthétique avec l'IA
    
    Combine la recherche d'articles et l'IA pour fournir une explication complète.
    """
    try:
        from app.llm import openrouter_client
        from app.config import settings
        
        # Rechercher les articles
        articles_found = search_articles_by_keyword(request.keyword)
        
        if not articles_found:
            raise HTTPException(
                status_code=404,
                detail=f"Aucun article trouvé pour le mot-clé '{request.keyword}'"
            )
        
        # Générer l'explication avec l'IA
        explication = openrouter_client.search_and_explain(
            keyword=request.keyword,
            articles_found=articles_found
        )
        
        return OpenRouterSearchExplainResponse(
            keyword=request.keyword,
            nombre_articles=len(articles_found),
            explication=explication,
            model=settings.OPENROUTER_MODEL
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur OpenRouter: {str(e)}")

@openrouter_router.get("/models", response_model=OpenRouterModelsResponse)
def openrouter_get_models():
    """
    Récupère la liste des modèles disponibles sur OpenRouter
    """
    try:
        from app.llm import openrouter_client
        from app.config import settings
        
        models = openrouter_client.get_available_models()
        
        return OpenRouterModelsResponse(
            models=models,
            default_model=settings.OPENROUTER_MODEL
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@openrouter_router.post("/enhanced-prime", response_model=PrimeResponse)
def create_enhanced_prime_with_ai(prime: Prime):
    """
    Crée une prime avec des explications enrichies par l'IA OpenRouter
    
    Combine la logique existante avec l'analyse IA pour des explications plus détaillées.
    """
    try:
        from app.llm import openrouter_client
        from app.config import settings
        
        # Détermination des articles pertinents (logique existante)
        articles = find_relevant_articles(prime.type_prime)
        explications_base = generate_explanations_from_articles(articles)
        
        # Enrichir avec l'IA si disponible
        try:
            analyse_ia = openrouter_client.analyze_prime(
                type_prime=prime.type_prime,
                motif=prime.motif,
                articles_context=articles
            )
            explications_base.append(f"📊 Analyse IA: {analyse_ia[:300]}...")
        except Exception as e:
            # Si l'IA n'est pas disponible, utiliser les explications de base
            print(f"⚠️ OpenRouter non disponible: {e}")
        
        prime.conformite = {
            "articles": articles,
            "explications": explications_base
        }
        
        add_prime_to_db(prime.dict())
        
        return PrimeResponse(
            message="Prime créée avec succès (enrichie par l'IA)",
            prime=prime
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création: {str(e)}")
