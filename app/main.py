from typing import List, Optional, Annotated
from fastapi import (
    FastAPI,
    HTTPException,
    Query,
    BackgroundTasks,
    Path,
    UploadFile,
)
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.chat import get_response
from app.core.upload_data import upload_data
from app.core.whisper import speech_to_text


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        # allow_origins=["*"],
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()


@app.get("/")
async def read_root(name: Optional[str] = "World"):
    return {"Hello": name}


@app.get(
    "/chat",
    summary="Chat with the AI",
    description="Get a response from the AI model based on the input text",
)
async def read_chat(
    question: str = Query(
        ..., description="Input text to get a response from the AI model"
    ),
    history: Annotated[str, Path(title="Chat history")] = "",
):
    try:
        response = get_response(question, history)
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
    result = speech_to_text(file.file)
    return {"result": result}
