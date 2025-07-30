from app.db.base import Base
from app.db.session import engine

# Importar todos los modelos aquí
from app.models import test_case_generated, uploaded_file

def init_db():
    print("🛠️  Creando las tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas correctamente.")

if __name__ == "__main__":
    init_db()
