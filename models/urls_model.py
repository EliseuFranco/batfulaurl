from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from sqlalchemy.sql import func
from typing import Optional, List

class URLS(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    slug: str = Field(index=True)
    original_url: str = Field(nullable=False)
    created_at: datetime = Field(default=func.now())

    user_id: Optional[int] = Field(foreign_key='users.id', nullable=True)  # pode ser None para anonimos
    owner: Optional["Users"] = Relationship(back_populates='urls')

    clicks: List["Clicks"] = Relationship(back_populates='url')

