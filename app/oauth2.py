from fastapi import Depends , status , HTTPException
from jose import JWTError, jwt
from datetime import datetime , timedelta 
from .schemas import Token,TokenData
from fastapi.security import OAuth2PasswordBearer
from .database import get_db  
from sqlalchemy.orm import Session
from .models import User
from .config import settings
# openssl rand -hex 32
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = settings.jwt_secret_key
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt_access_token_expire_minutes


def create_access_token (data:dict) : 
    to_encode = data.copy()
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : exp})
    encoded_jwt = jwt.encode(
        claims=to_encode , 
        algorithm= ALGORITHM , 
        key=SECRET_KEY
    )
    return encoded_jwt 


def verify_acces_token(token:str ,credentials_exception:str) : 
    try:
        payload = jwt.decode(
            token=token , 
            key=SECRET_KEY , 
            algorithms=ALGORITHM
        )

        user_id = payload.get("id")

        if user_id is None :
            raise credentials_exception
        
    
    except JWTError : 
        raise credentials_exception 
    
    return TokenData(id=str(user_id))

    

def get_current_user(token:str = Depends(oauth2_scheme) , db:Session = Depends(get_db)) : 
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED , 
        detail= "Invalid Authenticated Credentials" , 
        headers={"WWW-Authenticate": "Bearer"}
    )
    token : TokenData  =  verify_acces_token(token , credentials_exception)
    if token : 
        current_user = db.query(User).filter(User.id == token.id).one()
        return current_user 
























# test_verify_acc_token = verify_acces_token(create_access_token({"sub" : "mobasueny@gmail.com" , "id" : "1"}))
# print(test_verify_acc_token)


# jwt_test = create_access_token(data={"sub" : "mobasueny@gmail.com" , "id" : "1"})
# print(jwt_test)

