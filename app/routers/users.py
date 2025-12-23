from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..schemas import UserCreate, UserUpdate, UserOut, ErrorResponse
from ..database.database import get_db
from ..services import users as user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.put("", response_model=UserOut, status_code=200, responses={
    400: {"model": ErrorResponse},
    403: {"model": ErrorResponse},
    500: {"model": ErrorResponse}
})
def add_user(data: UserCreate, db: Session = Depends(get_db)):
    """Add a new user"""
    try:
        # Check if user with email already exists
        existing_user = user_service.get_user_by_email(db, data.email)
        if existing_user:
            raise HTTPException(
                status_code=403, 
                detail="User with that email already exists"
            )
        
        # Create new user
        user = user_service.create_user(db, data)
        return user
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Bad request")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="server error")

@router.patch("/{user_id}", response_model=UserOut, status_code=200, responses={
    400: {"model": ErrorResponse},
    404: {"model": ErrorResponse},
    500: {"model": ErrorResponse}
})
def edit_user_by_id(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    """Edit a user's attributes"""
    try:
        # Find user
        user = user_service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User with that id does not exist"
            )
        
        # Update user
        updated_user = user_service.update_user(db, user, data)
        return updated_user
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Bad request")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="server error")

@router.delete("/{user_id}", status_code=200, responses={
    400: {"model": ErrorResponse},
    404: {"model": ErrorResponse},
    500: {"model": ErrorResponse}
})
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Delete a user"""
    try:
        # Find user
        user = user_service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User with that id does not exist"
            )
        
        # Delete user
        user_service.delete_user(db, user)
        return {}
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Bad request")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="server error")

@router.get("/{user_id}", response_model=UserOut, status_code=200, responses={
    400: {"model": ErrorResponse},
    404: {"model": ErrorResponse},
    500: {"model": ErrorResponse}
})
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Find a user with ID"""
    try:
        user = user_service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User with that id does not exist"
            )
        return user
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Bad request")
    except Exception as e:
        raise HTTPException(status_code=500, detail="server error")

@router.get("", response_model=List[UserOut], status_code=200, responses={
    400: {"model": ErrorResponse},
    500: {"model": ErrorResponse}
})
def get_all_users(db: Session = Depends(get_db)):
    """Get all users"""
    try:
        users = user_service.get_all_users(db)
        return users
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Bad request")
    except Exception as e:
        raise HTTPException(status_code=500, detail="server error")

