from pydantic import BaseModel
from typing import Optional
from datetime import date

class TestCaseSchema(BaseModel):
    fecha: Optional[date] = None
    id: Optional[str]
    descripcion: Optional[str]
    prioridad: Optional[str]
    tipo: Optional[str]
    precondiciones: Optional[str]
    pasos: Optional[str]
    resultado_esperado: Optional[str]
    estado: Optional[str] = "Pendiente"
    resultado_actual: Optional[str] = "No ejecutado"
