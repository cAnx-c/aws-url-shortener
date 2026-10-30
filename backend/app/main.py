import uuid
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.config import settings
from app.models import ShortenRequest, ShortenResponse, UrlInfoResponse
from app.database import save_url, get_url_item

app = FastAPI(title="AWS URL Shortener API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/shorten", response_model=ShortenResponse, status_code=status.HTTP_201_CREATED)
def create_short_url(payload: ShortenRequest):
    short_code = str(uuid.uuid4())
    original_url_str = str(payload.original_url)
    created_at = datetime.now(timezone.utc).isoformat()

    try:
        save_url(short_code, original_url_str, created_at)
    except RuntimeError as err:
        raise HTTPException(status_code=500, detail=str(err))

    return ShortenResponse(
        short_code=short_code,
        original_url=original_url_str,
        short_url=f"{settings.BASE_URL.rstrip('/')}/{short_code}"
    )

@app.get("/urls/{short_code}", response_model=UrlInfoResponse)
def get_url_info(short_code: str):
    item = get_url_item(short_code)
    if not item:
        raise HTTPException(status_code=404, detail="Enlace no encontrado")

    return UrlInfoResponse(
        short_code=item["short_code"],
        original_url=item["original_url"],
        created_at=item["created_at"]
    )

@app.get("/{short_code}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
def redirect_to_original(short_code: str):
    item = get_url_item(short_code)
    if not item:
        raise HTTPException(status_code=404, detail="El enlace solicitado no existe")

    return RedirectResponse(url=item["original_url"], status_code=status.HTTP_307_TEMPORARY_REDIRECT)