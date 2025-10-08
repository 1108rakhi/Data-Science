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
    col_name : str
    dtype : str
    business_name : str
    business_description : str

class DescriptionResponse(BaseModel):
    table_name : str
    description : list[DescriptionSchema]
    class Config:
        from_attributes = True

# response schema for communication with glossary service
class GlossaryDescriptionResponse(BaseModel):
    term: str
    description: str