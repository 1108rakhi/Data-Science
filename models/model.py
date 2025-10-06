from sqlalchemy import Column, String, JSON, Integer
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

