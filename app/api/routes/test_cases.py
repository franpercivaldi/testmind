from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from typing import List
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.request import GenerateTestCasesRequest
from app.schemas.test_case import TestCaseSchema
from app.services.input_loader import load_input
from app.services.test_case_saver import save_generated_cases
from app.agents.case_builder_agent import CaseBuilderAgent
from app.crud.test_case_generated import get_cases_by_ticket
from app.services.excel_exporter import export_cases_to_excel
from app.schemas.request import ExportTestCasesRequest

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

@router.get("/generated", response_model=List[TestCaseSchema])
def list_generated_cases(ticket_key: str = Query(..., description="Clave del ticket de Jira (ej: APISIUCC-100)")):
    db: Session = SessionLocal()
    casos = get_cases_by_ticket(db, ticket_key)

    if not casos:
        raise HTTPException(status_code=404, detail="No se encontraron casos generados para este ticket")

    return [
        TestCaseSchema(
            id=str(c.id),
            descripcion=c.descripcion,
            prioridad=c.prioridad,
            tipo=c.tipo,
            precondiciones=c.precondiciones,
            pasos=c.pasos,
            resultado_esperado=c.resultado_esperado,
            estado=c.estado,
            resultado_actual=c.resultado_actual,
            fecha=str(c.fecha_generado.date()) if c.fecha_generado else None
        )
        for c in casos
    ]
    
@router.post("/export")
def export_test_cases(payload: ExportTestCasesRequest):
    db: Session = SessionLocal()

    try:
        filepath = export_cases_to_excel(db, payload.ticket_keys)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    filename = filepath.split("/")[-1]
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )