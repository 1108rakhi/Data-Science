from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from models.model import MetadataStore
from databases.base import Base
import os
from dotenv import load_dotenv

load_dotenv()
# DB_URL = "mysql+mysqlconnector://root:rootroot@host.docker.internal:3306/project3"
if os.getenv("RUN_ENV") == "docker":
    DB_URL = os.getenv("DB_URL_DOCKER")
else:
    DB_URL = os.getenv("DB_URL_LOCAL")

    
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind = engine, autocommit = False, autoflush=False)

Base.metadata.create_all(bind = engine)

def store_metadata(request):
    dbtype = request.dbtype.lower()
    if dbtype == "mysql":
        db_url = f"mysql+mysqlconnector://{request.username}:{request.password}@{request.host}/{request.catalog}"
        
    elif dbtype == "oracle":
        db_url = f"oracle+cx_oracle://{request.username}:{request.password}@{request.host}/?service_name={request.catalog}"
        
    elif dbtype == 'mssql':
        db_url = f"mssql+pyodbc://{request.username}:{request.password}@{request.host}/{request.catalog}?driver=ODBC+Driver+17+for+SQL+Server"
       
    else:
        raise ValueError(f"Unsupported database type {request.dbtype}. Allowed database types : mysql, oracle, mssql")
    
    meta_engine = create_engine(db_url)
    inspector = inspect(meta_engine)
    columns = inspector.get_columns(request.table_name, schema=None)
    save_metadata = [{"col_name": col["name"], "dtype": str(col["type"])} for col in columns]
    session = SessionLocal()
    
    try:
        session.add(
            MetadataStore(
                catalog = request.catalog,
                schema = None,
                table_name = request.table_name,
                metadata_json = save_metadata
            )
        )
        session.commit()

    finally:
        session.close()

    return save_metadata


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()