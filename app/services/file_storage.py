import os
from uuid import uuid4
from fastapi import UploadFile
from app.db.session import SessionLocal
from app.models.uploaded_file import UploadedFile
from app.schemas.upload import UploadedFileResponse

UPLOAD_DIR = "data/uploads"

def save_uploaded_file(file: UploadFile, uploaded_by: str | None = None) -> UploadedFileResponse:
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Nombre único
    file_ext = file.filename.split(".")[-1]
    unique_name = f"{uuid4()}.{file_ext}"
    full_path = os.path.join(UPLOAD_DIR, unique_name)

    # Guardar en disco
    with open(full_path, "wb") as f:
        f.write(file.file.read())

    # Guardar en base
    db = SessionLocal()
    db_file = UploadedFile(
        original_filename=file.filename,
        filepath=full_path,
        uploaded_by=uploaded_by
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    db.close()

    return UploadedFileResponse.from_orm(db_file)
