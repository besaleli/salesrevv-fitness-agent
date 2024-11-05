"""API."""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from .db import Base, engine
from .routers.document import router as document_router
from .routers.message import router as message_router

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app_: FastAPI):
    """Lifespan function."""
    logger.error("Starting up %s...", app_.title)
    logger.error("Creating vector extension...")
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        conn.commit()

    logger.error("Creating metadata...")
    Base.metadata.create_all(bind=engine)
    yield

    logger.info("Shutting down %s...", app_.title)

app = FastAPI(lifespan=lifespan)
app.include_router(document_router, prefix="/document", tags=["document"])
app.include_router(message_router, prefix="/message", tags=["message"])

@app.get("/")
async def index():
    """Index page."""
    return "API is up and running <3"
