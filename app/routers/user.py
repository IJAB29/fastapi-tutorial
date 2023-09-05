from typing import List
from fastapi import APIRouter, Depends, Response, status, HTTPException
from ..database import get_db
from ..import schemas, models, utils
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserRequest, db: Session = Depends(get_db)):

    # hash password
    user.password = utils.hash_pw(user.password)

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user
