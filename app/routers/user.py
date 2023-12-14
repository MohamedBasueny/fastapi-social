from fastapi import  status , HTTPException , Depends , APIRouter
from .. import models
from ..database import engine  , get_db
from sqlalchemy.orm import Session
from ..schemas import *
from typing import List
from app.utils import * 
##################################################Main Configuration####################################################
models.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/users" ,tags=["Users"])
##################################################Main Configuration####################################################

@router.post("/create-user/" , status_code=status.HTTP_201_CREATED , response_model=UserOut)
async def create_user(user:UserCreate , db:Session=Depends(get_db)):
    hashed_pw = get_password_hash(user.password)
    user.password = hashed_pw
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/get-user-by-id/{id}" , response_model=UserOut)
def get_user (id:int , db:Session=Depends(get_db)) :
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"user with id {id} doesn't exsist!")
    return user 
