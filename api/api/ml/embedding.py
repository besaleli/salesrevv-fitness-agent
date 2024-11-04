"""Embedding."""
from typing import List
import aiohttp

MODEL_SERVICE_URL = "http://model_service:8070/predict"

async def embedding(documents: List[str]) -> List[List[float]]:
    """Embedding.

    Args:
        documents (List[str]): Documents to embed.

    Returns:
        List[List[float]]: Embeddings.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(MODEL_SERVICE_URL, json={"inputs": documents}) as response:
            response.raise_for_status()
            return (await response.json())["predictions"]
