from sqlalchemy.orm import Session
from app.models.test_case_generated import TestCaseGenerated
from app.schemas.test_case import TestCaseSchema
from typing import List


def save_generated_cases(
    db: Session, cases: List[TestCaseSchema], ticket_key: str) -> List[TestCaseGenerated]:
    saved = []

    for case in cases:
        case_db = TestCaseGenerated(
            ticket_key=ticket_key,
            descripcion=case.descripcion,
            prioridad=case.prioridad,
            tipo=case.tipo,
            precondiciones=case.precondiciones,
            pasos=case.pasos,
            resultado_esperado=case.resultado_esperado,
            estado=case.estado,
            resultado_actual=case.resultado_actual,
        )
        db.add(case_db)
        saved.append(case_db)

    db.commit()
    return saved
