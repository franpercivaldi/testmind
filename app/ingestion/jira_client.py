from jira import JIRA
from app.core.config import settings
from app.schemas.jira import JiraIssue
from typing import List

class JiraClient:
    def __init__(self):
        options = {"server": settings.jira_api_base}
        self.client = JIRA(
            options=options,
            basic_auth=(settings.jira_email, settings.jira_token)
        )

    # Método para probar la conexión a Jira
    def test_connection(self) -> bool:
        try:
            user = self.client.current_user()
            print(f"[JiraClient] Conectado como: {user}")
            return True
        except Exception as e:
            print(f"[JiraClient] Error de conexión: {e}")
            return False

    # Método para obtener issues de Jira
    def get_issues(self, project_key: str, issue_type: str = None, status: str = None, max_results: int = 10) -> List[JiraIssue]:
        # Construir JQL
        jql = f'project = "{project_key}"'
        if issue_type:
            jql += f' AND issuetype = "{issue_type}"'
        if status:
            jql += f' AND status = "{status}"'

        print(f"[JiraClient] Ejecutando JQL: {jql}")

        try:
            issues = self.client.search_issues(jql, maxResults=max_results)

            return [
                JiraIssue(
                    key=issue.key,
                    summary=issue.fields.summary,
                    description=issue.fields.description,
                    issue_type=issue.fields.issuetype.name if issue.fields.issuetype else None,
                    status=issue.fields.status.name if issue.fields.status else None,
                    labels=issue.fields.labels,
                    assignee=issue.fields.assignee.displayName if issue.fields.assignee else None,
                    reporter=issue.fields.reporter.displayName if issue.fields.reporter else None,
                    created=issue.fields.created,
                    updated=issue.fields.updated
                )
                for issue in issues
            ]
        except Exception as e:
            print(f"[JiraClient] Error buscando issues: {e}")
            return []
