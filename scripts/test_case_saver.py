from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.agents.case_builder_agent import CaseBuilderAgent
from app.services.input_loader import load_input
from app.services.test_case_saver import save_generated_cases

# Simulamos una corrida para un archivo + tickets
file_id = "1"  # Usa uno real
ticket_ids = ["APISIUCC-897"]  # Podés pasar más si querés

# Cargar ejemplos + tickets
input_data = load_input(file_id, ticket_ids)

ejemplos = input_data["casos_existentes"]
tickets = input_data["tickets"]

agent = CaseBuilderAgent()
generated_cases = agent.build_cases(tickets, ejemplos)

db: Session = SessionLocal()
for ticket, case in zip(tickets, generated_cases):
    saved = save_generated_cases(db, [case], ticket.key)
    print(f"✅ Guardado caso para {ticket.key} -> ID: {saved[0].id}")
