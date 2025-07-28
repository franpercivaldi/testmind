from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class UploadedFileResponse(BaseModel):
    id: UUID
    original_filename: str
    filepath: str
    uploaded_at: datetime
    uploaded_by: str | None = None

    model_config = ConfigDict(from_attributes=True)
