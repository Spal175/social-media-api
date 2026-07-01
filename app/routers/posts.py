from sqlalchemy.sql import func
from typing import Optional

from .. import models,schemas,utils,oauth2
from fastapi import FastAPI,Response,HTTPException,Depends,APIRouter,status
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter(prefix="/posts")






@router.get("/",response_model=list[schemas.postout])

def get_posts(db:Session=Depends(get_db),user_id:int =Depends(oauth2.getcurusr),
              limit:int=10,skip:int=0,search:Optional[str]=""):
    # cursor.execute("""SELECT * FROM posts""")
    # c=cursor.fetchall()
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = (
    db.query(
        models.Post,
        func.count(models.Votes.post_id).label("votes")
    )
    .join(
        models.Votes,
        models.Votes.post_id == models.Post.id,
        isouter=True
    )
    .group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    .all()
)
    return posts

@router.post("/createposts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(newpost:schemas.PoseCreate,db:Session=Depends(get_db),
                 currentuser:int =Depends(oauth2.getcurusr)):
    # cursor.execute("""INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) returning *""",(newpost.title,newpost.content,newpost.published))
    # p=cursor.fetchone()
    # mydb.commit()
    new_post=models.Post(owner_id=currentuser.id,**newpost.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.get("/{id}",response_model=schemas.postout)
def get_posts(id:int,db:Session=Depends(get_db),user_id:int =Depends(oauth2.getcurusr)):
    # print(id)
    # cursor.execute("""SELECT * FROM POSTS WHERE ID = %s""",(str(id)))
    # post=cursor.fetchone()
    # print(post)
    
    post= db.query(
        models.Post,
        func.count(models.Votes.post_id).label("votes")
     ).join(
        models.Votes,
        models.Votes.post_id == models.Post.id,
        isouter=True
    ).group_by(models.Post.id).filter(models.Post.id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id}: was not found")
    return post 


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int,db:Session=Depends(get_db),user_id:int =Depends(oauth2.getcurusr)):
    # cursor.execute("""delete from posts where id = %s returning *""",(str(id),))
    # index=cursor.fetchone()
    # mydb.commit()
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id}: was not found")
    
    if post.owner_id!=user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"NOT AUTHORISED TO PERFORM REQUESTED ACTION")
    db.delete(post)
    db.commit()  
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}")
def update_posts(id:int,post:schemas.PoseCreate,db:Session=Depends(get_db),
                 user_id:int =Depends(oauth2.getcurusr)):
    # cursor.execute("""update posts set title=%s, content=%s,published=%s where id = %s returning *""",(post.title,post.content,post.published,str(id),))
    # index=cursor.fetchone()
    # mydb.commit()
    postqry=db.query(models.Post).filter(models.Post.id==id)
    upost=postqry.first()
    if upost is None:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    # cursor.execute("""select * from posts""")
    # psts=cursor.fetchall()
    if post.owner_id!=oauth2.getcurusr.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"NOT AUTHORISED TO PERFORM REQUESTED ACTION")
    

    postqry.update(post.dict(),synchronize_session=False)
    db.refresh(upost)
    db.commit()
    
    return postqry.first()