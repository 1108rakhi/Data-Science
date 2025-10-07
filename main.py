from fastapi import FastAPI
from router_metadata.navigator import router
app = FastAPI()
app.include_router(router, tags = ['Metadata'])