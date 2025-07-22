import os
from uuid import uuid4
from fastapi import UploadFile
from app.core.database import SessionLocal
from app.models.uploaded_file import UploadedFile
from app.schemas.upload import UploadedFileResponse

UPLOAD_DIR = "data/uploads"

def save_uploaded_file(file: UploadFile, uploaded_by: str | None = None) -> UploadedFileResponse:
    # Asegurarse de que el directorio exista
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Generar nombre único
    file_ext = file.filename.split(".")[-1]
    unique_name = f"{uuid4()}.{file_ext}"
    full_path = os.path.join(UPLOAD_DIR, unique_name)

    # Guardar físicamente
    with open(full_path, "wb") as f:
        f.write(file.file.read())

    # Registrar en DB
    db = SessionLocal()
    db_file = UploadedFile(
        filename=file.filename,
        filepath=full_path,
        uploaded_by=uploaded_by
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    db.close()

    return UploadedFileResponse(
        id=db_file.id,
        filename=db_file.filename,
        filepath=db_file.filepath,
        uploaded_at=db_file.uploaded_at,
        uploaded_by=db_file.uploaded_by
    )
