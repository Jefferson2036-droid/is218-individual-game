"""Account update: display name and password."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..deps import get_current_user, get_db
from ..models import User
from ..schemas import PasswordIn, ProfileIn
from ..security import hash_password, verify_password
from ..views import user_out

router = APIRouter(prefix="/api/me", tags=["accounts"])


@router.patch("")
def update_profile(data: ProfileIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user.display_name = data.display_name
    db.commit()
    return {"user": user_out(user)}


@router.post("/password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(data: PasswordIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not verify_password(data.current_password, user.password_hash):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Current password is wrong")
    user.password_hash = hash_password(data.new_password)
    db.commit()
