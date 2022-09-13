from ..schemas import User,ResUser
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models
from ..database import engine,get_db
from sqlalchemy.orm import Session
from ..utils import hash

router=APIRouter(prefix="/users",tags=["Users"])

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=ResUser)
async def create_user(user: User,db: Session = Depends(get_db)):
    user.user_password=hash(user.user_password)
    new_user = models.USER(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=ResUser)
async def create_user(id : int,db: Session = Depends(get_db)):
    searched_user = db.query(models.USER).filter(models.USER.user_id == id).first()

    if searched_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} was not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"message":f"post with id {id} was not found"}
    return searched_user
