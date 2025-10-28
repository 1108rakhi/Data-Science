from pydantic import BaseModel
from typing import Optional, List

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

# connections response model
class ConnectionSchema(BaseModel):

    connection_id : int
    connection_type : str
    connection_name : str
    # domain_name : str
    username : str
    pswd : str
    host : str
    port : str
    schema : str
    created_by : Optional[str] = None
    modified_by : Optional[str] = None
    class Config:
        orm_mode = True

class UpdateConnection(BaseModel):
    username : Optional[str] = None
    pswd : Optional[str] = None
    host : Optional[str] = None
    port : Optional[str] = None
    schema : Optional[str] = None


class CreateConnection(BaseModel):
    
    connection_type : str
    connection_name : str
    # domain_name : str
    username : str
    pswd : str
    host : str
    port : str
    schema : str

# jobs response models
class JobSchema(BaseModel):
    job_id : int
    connection_id : int
    job_name : str
    
    created_by : str
    modified_by : Optional[str] = None
    class config:
        orm_mode = True

class UpdateJob(BaseModel):
    connection_id : int
    job_name : str
    
class CreateJob(BaseModel):
    connection_id : int
    job_name : str
   
class Filter(BaseModel):
    job_id : int
    connection_id : int
    job_name : str
    include_schema : str
    include_table : str
    created_by : str
    modified_by : Optional[str] = None
    class config:
        orm_mode = True

class JobDetails(BaseModel):
    job_id: int
    connection_id: int
    job_name: str
    created_by: str

class Filter(BaseModel):
    message: str
    job_details: JobDetails
    filtered_schemas: Optional[List[str]] = None
    filtered_tables: Optional[List[str]] = None

    class Config:
        orm_mode = True
  
