from fastapi import APIRouter, Query
from typing import Optional, List

from app.ingestion.jira_client import JiraClient
from app.schemas.jira import JiraIssue

router = APIRouter(prefix="/jira", tags=["jira"])

jira_client = JiraClient()

@router.get("/issues", response_model=List[JiraIssue])
def get_jira_issues(
    project_key: str = Query(..., description="Clave del proyecto Jira"),
    issue_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    max_results: int = Query(10, ge=1, le=100)
):
    return jira_client.get_issues(project_key, issue_type, status, max_results)
