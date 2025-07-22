from pydantic import BaseModel
from datetime import datetime

class UploadedFileResponse(BaseModel):
    id: int
    filename: str
    filepath: str
    uploaded_at: datetime
    uploaded_by: str | None = None
