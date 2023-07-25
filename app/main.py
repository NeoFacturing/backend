from typing import List, Optional
from fastapi import (
    FastAPI,
    HTTPException,
    Query,
    BackgroundTasks,
    UploadFile,
    File,
)
import os
from pydantic import BaseModel
from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Query,
    BackgroundTasks,
    Path,
    status,
    Response,
)
from fastapi.middleware.cors import CORSMiddleware
from azure.storage.blob import BlobServiceClient


import requests
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import os
from typing import List, Optional, Annotated

from fastapi import FastAPI, Depends, HTTPException, Query, status, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from pydantic import BaseModel

from app.core.chat import get_response
from app.core.whisper import speech_to_text
from app.database.config import settings
from app.database.database import Session
from app.database.get_user import get_user
from app.database.schemas import Token, User
from app.security import create_access_token
from app.utils.bearer import OAuth2PasswordBearerWithCookie
from app.utils.hashing import Hasher
from app.utils.upload_file import upload_file


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(username: str, password: str, db: Session):
    print(username)
    user = get_user(username=username, db=db)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user


@app.post("/token", response_model=Token)
def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(
        minutes=int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
    )
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login/token")


def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, os.environ["SECRET_KEY"], algorithms=[os.environ["ALGORITHM"]]
        )
        username: str = payload.get("sub")
        print("username/email extracted is ", username)
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username=username, db=db)
    if user is None:
        raise credentials_exception
    return user


@app.get("/")
async def read_root(name: Optional[str] = "we are neoFacturing"):
    return {"Hello": name}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user_from_token)):
    return current_user


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    files: list[str] = []


@app.post(
    "/chat",
    summary="Chat with the AI",
    description="Get a response from the AI model based on the input text",
)
async def read_chat(request: ChatRequest):
    try:
        response = get_response(request.messages[-1].content, ai="qa-chain")
        if response is not None:
            return {"response": response}
        else:
            raise HTTPException(
                status_code=500, detail="Failed to get a response from the AI model"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload-data")
async def trigger_data_upload(background_tasks: BackgroundTasks):
    background_tasks.add_task(upload_data)
    return {"message": "Data upload triggered"}


@app.post("/whisper")
async def create_upload_file(file: UploadFile):
    result = await upload_file(file)
    return {"result": result}


@app.post("/uploadfile")
async def create_upload_file(
    # current_user: User = Depends(get_current_user_from_token),
    file: UploadFile = File(...),
):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(
            os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        )
        blob_client = blob_service_client.get_blob_client("uploads", file.filename)

        data = await file.read()
        blob_client.upload_blob(data, overwrite=True)
        print(f"File {file.filename} uploaded successfully")
        return {"filename": file.filename}
    except Exception as e:
        print("Error uploading file")
        print(e)
        raise HTTPException(status_code=500, detail="Failed to upload file")
