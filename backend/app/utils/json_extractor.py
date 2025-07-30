import json
import re
from typing import List

def extract_json_objects(text: str) -> List[dict]:
    """
    Extrae múltiples objetos JSON válidos desde un texto.
    """
    json_objects = []
    matches = re.finditer(r"\{.*?\}(?=\s*,?\s*\{|\s*$)", text, re.DOTALL)
    for match in matches:
        try:
            json_obj = json.loads(match.group())
            json_objects.append(json_obj)
        except json.JSONDecodeError as e:
            print(f"❌ Error parseando JSON: {e}")
    return json_objects
