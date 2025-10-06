from fastapi import FastAPI
from routers.navigator import router
app = FastAPI()
app.include_router(router, tags = ['Metadata'])