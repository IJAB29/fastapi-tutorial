from typing import List, Optional
from fastapi import APIRouter, Depends, Response, status, HTTPException
from ..database import get_db
from ..import schemas, models, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostVoteResponse])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)
    # ).limit(limit).offset(skip).all()

    votes = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).outerjoin(
        models.Vote,
        models.Post.id == models.Vote.post_id
    ).group_by(models.Post.id).limit(limit).offset(skip).all()

    # result = [
    #     {
    #         "post": post,
    #         "vote_count": vote_count
    #     }
    #     for post, vote_count in votes
    # ]

    return votes


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostRequest, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(
    #     title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.model_dump())
    new_post.user_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.PostVoteResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()

    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).outerjoin(
        models.Vote,
        models.Post.id == models.Vote.post_id
    ).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    query = db.query(models.Post).filter(models.Post.id == id)

    post = query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform action"
        )

    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostRequest, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    query = db.query(models.Post).filter(models.Post.id == id)

    post_query = query.first()

    if not post_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    if post_query.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform action"
        )

    query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query
