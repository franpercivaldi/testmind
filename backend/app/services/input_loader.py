from typing import List, Dict
from app.db.session import SessionLocal
from app.models.uploaded_file import UploadedFile
from app.ingestion.excel_reader import parse_excel_to_cases
from app.schemas.test_case import TestCaseSchema
from app.schemas.jira import JiraIssue
from app.ingestion.jira_client import JiraClient

def load_input(uploaded_file_id: int, ticket_ids: List[str]) -> Dict[str, List]:
    # 1. Obtener archivo de base de datos
    db = SessionLocal()
    db_file = db.query(UploadedFile).filter(UploadedFile.id == uploaded_file_id).first()
    db.close()

    if not db_file:
        raise ValueError(f"❌ Archivo con ID {uploaded_file_id} no encontrado.")

    # 2. Parsear Excel
    casos_existentes: List[TestCaseSchema] = parse_excel_to_cases(db_file.filepath)

    # 3. Obtener tickets de Jira por key
    jira = JiraClient()
    tickets: List[JiraIssue] = jira.get_issues_by_keys(ticket_ids)

    return {
        "casos_existentes": casos_existentes,
        "tickets": tickets
    }
