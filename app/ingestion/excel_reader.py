import os
import pandas as pd
from typing import List
from app.schemas.test_case import TestCaseSchema

COLUMNS_MAP = {
    "Fecha": "fecha",
    "ID": "id",
    "Descripción": "descripcion",
    "Prioridad": "prioridad",
    "Tipo de Caso": "tipo_caso",
    "Precondiciones": "precondiciones",
    "Pasos de prueba": "pasos",
    "Resultado Esperado": "resultado_esperado",
    "Estado": "estado",
    "Resultado Actual": "resultado_actual"
}

def parse_excel_to_cases(filepath: str) -> List[TestCaseSchema]:
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ Archivo no encontrado en: {filepath}")
    
    df = pd.read_excel(filepath)

    # Validar que están las columnas necesarias
    missing_cols = [col for col in COLUMNS_MAP if col not in df.columns]
    if missing_cols:
        raise ValueError(f"❌ Faltan columnas requeridas en el Excel: {missing_cols}")

    # Renombrar columnas a claves esperadas
    df = df.rename(columns=COLUMNS_MAP)

    # Asegurar que 'fecha' es string
    if "fecha" in df.columns:
        df["fecha"] = df["fecha"].astype(str)

    # Convertir a lista de objetos
    test_cases = [
        TestCaseSchema(**row.dropna().to_dict())
        for _, row in df.iterrows()
    ]

    return test_cases
