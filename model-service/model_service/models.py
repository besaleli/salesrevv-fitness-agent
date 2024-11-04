"""Models."""
from typing import List
from pydantic import BaseModel, Field
from .env_settings import MODEL_NAME

class PredictRequest(BaseModel):
    """Predict request."""
    inputs: List[str]


class PredictResponse(BaseModel):
    """Predict response."""
    predictions: List[List[float]]
    ml_model_id: str = Field(default=MODEL_NAME, alias='model_id')
