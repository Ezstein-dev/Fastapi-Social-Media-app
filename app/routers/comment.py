from typing import List, Optional
from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy import engine_from_config, alias
# from sqlalchemy.dialects.postgresql.json 
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from ..database import SessionLocal, get_db, engine
from sqlalchemy.sql import func, alias


router = APIRouter(
    prefix="/comments",
    tags=['Comments']
)

@router.post("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.Comment)
def create_comments(id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db), 
                current_user: int =  Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {comment.post_id} does not exist")
    new_comment = models.Comment(user_id=current_user.id, post_id=id, **comment.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    print(new_comment)
    return new_comment 

def json_agg(table):
   result = (func.json_agg(table.id),func.json_agg(table.user_id), func.json_agg(table.comment),func.json_agg(table.created_at))
   return result


@router.get("/post/{id}", response_model=schemas.PostCommentOut)
def get_post_comments(id: int, db: Session = Depends(get_db), 
                current_user: int =  Depends(oauth2.get_current_user)):
    post =( 
           db.query(models.Post, 
           func.count(models.Vote.user_id)
           .label("likes"))
           .join(models.Vote, 
            models.Post.id == models.Vote.post_id, 
            isouter=True)
            .group_by(models.Post.id)
            .filter(models.Post.id == id).all()
    )
    comments =( 
               db.query(models.Comment, 
                        func.count(models.Vote.user_id)
                        .label("likes")).join(models.Vote, 
            models.Comment.id == models.Vote.comment_id, 
            isouter=True)
            .group_by(models.Comment.id)
            .filter(models.Comment.post_id == id).all()
               )
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail = f" The post with id:{id} was not found")
    print(post, comments)
    result = {"post": post, "comments": comments}
    return result


@router.get("/{id}", response_model=schemas.CommentOut)
def get_comment(id: int, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):

    comment = (
        db.query(models.Comment,
                 func.count(models.Vote.user_id)
                 .label("likes")).join(models.Vote,
                                       models.Comment.id == models.Vote.comment_id,
                                       isouter=True)
        .group_by(models.Comment.id)
        .filter(models.Comment.id == id).first()
    )
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" The post with id:{id} was not found")
    return comment

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(id: int, db: Session = Depends(get_db), 
                current_user: int =  Depends(oauth2.get_current_user)):
   comment_query = db.query(models.Comment).filter(models.Comment.id == id)
   comment = comment_query.first()
   if comment == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"comment with id:{id} does not exist")
   if comment.user_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                        detail="Not authorized to perform requested action")
   comment_query.delete(synchronize_session=False)
   db.commit()
   return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Comment)
def update_comment(id: int, updated_comment: schemas.CommentCreate, db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    comment_query = db.query(models.Comment).filter(models.Comment.id == id)
    comment = comment_query.first()
    if comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"comment with id:{id} does not exist")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                        detail="Not authorized to perform requested action")
    comment_query.update(updated_comment.dict(), synchronize_session=False)
    db.commit()
    return comment
