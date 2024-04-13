from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database as db, schemas, models, utils, oath2


# * This FILE is to authenticate User

router = APIRouter(tags=["Authentication"])


#! In this function we will take User entered password and hashed password from DB and check both are same or not if same we will allow else raise exception
@router.post("/login", response_model=schemas.Token)
def auth(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(db.get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credentials",
        )
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credentials",
        )
    access_token = oath2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
