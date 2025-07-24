from typing import List
from app.schemas.jira import JiraIssue
from app.schemas.test_case import TestCaseSchema
from app.core.openai_client import chat_completion
from app.utils.json_extractor import extract_json_objects
import json

class CaseBuilderAgent:
    def __init__(self):
        pass

    def build_cases(self, tickets: List[JiraIssue], ejemplos: List[TestCaseSchema] = []) -> List[TestCaseSchema]:
        casos_generados: List[TestCaseSchema] = []

        for ticket in tickets:
            prompt = self._build_prompt(ticket, ejemplos)
            try:
                response = chat_completion(prompt)
                print(f"🔎 Respuesta bruta de OpenAI:\n{response}")

                parsed_cases = extract_json_objects(response)

                for data in parsed_cases:
                    try:
                        caso = TestCaseSchema(**data)
                        casos_generados.append(caso)
                    except Exception as e:
                        print(f"❌ Error validando schema para {ticket.key}: {e}")

            except Exception as e:
                print(f"❌ Error generando caso para {ticket.key}: {e}")

        return casos_generados

    def _build_prompt(self, ticket: JiraIssue, ejemplos: List[TestCaseSchema]) -> List[dict]:
        examples_text = "\n".join(
            f"""
            ID: {e.id or 'TC-001'}
            Descripción: {e.descripcion}
            Prioridad: {e.prioridad}
            Tipo de Caso: {e.tipo}
            Precondiciones: {e.precondiciones}
            Pasos de prueba: {e.pasos}
            Resultado Esperado: {e.resultado_esperado}
            """ for e in ejemplos[:2]  # solo algunos ejemplos
        )

        system = {
            "role": "system",
            "content": (
                "Eres un experto en QA. Tu tarea es generar varios casos de prueba "
                "a partir de la descripción de un ticket de Jira. Devuelve estrictamente "
                "una lista JSON válida. No incluyas ningún texto adicional fuera del JSON.\n\n"
                "Formato esperado: una lista de objetos JSON como esta:\n"
                "[\n"
                "  {\n"
                '    "id": "TC-001",\n'
                '    "fecha": "2024-07-17",\n'
                '    "descripcion": "...",\n'
                '    "prioridad": "Alta",\n'
                '    "tipo": "Funcional",\n'
                '    "precondiciones": "...",\n'
                '    "pasos": "1. Paso uno\\n2. Paso dos",\n'
                '    "resultado_esperado": "...",\n'
                '    "estado": "Pendiente",\n'
                '    "resultado_actual": "No ejecutado"\n'
                "  },\n"
                "  ...\n"
                "]"
            )
        }

        user = {
            "role": "user",
            "content": f"""
            Ticket:
            Título: {ticket.summary}
            Descripción: {ticket.description or "Sin descripción"}

            Ejemplos:
            {examples_text or "No hay ejemplos"}

            Genera de 1 a 3 casos de prueba como una lista JSON válida. No agregues explicaciones.
            """
        }

        return [system, user]
