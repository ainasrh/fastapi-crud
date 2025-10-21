from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import uuid4




class ProductSchema(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    price: float
    quantity: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


class ProductUpdateSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    updated_at: Optional[datetime] = None