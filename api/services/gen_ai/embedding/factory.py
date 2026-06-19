"""Factory helpers for configured embedding providers."""

from typing import Optional

from api.db.db_client import DBClient
from api.services.configuration.registry import ServiceProviders

from .azure_openai_service import AzureOpenAIEmbeddingService
from .base import BaseEmbeddingService
from .openai_service import OpenAIEmbeddingService


def create_embedding_service(
    *,
    db_client: DBClient,
    provider: Optional[str] = None,
    api_key: Optional[str] = None,
    model_id: Optional[str] = None,
    base_url: Optional[str] = None,
    endpoint: Optional[str] = None,
    api_version: Optional[str] = None,
    default_headers: Optional[dict[str, str]] = None,
) -> BaseEmbeddingService:
    """Create an embedding service for the resolved model configuration."""

    if provider == ServiceProviders.AZURE.value and endpoint:
        return AzureOpenAIEmbeddingService(
            db_client=db_client,
            api_key=api_key,
            endpoint=endpoint,
            model_id=model_id or "text-embedding-3-small",
            api_version=api_version or "2024-02-15-preview",
        )

    if provider == ServiceProviders.OLLAMA.value:
        return OpenAIEmbeddingService(
            db_client=db_client,
            api_key=api_key or "ollama",
            model_id=model_id or "rjmalagon/gte-qwen2-1.5b-instruct-embed-f16",
            base_url=base_url or "http://ollama:11434/v1",
        )

    return OpenAIEmbeddingService(
        db_client=db_client,
        api_key=api_key,
        model_id=model_id or "text-embedding-3-small",
        base_url=base_url,
        default_headers=default_headers,
    )
