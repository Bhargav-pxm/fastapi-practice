from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oath2, database
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional

router = APIRouter(prefix="/vote", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oath2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {vote.post_id} do not exist",
        )
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    )
    existing_vote = vote_query.first()
    if vote.dir == 1:
        if existing_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} has already voted on post {vote.post_id} !!!",
            )
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Voted successfully!"}
    else:
        if not existing_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="vote Do not exist"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote Removed!"}
