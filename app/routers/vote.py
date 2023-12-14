from fastapi import APIRouter , status , Depends , HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from ..models import *
from ..oauth2 import get_current_user
from ..schemas import VoteSchema , UserOut


router = APIRouter(
    prefix="/vote", 
    tags=["Vote"]
)

@router.post("/" , status_code=status.HTTP_201_CREATED) 
def vote(vote:VoteSchema ,
         db : Session = Depends(get_db) ,
         current_user : UserOut =  Depends(get_current_user )) : 
    

    post_is_found = db.query(Post).filter(Post.id == vote.post_id).first()
    if not post_is_found  : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id {vote.post_id} is not found")
    
    #check that the post isn't voted yet by the user 
    post_is_already_voted_up = db.query(Vote).filter(
    Vote.post_id == vote.post_id , 
    Vote.user_id == current_user.id)

    if vote.direction == 1 :

        if not post_is_already_voted_up.first()  : 
            vote_model = Vote(post_id = vote.post_id , user_id = current_user.id )
            db.add(vote_model)
            db.commit()
        else : 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail=f"post with id {vote.post_id} is already voted consider down-vote it!")
        
    elif vote.direction == 0 : 

        if post_is_already_voted_up.first()  :
            post_is_already_voted_up.delete(synchronize_session=False)
            db.commit()
        else : 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail=f"no post found with id = {vote.post_id}")

