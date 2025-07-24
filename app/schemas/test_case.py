from pydantic import BaseModel
from typing import Optional
class TestCaseSchema(BaseModel):
    fecha: Optional[str] = None
    id: Optional[str]
    descripcion: Optional[str]
    prioridad: Optional[str]
    tipo: Optional[str]
    precondiciones: Optional[str]
    pasos: Optional[str]
    resultado_esperado: Optional[str]
    estado: Optional[str] = "Pendiente"
    resultado_actual: Optional[str] = "No ejecutado"
