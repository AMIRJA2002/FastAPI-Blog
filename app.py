from core.users.router import user_router
from core.post.router import post_router
from fastapi import FastAPI
import uvicorn

app = FastAPI()

app.include_router(user_router, prefix='/user')
app.include_router(post_router, prefix='/post')

if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8080, reload=True)
