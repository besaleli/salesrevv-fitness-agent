"""Document router."""
from pydantic import BaseModel
from fastapi import APIRouter
from ..models.document import Document
from ..db import SessionLocal
from ..embedding import embedding

router = APIRouter()

class DocumentCreateRequest(BaseModel):
    """Document create request."""
    content: str

class DocumentCreateResponse(BaseModel):
    """Document create response."""
    id: str

@router.post("/create", response_model=DocumentCreateResponse)
async def create_document(document: DocumentCreateRequest):
    """Create document."""

    with SessionLocal() as session:
        document = Document(
            content=document.content,
            embedding=(await embedding([document.content]))[0]
            )
        session.add(document)
        session.commit()
        return DocumentCreateResponse(id=document.id.hex)
