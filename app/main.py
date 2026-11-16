"""Arena Climb API. Run with: uvicorn app.main:app --reload"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

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
