import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class TestCaseGenerated(Base):
    __tablename__ = "test_cases_generated"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    ticket_key = Column(String, index=True, nullable=False)
    descripcion = Column(Text, nullable=False)
    prioridad = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    precondiciones = Column(Text, nullable=False)
    pasos = Column(Text, nullable=False)
    resultado_esperado = Column(Text, nullable=False)
    estado = Column(String, nullable=False, default="Pendiente")
    resultado_actual = Column(String, nullable=False, default="No ejecutado")
    fecha_generado = Column(DateTime, default=datetime.utcnow)
