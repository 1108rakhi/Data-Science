from pydantic import BaseModel
from typing import Optional

# metadata pydantic models
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

# business descriptions pydantic models
class DescriptionSchema(BaseModel):
    business_name : str
    business_description : str

class DescriptionResponse(BaseModel):
    table_name : str
    description : list[DescriptionSchema]