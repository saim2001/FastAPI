from fastapi import FastAPI
from . import models
from .database import engine
from .routers import posts,users,Authentication,Like
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

models.BASE.metadata.create_all(bind=engine)

app=FastAPI()
origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(Authentication.router)
app.include_router(Like.router)

@app.get('/')
def root():
    return {"message":"hello"}







