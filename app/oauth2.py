import datetime

from . import schemas,database,models
from jose import JWTError,jwt
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings
oauth2_schme=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=int(settings.access_token_expire_minutes)

def crtacstkn(data:dict):
    to_encode=data.copy()
    expire=datetime.datetime.now() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
   
    return encoded_jwt

def vrfacstkn(token:str,credentials_exceptions):

    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exceptions
        token_data=schemas.tokendata(id=str(id))

    except JWTError:
        raise credentials_exceptions
    
    return token_data
    

def getcurusr(tkn: str=Depends(oauth2_schme),db:Session=Depends(database.get_db)):
    credentials_exceptions=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",
                                         headers={"WWW-Authenticate":"Bearer"})
    token=vrfacstkn(tkn,credentials_exceptions)
    user=db.query(models.users).filter(models.users.id==token.id).first()
    return user
