from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from main_app.database import SessionLocal
from main_app.models import ServiceArea, Provider
from main_app.schemas import ServiceAreaCreate, ServiceAreaUpdate
from main_app.utils.geolocation import get_service_areas_by_location
from typing import List
from sqlalchemy import exc

router = APIRouter()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/service-areas/")
async def create_service_area(
    service_area: ServiceAreaCreate, db: Session = Depends(get_db)
):
    """
    Create a new main_app area in the database.
    """
    try:
        db_service_area = ServiceArea(**service_area.dict())
        db.add(db_service_area)
        db.commit()
        db.refresh(db_service_area)
        return db_service_area
    except exc.SQLAlchemyError as e:
        db.rollback()  # Rollback the session to avoid any state issues
        raise HTTPException(status_code=500, detail="Database error occurred")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/service-areas/{area_id}")
async def read_service_area(area_id: str, db: Session = Depends(get_db)):
    """
    Get a main_app area by ID.
    """
    try:
        service_area = db.query(ServiceArea).filter(ServiceArea.id == area_id).first()
        if service_area is None:
            raise HTTPException(status_code=404, detail="Service area not found")
        return service_area
    except HTTPException:
        raise
    except exc.IntegrityError as ie:
        raise HTTPException(status_code=400, detail="Integrity error occurred")
    except exc.SQLAlchemyError as se:
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/service-areas/")
async def list_service_areas(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    """
    List all main_app areas with pagination.
    """
    try:
        service_areas = db.query(ServiceArea).offset(skip).limit(limit).all()
        return service_areas
    except exc.SQLAlchemyError as se:
        # General SQLAlchemy error
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        # Unexpected errors
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.put("/service-areas/{service_area_id}")
def update_service_area(
    service_area_id: int,
    updated_service_area: ServiceAreaUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a servicearea by ID.
    """
    try:
        # Fetch the ServiceArea from the database using the provided service_area_id
        service_area = (
            db.query(ServiceArea).filter(ServiceArea.id == service_area_id).first()
        )

        # If the ServiceArea is not found, raise a 404 error
        if not service_area:
            raise HTTPException(status_code=404, detail="Service area not found")

        # If a new provider_id is provided, check if it is valid
        if updated_service_area.provider_id is not None:
            provider = (
                db.query(Provider)
                .filter(Provider.id == updated_service_area.provider_id)
                .first()
            )
            # If the Provider is not found, raise a 400 error
            if not provider:
                raise HTTPException(status_code=404, detail="Provider not found")

        # Update the fields of the ServiceArea with the values from the request
        for key, value in updated_service_area.model_dump(exclude_unset=True).items():
            setattr(service_area, key, value)

        # Commit the changes to the database
        db.commit()
        # Refresh the service_area instance to get the latest state from the database
        db.refresh(service_area)

        # Return the updated ServiceArea
        return service_area

    except HTTPException as http_exc:
        raise http_exc
    except exc.SQLAlchemyError as se:
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.delete("/service-areas/{area_id}")
def delete_provider(area_id: int, db: Session = Depends(get_db)):
    """
    Delete a provider by ID.
    """
    try:
        provider = db.query(ServiceArea).filter(ServiceArea.id == area_id).first()
        if not provider:
            raise HTTPException(status_code=404, detail="Service Area not found")

        db.delete(provider)
        db.commit()
        return {"success": True, "message": "Service Area deleted"}
    except HTTPException as http_exc:
        raise http_exc
    except exc.SQLAlchemyError as se:
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/service-areas/locations/")
async def get_service_areas_by_lat_lng(
    lat: float, lng: float, db: Session = Depends(get_db)
):
    """
    Get main_app areas containing the specified latitude and longitude.
    """
    try:
        service_areas = db.query(ServiceArea).all()  # Fetch all main_app areas
        results = get_service_areas_by_location(lat, lng, service_areas)  # Use caching
        return results
    except HTTPException as http_exc:
        raise http_exc
    except exc.SQLAlchemyError as se:
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
