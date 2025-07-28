from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from app.services.file_storage import save_uploaded_file
from app.schemas.upload import UploadedFileResponse
from app.schemas.test_case import TestCaseSchema
from app.ingestion.excel_reader import parse_excel_to_cases
from app.db.session import SessionLocal
from app.models.uploaded_file import UploadedFile

router = APIRouter(prefix="/excel", tags=["Excel Upload"])

@router.post("/upload", response_model=UploadedFileResponse)
def upload_excel(
    file: UploadFile = File(..., description="Archivo Excel (.xlsx)"),
    uploaded_by: str = Form(None)
):
    return save_uploaded_file(file, uploaded_by)

@router.get("/cases", response_model=list[TestCaseSchema])
def get_cases_from_excel(file_id: UUID = Query(..., description="ID del archivo subido")):
    db: Session = SessionLocal()

    db_file = db.query(UploadedFile).filter(UploadedFile.id == file_id).first()
    db.close()

    if not db_file:
        raise HTTPException(status_code=404, detail=f"Archivo con ID {file_id} no encontrado.")

    try:
        casos = parse_excel_to_cases(db_file.filepath)
        return casos
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar Excel: {str(e)}")