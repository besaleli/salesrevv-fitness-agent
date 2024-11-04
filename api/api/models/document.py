"""Document models."""
from typing import List
import uuid
from sqlalchemy import UUID, Text
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector
from ..db import Base

class Document(Base):
    """Document model."""
    __tablename__ = "document"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content: Mapped[str] = mapped_column(Text(), nullable=False)
    embedding: Mapped[List[str]] = mapped_column(Vector(), nullable=False)
