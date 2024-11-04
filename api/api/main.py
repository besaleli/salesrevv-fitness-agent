"""API."""
from fastapi import FastAPI
from .db import Base, engine, DATABASE_URL
from .routers.document import router as document_router

print(DATABASE_URL)
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(document_router, prefix="/document", tags=["document"])

@app.get("/")
def index():
    """Index page."""
    return "API is up and running <3"
