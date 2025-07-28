import os
from typing import List
from datetime import datetime
from openpyxl import Workbook
from app.models.test_case_generated import TestCaseGenerated
from sqlalchemy.orm import Session


EXPORT_FOLDER = "data/exports"

def export_cases_to_excel(db: Session, ticket_keys: List[str]) -> str:
    # Crear carpeta si no existe
    os.makedirs(EXPORT_FOLDER, exist_ok=True)

    # Buscar todos los casos para los tickets indicados
    cases = db.query(TestCaseGenerated).filter(TestCaseGenerated.ticket_key.in_(ticket_keys)).all()

    if not cases:
        raise ValueError("No se encontraron casos para los ticket_keys proporcionados.")

    # Crear workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Casos Generados"

    # Escribir encabezado
    headers = [
        "ID", "Descripción", "Prioridad", "Tipo", "Precondiciones",
        "Pasos", "Resultado Esperado", "Estado", "Resultado Actual",
        "Ticket Key", "Fecha Generado"
    ]
    ws.append(headers)

    # Escribir datos
    for case in cases:
        ws.append([
            str(case.id),
            case.descripcion,
            case.prioridad,
            case.tipo,
            case.precondiciones,
            case.pasos,
            case.resultado_esperado,
            case.estado,
            case.resultado_actual,
            case.ticket_key,
            case.fecha_generado.strftime("%Y-%m-%d %H:%M:%S")
        ])

    # Guardar archivo con nombre único
    filename = f"casos_generados_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.xlsx"
    filepath = os.path.join(EXPORT_FOLDER, filename)
    wb.save(filepath)

    return filepath
