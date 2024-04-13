from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db


# TODO: this variable we use so that we can call this in main.py,using prefix we can skip using /users in each function

router = APIRouter(prefix="/users", tags=["Users"])


# ! this function/API is to create user


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):

    # TODO : hash user password by getting password using user.password
    hashed_pass = utils.hashing(user.password)
    user.password = hashed_pass
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ! this function/API is to GET One user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id : {id} does not exist",
        )
    return user
