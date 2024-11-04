"""API."""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    """Index page."""
    return "API is up and running <3"
