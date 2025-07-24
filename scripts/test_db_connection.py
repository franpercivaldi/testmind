from sqlalchemy import text
from app.db.session import engine

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("✅ ¡Conexión a la base de datos exitosa!")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
