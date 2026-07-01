from fastapi import FastAPI,status,APIRouter,HTTPException,Depends,Response

from sqlalchemy.orm import Session

from app import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database,models,schemas,models,utils,oauth2

router=APIRouter(tags=['Authentication'])

@router.post('/login',response_model=schemas.token)
def login(user_credential:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    
    usr=db.query(models.users).filter(models.users.email==user_credential.username).first()

    if not usr:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid credentials")
    
    if not utils.verifier(user_credential.password,usr.password):
        raise HTTPException(status=status.HTTP_403_FORBIDDEN,detail="invalid credentials")
    
    access_token=oauth2.crtacstkn(data={"user_id":usr.id})

    return {"access_token":access_token,"token_type":"bearer"}
