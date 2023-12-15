from typing import Annotated
from fastapi import APIRouter , status , Depends , HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import UserLogin , UserOut
from app.utils import get_password_hash , verify_passwords
from ..models import *
from ..oauth2 import * 
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(
    prefix="/auth", 
    tags=["Authentication"]
)


@router.post("/login" , status_code=status.HTTP_200_OK , response_model=Token)
async def login(user_credentials : Annotated[OAuth2PasswordRequestForm, Depends()] , db : Session = Depends(get_db)):

    user = db.query(User).filter(User.email == user_credentials.username).first()
    
    if not user :
        print(f"couldn't find a user with this email : {user_credentials.username}")
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN ,
                             detail=f"couldn't find a user with this email : {user_credentials.username}")
    # print(user.email)

    are_passwords_match = verify_passwords(user_credentials.password ,user.password) 

    if not are_passwords_match : 
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="invalid password")
    
    access_token = create_access_token(data={"id":user.id})

    return  Token(access_token=access_token , token_type="bearer")
