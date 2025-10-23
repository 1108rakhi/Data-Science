from fastapi import APIRouter, HTTPException, Depends
from schemas.schema import PayloadRequest, PayloadResponse, MetadataSchema, DescriptionResponse, DescriptionSchema, GlossaryDescriptionResponse
from databases.database import store_metadata
from sqlalchemy.orm import Session
from databases import database
from models import model
from gemini_utils import generate_descriptions
import httpx

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
    # col_names = [col["col_name"] for col in metadata_list]
    try:
        openai_response = generate_descriptions(request.table_name, metadata_list)
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

glossary_description_router = APIRouter()

@glossary_description_router.get("/glossary_description/{glossary_id}", response_model=GlossaryDescriptionResponse)
def glossary_description(id:int):
    glossary_service_url = f"http://myapp:8000/glossary/{id}"
    response = httpx.get(glossary_service_url)
    output = response.json()
    if not output:
        raise HTTPException(status_code=500, detail="Unable to connect to glossary service")
    
    term = output.get("term")
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    metadata_list = [{"col_name": term, "desc": "STRING"}]
    ai_response = generate_descriptions(term, metadata_list)
    if isinstance(ai_response, list):
        description_text = ai_response[0]["business_description"]
    else:
        description_text = "No description generated."

    return GlossaryDescriptionResponse(
        term=term,
        description=description_text
    )