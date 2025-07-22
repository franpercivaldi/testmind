from pydantic import BaseModel
from typing import Optional

class TestCaseSchema(BaseModel):
    fecha: Optional[str]
    id: Optional[str]
    descripcion: str
    prioridad: Optional[str]
    tipo_caso: Optional[str]
    precondiciones: Optional[str]
    pasos: Optional[str]
    resultado_esperado: Optional[str]
    estado: Optional[str]
    resultado_actual: Optional[str]
