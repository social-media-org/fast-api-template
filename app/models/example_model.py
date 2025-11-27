"""Example Pydantic models for demonstration."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ExampleBase(BaseModel):
    """Base model for Example entity."""

    name: str = Field(..., min_length=1, max_length=100, description="Example name")
    description: Optional[str] = Field(None, max_length=500, description="Example description")
    is_active: bool = Field(default=True, description="Active status")


class ExampleCreate(ExampleBase):
    """Model for creating a new Example."""

    pass


class ExampleUpdate(BaseModel):
    """Model for updating an existing Example."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None


class ExampleInDB(ExampleBase):
    """Model for Example stored in database."""

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="Unique identifier (UUID)")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ExampleResponse(ExampleInDB):
    """Model for Example API response."""

    pass
