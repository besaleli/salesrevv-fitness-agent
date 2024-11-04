"""Model service."""
import logging
from fastapi import FastAPI
from .encoder import Encoder
from .models import PredictRequest, PredictResponse

logger = logging.getLogger(__name__)

encoder = Encoder()

app = FastAPI()

@app.get("/")
async def index():
    """Index page."""
    return "API is up and running <3"

@app.get("/health")
async def health():
    """Health."""
    return "OK"

@app.get("/predict")
async def predict(request: PredictRequest):
    """Predict."""
    return PredictResponse(
        predictions=await encoder.encode(request.inputs)
        )
