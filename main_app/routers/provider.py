from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from main_app.database import SessionLocal
from main_app.models import Provider
from main_app.schemas import ProviderCreate, ProviderUpdate
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


@router.post("/providers/")
async def create_provider(provider: ProviderCreate, db: Session = Depends(get_db)):
    """
    Create a new provider in the database.
    """
    try:
        db_provider = Provider(**provider.model_dump())
        db.add(db_provider)
        db.commit()
        db.refresh(db_provider)
        return db_provider

    except exc.SQLAlchemyError as e:
        db.rollback()  # Rollback the session to avoid any state issues
        # Extract the error message
        error_message = str(e.orig)  # Get the original error message

        # Here you can check if it's a unique constraint violation
        if "unique constraint" in error_message.lower():
            raise HTTPException(status_code=400, detail="Email already registered.")

        raise HTTPException(status_code=500, detail="Database error occurred")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/providers/{provider_id}")
async def read_provider(provider_id: str, db: Session = Depends(get_db)):
    """
    Get a provider by ID.
    """
    try:
        provider = db.query(Provider).filter(Provider.id == provider_id).first()
        if provider is None:
            raise HTTPException(status_code=404, detail="Provider not found")
        return provider
    except HTTPException:
        raise
    except exc.IntegrityError as e:
        raise HTTPException(status_code=400, detail="Integrity error occurred")
    except exc.SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        print(e)
        a = e
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/providers/")
async def list_providers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    List all providers with pagination.
    """
    try:
        providers = db.query(Provider).offset(skip).limit(limit).all()
        return providers
    except exc.SQLAlchemyError as se:
        # General SQLAlchemy error
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        # Unexpected errors
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.put("/providers/{provider_id}")
def update_provider(
    provider_id: int, updated_provider: ProviderUpdate, db: Session = Depends(get_db)
):
    """
    Update a provider by ID.
    """
    try:
        provider = db.query(Provider).filter(Provider.id == provider_id).first()
        if not provider:
            raise HTTPException(status_code=404, detail="Provider not found")

        for key, value in updated_provider.model_dump(exclude_unset=True).items():
            setattr(provider, key, value)

        db.commit()
        db.refresh(provider)
        return provider
    except HTTPException as http_exc:
        # Raise the HTTPException if a specific HTTP error is detected
        raise http_exc
    except exc.SQLAlchemyError as e:
        db.rollback()  # Rollback the session to avoid any state issues
        # Extract the error message
        error_message = str(e.orig)  # Get the original error message

        # Here you can check if it's a unique constraint violation
        if "unique constraint" in error_message.lower():
            raise HTTPException(status_code=400, detail="Email already registered.")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        # Catch all other unexpected errors
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.delete("/providers/{provider_id}")
def delete_provider(provider_id: int, db: Session = Depends(get_db)):
    """
    Delete a provider by ID.
    """
    try:
        provider = db.query(Provider).filter(Provider.id == provider_id).first()
        if not provider:
            raise HTTPException(status_code=404, detail="Provider not found")

        db.delete(provider)
        db.commit()
        return {"success": True, "message": "Provider deleted"}
    except HTTPException as http_exc:
        # Raise the HTTPException if a specific HTTP error is detected
        raise http_exc
    except exc.SQLAlchemyError as se:
        # Catch any SQLAlchemy-specific errors (e.g., database issues)
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        # Catch all other unexpected errors
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
