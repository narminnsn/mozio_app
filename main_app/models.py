from sqlalchemy import Column, String, Float, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship
from main_app.database import Base


# Provider model
class Provider(Base):
    __tablename__ = "providers"  # Table name
    id = Column(Integer, primary_key=True, autoincrement=True)  # Provider ID
    name = Column(String, index=True)  # Provider name
    email = Column(String, unique=True, index=True)  # Provider email
    phone_number = Column(String)  # Provider phone number
    language = Column(String)  # Provider language
    currency = Column(String)  # Provider currency

    # Relationship with ServiceArea
    service_areas = relationship("ServiceArea", back_populates="provider")


# ServiceArea model
class ServiceArea(Base):
    __tablename__ = "service_areas"  # Table name
    id = Column(Integer, primary_key=True, autoincrement=True)  # Service area ID
    name = Column(String)  # Service area name
    price = Column(Float)  # Service area price
    geojson = Column(JSON, nullable=True)  # GeoJSON information
    provider_id = Column(Integer, ForeignKey("providers.id"))  # Foreign key to Provider

    # Relationship with Provider
    provider = relationship("Provider", back_populates="service_areas")
