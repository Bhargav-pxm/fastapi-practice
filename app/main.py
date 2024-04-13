from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# * This FILE is used to define API CALLS and create FUNCTIONS


# models.Base.metadata.create_all(bind=engine)

# !this variable is used to initialize the FastAPI
app = FastAPI()


# * these line are used to call routes methods/functions in main.py

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#! initial base url


@app.get("/")
async def root():
    return {"message": "API testing using python API tutorial"}


origins = [
    "*"
    # Assuming your React app runs on this port
    # Add other origins as needed
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
