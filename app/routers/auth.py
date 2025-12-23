from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..schemas import UserLogin, UserOut, ErrorResponse
from ..database.database import get_db
from ..services import users as user_service
from ..utils.security import verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=UserOut, status_code=200, responses={
    400: {"model": ErrorResponse},
    401: {"model": ErrorResponse},
    500: {"model": ErrorResponse}
})
def login(data: UserLogin, db: Session = Depends(get_db)):
    """Login with email and password"""
    try:
        # Find user by email
        user = user_service.get_user_by_email(db, data.email)
        if not user:
            raise HTTPException(
                status_code=401, 
                detail="Invalid email or password"
            )
        
        # Verify password
        if not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=401, 
                detail="Invalid email or password"
            )
        
        return user
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Bad request")
    except Exception as e:
        raise HTTPException(status_code=500, detail="server error")

