from app.core.database import SessionLocal

try:
    db = SessionLocal()
    db.execute("SELECT 1")
    print("✅ Conexión exitosa a PostgreSQL")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
finally:
    db.close()
