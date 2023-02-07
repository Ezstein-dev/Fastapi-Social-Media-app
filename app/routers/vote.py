from fastapi import Depends, HTTPException, Response, status, APIRouter
from .. import schemas, oauth2, database, models
from ..database import SessionLocal, get_db

router=APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/post", status_code=status.HTTP_201_CREATED)
def post_vote(vote: schemas.PostVote, db: SessionLocal = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {vote.post_id} does not exist")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    voted_post = vote_query.first()
    if(vote.dir == 1):
        if voted_post:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already vote on the post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message": "Successfully added vote"}
    else:
        if not voted_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"Message": "Succcessfully deleted"} 
    

@router.post("/comment", status_code=status.HTTP_201_CREATED)
def comment_vote(vote: schemas.CommentVote, db: SessionLocal = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.id == vote.comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"comment with id: {vote.comment_id} does not exist")
    vote_query = db.query(models.Vote).filter(
        models.Vote.comment_id == vote.comment_id, models.Vote.user_id == current_user.id)
    voted_comment = vote_query.first()
    if (vote.dir == 1):
        if voted_comment:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already vote on the post {vote.post_id}")
        new_vote = models.Vote(comment_id=vote.comment_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message": "Successfully added vote"}
    else:
        if not voted_comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"Message": "Succcessfully deleted"}
        
