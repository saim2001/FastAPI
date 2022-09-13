from sqlalchemy import func
from sqlalchemy.sql import label

from ..schemas import PostCreate,ResPost,Post_W_Likes
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from ..oauth2 import get_current_user


router=APIRouter(prefix="/posts",tags=["Posts"])





@router.get("/",response_model=List[Post_W_Likes])
async def get_posts(db: Session = Depends(get_db),current_user: int = Depends(get_current_user),
                    search: Optional[str] = "" ,limit:int=10):
    # cursor.execute("""SELECT * FROM posts """)
    # posts=cursor.fetchall()

    results=db.query(models.POST,func.count(models.LIKE.like_post_id).label('likes')).join(models.LIKE,
            models.LIKE.like_post_id==models.POST.post_id,isouter=True).group_by(models.POST.post_id).filter(models.POST.post_title.contains(search )).limit(limit).all()
    return results

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=ResPost)
async def create_post(post: PostCreate,db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    # cursor.execute("""INSERT INTO posts (post_title,post_content,post_published)
    # VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # connection.commit()
    print(current_user.user_id)
    new_post=models.POST(owner_id=current_user.user_id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)


    return new_post

@router.get("/{id}",response_model=Post_W_Likes)
def get_post(id: int,response: Response,db: Session = Depends(get_db),current_user: int = Depends(get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE post_id = %s """, (str(id)))
    # searched_post=cursor.fetchone()
    # print(searched_post)
    searched_post=db.query(models.POST,func.count(models.LIKE.like_post_id).label('likes')).join(models.LIKE,
            models.LIKE.like_post_id==models.POST.post_id,isouter=True).group_by(models.POST.post_id).filter(models.POST.post_id==id).first()

    if searched_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"message":f"post with id {id} was not found"}
    return searched_post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int,db: Session = Depends(get_db),current_user: int = Depends(get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE post_id = %s RETURNING *""",str(id))
    # del_post=cursor.fetchone()
    # connection.commit()
    del_post=db.query(models.POST).filter(models.POST.post_id==id)

    if del_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    if del_post.first().owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Action not authorized")
    del_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=ResPost)
def update(id: int,post: PostCreate,db: Session = Depends(get_db),current_user: int = Depends(get_current_user)):
    # cursor.execute("""UPDATE posts SET post_title=%s, post_content=%s, post_published=%s
    # WHERE post_id=%s
    # RETURNING *""",(post.title,post.content,post.published,str(id)))
    # upd_post=cursor.fetchone()
    # connection.commit()
    query=db.query(models.POST).filter(models.POST.post_id==id)
    upd_post=query.first()

    if  upd_post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    if upd_post.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Action not authorized")
    query.update(post.dict(),synchronize_session=False)
    db.commit()
    return query.first()