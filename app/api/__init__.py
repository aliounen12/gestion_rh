"""
Module API - Routers FastAPI
"""

from .assistant import assistant_router, health_router

__all__ = [
    "assistant_router",
    "health_router"
]

