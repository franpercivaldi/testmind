from sqlalchemy.orm import Session
from app.models.test_case_generated import TestCaseGenerated
from typing import List

def get_cases_by_ticket(db: Session, ticket_key: str) -> List[TestCaseGenerated]:
    return db.query(TestCaseGenerated).filter(TestCaseGenerated.ticket_key == ticket_key).all()
