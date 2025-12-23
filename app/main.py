from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database.database import Base, engine
from .routers import users as users_router
from .routers import auth as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="User Management API", version="1.0.0", lifespan=lifespan)

@app.get("/health")
def health():
    return {"ok": True}

app.include_router(auth_router.router)
app.include_router(users_router.router)

