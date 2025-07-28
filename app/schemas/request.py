from uuid import UUID
from pydantic import BaseModel
from typing import List

class GenerateTestCasesRequest(BaseModel):
    file_id: UUID
    ticket_ids: List[str]
