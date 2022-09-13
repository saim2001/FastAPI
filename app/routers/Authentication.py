from ..schemas import UserLogin
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models
from ..database import get_db
from sqlalchemy.orm import Session
from ..utils import verify
from ..oauth2 import create_access_token
from ..schemas import Token

router=APIRouter(tags=["Authentication"])
@router.post("/login",response_model=Token)
def login(user_cred:OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user=db.query(models.USER).filter(models.USER.user_email==user_cred.username).first()
    if not user:
        print("in")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Wrong Credentials")
    if not verify(user_cred.password,user.user_password):
        print(verify(user_cred.password, user.user_password))
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Wrong Credentials")
    access_token=create_access_token(data={"user id":user.user_id})
    return {"access_token":access_token,"token_type":"bearer"}

