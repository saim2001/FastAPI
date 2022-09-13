from jose import JWTError,jwt
from datetime import datetime,timedelta
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

from . import schemas,models,database


oauth2_schema=OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY=settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,cred_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str=payload.get("user id")
        if id is None:
            raise cred_exception
        token_data=schemas.Token_Data(user_id=id)
    except JWTError:
        raise cred_exception
    return token_data
def get_current_user(token:str=Depends(oauth2_schema),db: Session =Depends(database.get_db)):
    cerd_exeption=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="could not validate credentials",
                                    headers={"WWW-Authenticate":"Bearer"})

    token=verify_access_token(token,cerd_exeption)
    user=db.query(models.USER).filter(models.USER.user_id==token.user_id).first()
    return user

