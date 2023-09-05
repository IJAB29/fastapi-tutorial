from fastapi import APIRouter, Depends, Response, status, HTTPException
from ..database import get_db
from ..import schemas, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


# @router.post("/", status_code=status.HTTP_201_CREATED)
# def vote(vote_schema: schemas.VoteRequest, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

#     post = db.query(models.Post).filter(
#         models.Post.id == vote_schema.post_id).first()
#     if post is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="does not exist"
#         )

#     query = db.query(models.Vote).filter(
#         models.Vote.post_id == vote_schema.post_id,
#         models.Vote.user_id == current_user.id
#     )
#     vote = query.first()

#     if vote_schema.up_vote:
#         if vote:
#             raise HTTPException(
#                 status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post"
#             )

#         new_vote = models.Vote(
#             post_id=vote_schema.post_id, user_id=current_user.id)
#         db.add(new_vote)
#         db.commit()

#         return {"message": "succesfully added vote"}
#     else:
#         if vote is None:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND, detail="does not exist"
#             )

#         query.delete(synchronize_session=False)
#         db.commit()

#         return {"message": "succesfully deleted vote"}


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote_schema: schemas.VoteRequest, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    # Used .get() instead of .filter().first() to retrieve the post.
    post = db.query(models.Post).get(vote_schema.post_id)
    if post is None:
        raise HTTPException(
            # Simplified error message details for consistency and clarity.
            status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist"
        )

    existing_vote = db.query(models.Vote).filter(
        models.Vote.post_id == vote_schema.post_id,
        models.Vote.user_id == current_user.id
    ).first()

    if vote_schema.up_vote:
        if existing_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on this post"
            )

        new_vote = models.Vote(
            post_id=vote_schema.post_id, user_id=current_user.id)
        db.add(new_vote)
    else:
        if existing_vote is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist"
            )

        db.delete(existing_vote)

    # Combined the database commit operation after both vote addition and deletion.
    db.commit()

    return {"message": "Vote operation successful"}
