from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.routers import users, posts


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Shutdown (optional cleanup)
    await engine.dispose()


app = FastAPI(
    title="FastAPI Assignment",
    lifespan=lifespan
)

app.include_router(users.router)
app.include_router(posts.router)
