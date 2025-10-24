from fastapi import FastAPI
from router_metadata.navigator import router, desc_router, glossary_description_router
from router_connection import connection_crud
app = FastAPI()
app.include_router(router, tags = ['Metadata'])
app.include_router(desc_router, tags=['Business Descriptions'])
app.include_router(glossary_description_router, tags=["Glossary Description"])
app.include_router(connection_crud.conn_router, tags= ['Connections'])