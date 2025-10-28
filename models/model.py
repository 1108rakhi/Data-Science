from sqlalchemy import Column, String, JSON, Integer, ForeignKey
# from sqlalchemy.orm import sessionmaker, declarative_base
# Base = declarative_base()
from databases.base import Base
class MetadataStore(Base):
    __tablename__ = 'metadata_response'
    id = Column(Integer, primary_key=True, autoincrement=True, index = True)
    catalog = Column(String(50))
    schema = Column(String(50))
    table_name = Column(String(50))
    metadata_json = Column(JSON)

# model for connection table
class Connection(Base):
    __tablename__ = "connections"
    connection_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    connection_type = Column(String(20), nullable=False)
    connection_name = Column(String(50), nullable=False)
    # domain_name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    pswd = Column(String(50), nullable=False)
    host = Column(String(20), nullable=False)
    port = Column(String(10), nullable=False)
    schema = Column(String(50), nullable=False)
    created_by = Column(String(50))
    modified_by = Column(String(50),nullable=False, default='null')

# model for jobs table
class Jobs(Base):
    __tablename__ = "jobs"
    job_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    connection_id = Column(Integer, ForeignKey("connections.connection_id"))
    job_name = Column(String(50), nullable=False) 
    # includes = Column(String(50))   
    created_by = Column(String(50))
    modified_by = Column(String(50),nullable=False, default='null')


