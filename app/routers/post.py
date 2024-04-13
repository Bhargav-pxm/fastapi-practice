from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oath2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func

# TODO: this variable we use so that we can call this in main.py,using prefix we can skip using /users in each function

router = APIRouter(tags=["Posts"])


#! To get all posts
@router.get("/posts", response_model=List[schemas.PostVotes])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 50,
    skip: int = 0,
    filter: Optional[str] = "",
):
    # cursor.execute(""" select * from posts""")
    # posts = cursor.fetchall()
    # posts = (
    #     db.query(models.Post)
    #     .filter(models.Post.title.contains(filter))
    #     .limit(limit)
    #     .offset(skip)
    #     .all()
    # )
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(filter))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return posts


#! creating a new post
@router.post(
    "/post", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_post(
    post: schemas.CreatePost,
    db: Session = Depends(get_db),
    current_user: int = Depends(oath2.get_current_user),
):
    # cursor.execute(
    #     """insert into posts (title,content, published) values(%s,%s,%s) returning *""",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.email)
    new_post = models.Post(user_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#! To Get single post
@router.get("/post/{id}", response_model=schemas.PostVotes)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oath2.get_current_user),
):
    # cursor.execute("""select * from posts where id = %s""", (str(id)))
    # post = cursor.fetchone()

    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id : {id} not found!",
        )
    return post


#! To Delete single post
@router.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oath2.get_current_user),
):
    # cursor.execute("""delete from posts where id = %s returning *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id : {id} does not exist",
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Please make sure you have correct access rights to do the current action",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#! To Update single post
@router.put("/post/{id}", response_model=schemas.PostResponse)
def update_post(
    id: int,
    updated_post: schemas.UpdatePost,
    db: Session = Depends(get_db),
    current_user: int = Depends(oath2.get_current_user),
):
    # cursor.execute(
    #     """update posts set title  =%s, content=%s, published =%s where id = %s returning *""",
    #     (post.title, post.content, post.published, str(id)),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id : {id} does not exist",
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Please make sure you have correct access rights to do the current action",
        )
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
