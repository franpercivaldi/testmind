# scripts/test_jira_connection.py

from app.ingestion.jira_client import JiraClient

if __name__ == "__main__":
    jc = JiraClient()
    jc.test_connection()
