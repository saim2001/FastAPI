from ..schemas import User,ResUser,Like
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from ..oauth2 import get_current_user
from .. import models
from ..database import engine,get_db
from sqlalchemy.orm import Session

router=APIRouter(prefix="/like",tags=["Like"])

@router.post("/",status_code=status.HTTP_201_CREATED)
def like(like: Like, db: Session = Depends(get_db), current_user: int =Depends(get_current_user)):
    query=db.query(models.LIKE).filter(models.LIKE.like_post_id==like.like_post_id,
                                       models.LIKE.like_user_id==current_user.user_id)
    p_query=db.query(models.POST).filter(models.POST.post_id==like.like_post_id).first()
    if not p_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {like.like_post_id} does not exist")
    found_like=query.first()
    if like.like_dir==1:
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                detail=f"{current_user.user_id} has already like the post {like.like_post_id}")
        n_like=models.LIKE(like_post_id=like.like_post_id,like_user_id=current_user.user_id)
        db.add(n_like)
        db.commit()
        return {"message":"Liked!"}
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="like does not exist")
        query.delete(synchronize_session=False)
        db.commit()

        return {"message":"like removed"}


