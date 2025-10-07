from fastapi import APIRouter, HTTPException, Depends
from schemas.schema import PayloadRequest, PayloadResponse, MetadataSchema
from databases.database import store_metadata
from sqlalchemy.orm import Session
from databases import database
from models import model
router = APIRouter()

@router.post("/table_metadata", response_model=PayloadResponse)
def table_metadata(request: PayloadRequest):
    metadata_list = store_metadata(request)
    
    # if not metadata_list:
    #     raise HTTPException(status_code=404,detail="Metadata not found")
    save_metadata = [MetadataSchema(**col) for col in metadata_list]
    return PayloadResponse(
        catalog=request.catalog,
        schema=None,
        table_name=request.table_name,
        metadata_json=save_metadata
    )

@router.get("/table_metadata", response_model=list[PayloadResponse])
def get_metadata(db:Session = Depends(database.get_db)):
    rows = db.query(model.MetadataStore).all()
    # save_metadata=[]
    # for row in rows:
    #     for col in row.metadata_json:
    #         save_metadata.append(MetadataSchema(**col))

    return rows
