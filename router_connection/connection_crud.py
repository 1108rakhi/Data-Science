from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from databases import database
from models import model
from schemas import schema
from jose import jwt, JWTError
from typing import Optional

conn_router = APIRouter()

secret_key = 'mysecret'
Algorithm = 'HS256'

def decode_token(token: str):
    try:
        decoded = jwt.decode(token, secret_key, algorithms=[Algorithm])
        return decoded
    except JWTError:
        raise HTTPException(status_code=401, detail = 'Invalid token')
    

def check_name(authorization : str):
    if not authorization:
        raise HTTPException(status_code=401, detail='Invalid authorization')
    
    role_check = decode_token(authorization)
    return role_check.get('sub')

# creating connection
@conn_router.post("/connections", response_model=schema.ConnectionSchema)
def create_connection(request: schema.CreateConnection, db: Session = Depends(database.get_db),current_user:str = Depends(check_name)):
    new_conn = model.Connection(
        connection_type=request.connection_type,
        connection_name=request.connection_name,
        # domain_name=request.domain_name,
        username=request.username,
        pswd=request.pswd,
        host=request.host,
        port=request.port,
        db_schema=request.db_schema,
        created_by=current_user
    )
    db.add(new_conn)
    db.commit()
    db.refresh(new_conn)
    return new_conn


# read all connections
@conn_router.get("/connections", response_model=list[schema.ConnectionSchema])
def get_connections(db: Session = Depends(database.get_db)):
    connections = db.query(model.Connection).all()
    if not connections:
        raise HTTPException(status_code=404, detail="No connections found")
    return connections


# get connection by id
@conn_router.get("/connections/{connection_id}", response_model=schema.ConnectionSchema)
def get_connection_by_id(connection_id: int, db: Session = Depends(database.get_db)):
    connection = db.query(model.Connection).filter(model.Connection.connection_id == connection_id).first()
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")
    return connection


# update connection
@conn_router.put("/connections/{connection_id}")
def update_connection(connection_id: int, request: schema.UpdateConnection, db: Session = Depends(database.get_db),current_user:str = Depends(check_name)):
    connection = db.query(model.Connection).filter(model.Connection.connection_id == connection_id).first()
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")
    connection.username = request.username
    connection.pswd = request.pswd
    connection.host = request.host
    connection.port = request.port
    connection.db_schema = request.db_schema
    connection.modified_by = current_user

    db.commit()
    db.refresh(connection)
    return connection


# delete connection
@conn_router.delete("/connections/{connection_id}")
def delete_connection(connection_id: int, db: Session = Depends(database.get_db)):
    connection = db.query(model.Connection).filter(model.Connection.connection_id == connection_id).first()
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")

    db.delete(connection)
    db.commit()
    return {"message": f"Connection with ID {connection_id} deleted successfully"}


job_router = APIRouter()

# creating job
@job_router.post("/jobs", response_model=schema.JobSchema)
def create_job(request : schema.CreateJob, db : Session = Depends(database.get_db),  current_user : str = Depends(check_name)):
    new_job = model.Jobs(
        connection_id = request.connection_id,
        job_name = request.job_name,
        created_by = current_user
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job


# get all jobs
@job_router.get("/jobs",response_model=list[schema.JobSchema])
def get_job(include:Optional[str] = None,
            include_type : Optional[str] = Query("contains", enum=["contains","startswith","endswith"]),
            db:Session = Depends(database.get_db)
            ):
    query = db.query(model.Jobs).join(model.Connection)
    if include:
        if include_type == "contains":
            query = query.filter(model.Connection.db_schema.like(f"%{include}%"))
        elif include_type == "startswith":
            query = query.filter(model.Connection.db_schema.like(f"{include}%"))
        elif include_type == "endswith":
            query = query.filter(model.Connection.db_schema.like(f"%{include}"))

 
    jobs = query.all()
    if not jobs:
        raise HTTPException(status_code=404, detail="No jobs found matching filters")
    
    return jobs

# get jobs by id
@job_router.get("/jobs/{job_id}")
def get_job_by_id(job_id:int, db: Session = Depends(database.get_db)):
    jobs = db.query(model.Jobs).filter(model.Jobs.job_id == job_id).first()
    if not jobs:
        raise HTTPException(status_code=400, detail="Job not found")
    return jobs

# update jobs
@job_router.put("/jobs/{job_id}")
def update_job(job_id : int, request:schema.UpdateJob, db:Session = Depends(database.get_db), current_user : str = Depends(check_name)):
    job = db.query(model.Jobs).filter(model.Jobs.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job.connection_id = request.connection_id
    job.job_name = request.job_name
    db.commit()
    db.refresh(job)
    return job


# delete jobs
@job_router.delete("/jobs/{job_id}")
def delete_job(job_id:int, db : Session = Depends(database.get_db)):
    jobs = db.query(model.Jobs).filter(model.Jobs.job_id == job_id).first()
    if not jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(jobs)
    db.commit()
    return {"message": f"Job with ID {job_id} deleted successfully"}




