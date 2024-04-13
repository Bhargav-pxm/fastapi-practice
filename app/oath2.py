from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import timedelta, datetime, timezone
from . import schemas as sc, database as dbs, models as m
from sqlalchemy.orm import Session
from .config import settings


# * This File is to create the Authentication using the JWT

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# SECRET KEY
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minute


# ! Creates a JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ! Verifies access token and returns ID
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)

        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = sc.TokenData(id=str(id))
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(dbs.get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-AUthenticate": "Bearer"},
    )
    token = verify_access_token(token, credential_exception)
    user = db.query(m.User).filter(m.User.id == token.id).first()
    return user
