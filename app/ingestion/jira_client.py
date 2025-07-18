from jira import JIRA
from app.core.config import settings

class JiraClient:
    def __init__(self):
        options = {"server": settings.jira_api_base}
        self.client = JIRA(
            options=options,
            basic_auth=(settings.jira_email, settings.jira_token)
        )

    def test_connection(self) -> bool:
        try:
            user = self.client.current_user()
            print(f"[JiraClient] Conectado como: {user}")
            return True
        except Exception as e:
            print(f"[JiraClient] Error de conexión: {e}")
            return False
