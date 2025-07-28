from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.request import GenerateTestCasesRequest
from app.schemas.test_case import TestCaseSchema
from app.services.input_loader import load_input
from app.services.test_case_saver import save_generated_cases
from app.agents.case_builder_agent import CaseBuilderAgent

router = APIRouter(prefix="/test-cases", tags=["Test Cases"])

@router.post("/generate", response_model=List[TestCaseSchema])
def generate_test_cases(payload: GenerateTestCasesRequest):
    db: Session = SessionLocal()
    input_data = load_input(payload.file_id, payload.ticket_ids)

    if not input_data["tickets"]:
        raise HTTPException(status_code=404, detail="No se encontraron tickets válidos")

    agent = CaseBuilderAgent()
    generated_cases = agent.build_cases(input_data["tickets"], input_data["casos_existentes"])

    saved_schemas = []

    for ticket_key, case in generated_cases:
        saved_orm_list = save_generated_cases(db, [case], ticket_key)

        for s in saved_orm_list:
            saved_schemas.append(TestCaseSchema(
                id=str(s.id),
                descripcion=s.descripcion,
                prioridad=s.prioridad,
                tipo=s.tipo,
                precondiciones=s.precondiciones,
                pasos=s.pasos,
                resultado_esperado=s.resultado_esperado,
                estado=s.estado,
                resultado_actual=s.resultado_actual,
                fecha=str(s.fecha_generado.date()) if s.fecha_generado else None
            ))


    return saved_schemas
