"""Arena Climb API. Run with: uvicorn app.main:app --reload"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from . import models  # noqa: F401  (registers the tables)
from .db import Base, engine
from .routers import account, armory, auth, dashboard, matches


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Arena Climb API", version="0.1.0", lifespan=lifespan)
app.include_router(auth.router)
app.include_router(matches.router)
app.include_router(dashboard.router)
app.include_router(account.router)
app.include_router(armory.router)


@app.get("/api/health", tags=["status"])
def health():
    return {"status": "ok"}


# The game's pages. Mounted last so every /api route above wins.
_HERE = Path(__file__).resolve().parent
_RENDERS = _HERE.parent / "art" / "renders"
if _RENDERS.is_dir():
    app.mount("/art/renders", StaticFiles(directory=_RENDERS), name="renders")
app.mount("/", StaticFiles(directory=_HERE / "static", html=True), name="site")
