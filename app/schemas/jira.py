from pydantic import BaseModel
from typing import Optional, List

class JiraIssue(BaseModel):
    key: str
    summary: str
    description: Optional[str]
    issue_type: Optional[str]
    status: Optional[str]
    labels: Optional[List[str]]
    assignee: Optional[str]
    reporter: Optional[str]
    created: Optional[str]
    updated: Optional[str]
