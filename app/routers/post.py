from fastapi import Body, FastAPI, Response , status , HTTPException , Depends , APIRouter
from .. import models
from ..database import engine  , get_db
from sqlalchemy.orm import Session 
from ..schemas import *
from typing import List
from ..oauth2 import get_current_user
from sqlalchemy.exc import NoResultFound
from sqlalchemy import func
##################################################Main Configuration####################################################
models.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/posts" , tags=["Posts"])
##################################################Main Configuration####################################################

# @router.get("/get-all-posts" , response_model=List[Post]) 
@router.get("/get-all-posts" , response_model=List[PostOut]) 
async def get_posts(*,db:Session=Depends(get_db),
                     current_user : int = Depends(get_current_user) 
                     ,limit:int = 10 ,
                       skip:int=0,
                       search:Optional[str] = ''):
    # posts = cursor.execute("""SELECT * FROM posts""").fetchall()
    # posts = db.query(models.Post)\
    #     .filter(models.Post.content.contains(search))\
    #     .offset(skip)\
    #     .limit(limit=limit)
    
    posts_with_votes= db.query(models.Post ,func.count(models.Vote.post_id).label("votes")).\
    join(models.Vote , models.Post.id == models.Vote.post_id ,isouter=True).\
    group_by(models.Post.id).\
        filter(models.Post.content.contains(search))\
        .offset(skip)\
        .limit(limit=limit)

    
    return posts_with_votes

@router.post("/create-post/" , status_code=status.HTTP_201_CREATED,response_model=Post)
async def create_post (post:PostCreate , response:Response,db:Session=Depends(get_db) , current_user : UserOut = Depends(get_current_user)) :
    # created_post = cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""" ,
    #                params=(
    #                    post.title,
    #                    post.content,
    #                    post.published
    #                )
    #                ).fetchone()
    # conn.commit()

    print(current_user.email)
    created_post = models.Post(owner_id = current_user.id,**post.model_dump())
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return  created_post


# @router.get("/posts/latest")
# def get_latest_post ():
#     return {"post" : my_posts[-1]}

@router.get("/get-post-by-id/{id}",response_model=PostOut)
async def get_post_by_id (id:int , response:Response,db:Session=Depends(get_db), current_user : UserOut = Depends(get_current_user)) :
    # post = cursor.execute("""SELECT * FROM posts WHERE id = %s """ ,
    #                        params=(str(id),)).fetchone()
    try :
        post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).\
            join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).\
            group_by(models.Post.id)\
            .filter(models.Post.owner_id == current_user.id).one()
        
    except NoResultFound :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , 
                            detail=f"couldn't find post with id = {id} & user_id = {current_user.id}")
    except Exception as e :
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED 
                            ,detail= f"this error has accoured \nerror {e}")
                           
    return post
    


@router.delete("/delete-post-by-id/{id}" , status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_by_id(id:int,db:Session=Depends(get_db), current_user : UserOut = Depends(get_current_user)) : 
    # post_deleted = cursor.execute("""DELETE FROM posts WHERE id =%s RETURNING * """ , 
    #                               params=(str(id),)).fetchone()
    post_to_be_deleted = db.query(models.Post).filter(models.Post.id == id)\
    .filter(models.Post.owner_id  == current_user.id)

    if not post_to_be_deleted.first(): 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , 
                            detail=f"no post was found with id = {id}")
    post_to_be_deleted.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/update-post-by-id/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_post_id (id:int , post:PostUpdate , db:Session=Depends(get_db), current_user : UserOut = Depends(get_current_user)):
    # updated_post = cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *""" , 
    #                               params=(post.title,
    #                                       post.content,
    #                                       post.published,
    #                                       str(id)
    #                               )).fetchone()   
    updated_post_model = db.query(models.Post).filter(models.Post.id == id)\
    .filter(models.Post.owner_id == current_user.id)
    
    if not updated_post_model.first() :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , 
                    detail=f"no post was found with id = {id}")
    
    updated_post_model.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)