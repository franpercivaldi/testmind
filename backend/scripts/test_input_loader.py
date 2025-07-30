from app.services.input_loader import load_input

if __name__ == "__main__":
    file_id = 5
    ticket_ids = ["APISIUCC-926", "APISIUCC-925"]

    result = load_input(file_id, ticket_ids)

    print(f"✅ Casos existentes: {len(result['casos_existentes'])}")
    print(f"✅ Tickets cargados: {[t.key for t in result['tickets']]}")
