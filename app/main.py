import time
from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas, utils
from .database import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# Unecessary since alembic will handle creation of tables
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# ONLY FOR RAW SQL QUERIES
# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", database="fastapi",
#                                 user="postgres", password="admin", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print(f"Database connection failed: {error}")
#         time.sleep(2)


# my_posts = [
#     {
#         "title": "HATDOG?",
#         "content": "AAAAAAAAAAAAAAAAAAAAAAAA",
#         "published": True,
#         "rating": 6,
#         "id": 4453664
#     }

# ]


# def find_post(id):
#     for i, post in enumerate(my_posts):
#         if post["id"] == id:
#             return i, post


@app.get("/")
def root():
    return {"message": "Hello World!AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"}
