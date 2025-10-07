from fastapi import APIRouter, HTTPException, Depends
from schemas.schema import PayloadRequest, PayloadResponse, MetadataSchema, DescriptionResponse, DescriptionSchema
from databases.database import store_metadata
from sqlalchemy.orm import Session
from databases import database
from models import model
from gemini_utils import generate_descriptions

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
    return rows

# router for business descriptions
desc_router = APIRouter()

@desc_router.post('/generate_description', response_model=DescriptionResponse)
def generate_description(request : PayloadRequest):
    metadata_list = store_metadata(request)
    if not metadata_list:
        raise HTTPException(status_code=404, detail="No data found to generate description")
    col_names = [col["col_name"] for col in metadata_list]
    try:
        openai_response = generate_descriptions(request.table_name, col_names)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate descriptions: {str(e)}")

    # openai_response = generate_descriptions(request.table_name,col_names)
    # descriptions = [DescriptionSchema(**c) for c in openai_response]
    descriptions = []
    for c in openai_response:
        if isinstance(c, dict):
            descriptions.append(DescriptionSchema(**c))
        else:
            print("Skipping non-dict item:", c)

    return DescriptionResponse(
        table_name= request.table_name,
        description=descriptions
    )
