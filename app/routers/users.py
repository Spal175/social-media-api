from multiprocessing import synchronize

from .. import models,schemas,utils
from fastapi import FastAPI,Response,HTTPException,Depends,APIRouter,status
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter(prefix="/users")


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.userout)
def usercreate(user:schemas.usercreate, db:Session=Depends(get_db)):
    hashedpwd=utils.hasher(user.password)
    user.password=hashedpwd
    new_user=models.users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.userout)
def get_user(id:int,db:Session=Depends(get_db)):
    usr=db.query(models.users).filter(models.users.id==id).first()
    if not usr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id {id} does not exist")
    return usr