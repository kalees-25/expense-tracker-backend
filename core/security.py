import os

from dotenv import load_dotenv

from datetime import datetime , timedelta 

from passlib.context import CryptContext

from jose import JWTError , jwt

from fastapi import Depends , HTTPException , status

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session


from core.database.connection import get_db

from models.users import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES" , 30))

# -----------------------PASSWORD CONTEXT---------------------------------
pwd_context = CryptContext(
    
    schemes=["bcrypt"],    
    
    deprecated="auto"        #It handles future updates automatically, 
    
)


# ------------------OAUTH2 SCHEME FUNCTION-------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ------------------HASH PASSWORD FUNCTION-------------------------
def hash_password(password:str) -> str:

    return pwd_context.hash(password)


# ------------------VERIFY PASSWORD FUNCTION-------------------------
def verify_password(
    plain_password: str,
    
    hashed_password: str) -> bool:

    try:
        return pwd_context.verify(
        
        plain_password,
        
        hashed_password
        
    )

    except Exception:
        return False
    

    # ------------------CREATE ACCESS TOKEN FUNCTION-------------------------
def create_access_token (data:dict , 
                         expires_delta:timedelta | None = None):
    
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
        
    to_encode.update({"exp":expire})
    
    encoded_jwt = jwt.encode(to_encode ,
                             
                             SECRET_KEY , 
                             
                             algorithm=ALGORITHM)
    
    return encoded_jwt


# ------------------ AUTHORIZATION MIDDLEWARE / DEPENDENCY FUNCTION  -------------------------
def get_current_user(token:str = Depends(oauth2_scheme),
                    db:Session = Depends(get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    
    )
    
    try:
        payload  = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        
        
        if user_id is None:
            raise credentials_exception
        
    except JWTError:
        raise  credentials_exception
    
    user = db.query(User).filter(User.id==  int(user_id)).first()
    
    if  not user:
        raise credentials_exception
    
    return user

    
    