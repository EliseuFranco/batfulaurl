from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from sqlalchemy.sql import func
from typing import Optional
from .urls_model import URLS

class Clicks(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    shortned_url_id: int = Field(foreign_key='urls.id', nullable=False)
    ip_address: str = Field(index=True)
    country: str = Field(nullable=False)
    city: str = Field(nullable=False)
    clicked_at: datetime = Field(default=func.now())

    url: Optional[URLS] = Relationship(back_populates="clicks")