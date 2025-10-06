from pydantic import BaseModel
from typing import Optional

class PayloadRequest(BaseModel):
    host : str
    username : str
    password : str
    dbtype : str
    catalog: str
    schema : str
    table_name : str

class MetadataSchema(BaseModel):
    col_name : str
    dtype : str

class PayloadResponse(BaseModel):
    catalog : str
    schema : Optional[str] = None
    table_name : str
    metadata_json : list[MetadataSchema]
    class Config:
        orm_mode = True