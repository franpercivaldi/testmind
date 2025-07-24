from app.db.base import engine, Base
from app.models.uploaded_file import UploadedFile
from app.core.config import settings
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database_if_not_exists():
    conn = psycopg2.connect(
        dbname="postgres",
        user=settings.postgres_user,
        password=settings.postgres_password,
        host=settings.postgres_host,
        port=settings.postgres_port,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{settings.postgres_name}'")
    exists = cursor.fetchone()

    if not exists:
        print(f"🆕 Creando base de datos '{settings.postgres_name}'...")
        cursor.execute(f'CREATE DATABASE "{settings.postgres_name}"')
    else:
        print(f"✔️ La base de datos '{settings.postgres_name}' ya existe.")

    cursor.close()
    conn.close()

def init():
    create_database_if_not_exists()
    print("🔧 Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas.")

if __name__ == "__main__":
    init()
