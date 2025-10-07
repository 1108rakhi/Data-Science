from fastapi import FastAPI
from router_metadata.navigator import router, desc_router
app = FastAPI()
app.include_router(router, tags = ['Metadata'])
app.include_router(desc_router, tags=['Business Descriptions'])