from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_passwords(plain_password , hashed_password) : 
    return pwd_context.verify(secret=plain_password , hash=hashed_password)