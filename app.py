from core.users.router import user_router
from core.post.router import post_router
from dependencies import init_db
from fastapi import FastAPI
import uvicorn


from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

inputs = {
    "title": "Blog Application",
    "description": "This is a blogging application API where users can create and manage posts.",
    "version": "1",
    "lifespan": lifespan,
}

app = FastAPI(**inputs)

app.include_router(user_router, prefix='/user')
app.include_router(post_router, prefix='/post')



if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8080, reload=True)
