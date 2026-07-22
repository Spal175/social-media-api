from fastapi import FastAPI,Response,HTTPException,Depends,APIRouter,status
from .. import models,schemas,database,oauth2
from sqlalchemy.orm import Session
router=APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session=Depends(database.get_db),
current_user : int =Depends(oauth2.getcurusr),):
    
    vteqry = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    foundvote = vteqry.first()

    post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {vote.post_id} not found")


    if(vote.dir==1):
        if foundvote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Votes(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()

        return {"message":"successfully added vote!"}
    else:
        if not foundvote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"vote not found")
        vteqry.delete(synchronize_session=False)
        db.commit()
        return {"message":'successfully deleted vote!'}
    

