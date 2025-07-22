from fastapi import APIRouter, UploadFile, File, Form
from app.services.file_storage import save_uploaded_file
from app.schemas.upload import UploadedFileResponse

router = APIRouter(prefix="/excel", tags=["Excel Upload"])

@router.post("/upload", response_model=UploadedFileResponse)
def upload_excel(
    file: UploadFile = File(..., description="Archivo Excel (.xlsx)"),
    uploaded_by: str = Form(None)
):
    """
    Sube un archivo Excel y lo guarda en disco + base de datos.
    """
    return save_uploaded_file(file, uploaded_by)
