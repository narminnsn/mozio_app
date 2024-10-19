from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# Provider schemas


class ProviderCreate(BaseModel):
    name: str
    email: str
    phone_number: str
    language: str
    currency: str


class ProviderUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    language: Optional[str]
    currency: Optional[str]


# Provider response schema
class ProviderResponse(ProviderCreate):
    id: int

    class Config:
        orm_mode = True  # Enable ORM mode


# ServiceArea schema
class ServiceAreaCreate(BaseModel):
    name: str
    price: float
    geojson: Dict[str, Any]
    provider_id: int


class ServiceAreaUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]
    geojson: Optional[Dict[str, Any]]
    provider_id: Optional[int]


# ServiceArea response schema
class ServiceAreaResponse(ServiceAreaCreate):
    id: int
    provider: ProviderResponse  # Include provider information

    class Config:
        orm_mode = True  # Enable ORM mode
