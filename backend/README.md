# TestMind Backend

Este proyecto es el backend de la aplicación **TestMind**, diseñado para gestionar la generación de casos de prueba basados en archivos Excel y tickets de Jira. Está construido con **FastAPI** y utiliza **PostgreSQL** como base de datos.

## Estructura del Proyecto
backend/
├── .env                     # Configuración de variables de entorno
├── .gitignore              # Archivos ignorados por Git
├── Dockerfile              # Configuración de Docker para el backend
├── docker-compose.yml      # Orquestación de servicios con Docker Compose
├── requirements.txt        # Dependencias del proyecto
├── app/                    # Código fuente principal
│   ├── agents/             # Módulos para agentes externos
│   ├── api/                # Endpoints de la API
│   ├── core/               # Configuración y lógica central
│   ├── crud/               # Operaciones CRUD
│   ├── data/               # Gestión de datos
│   ├── db/                 # Conexión y modelos de base de datos
│   ├── export/             # Funcionalidades de exportación
│   ├── ingestion/          # Procesamiento de datos de entrada
│   ├── models/             # Modelos de datos
│   ├── rag/                # Recuperación de información (RAG)
│   ├── schemas/            # Esquemas de validación
│   ├── services/           # Servicios de negocio
│   └── utils/              # Utilidades generales
├── data/                   # Archivos de datos
│   ├── exports/            # Archivos exportados
│   └── uploads/            # Archivos subidos
├── scripts/                # Scripts auxiliares
│   ├── init_db.py              # Inicialización de la base de datos
│   ├── test_case_builder.py    # Generación de casos de prueba
│   ├── test_case_generated.py # Casos de prueba generados
│   ├── test_case_saver.py     # Guardado de casos de prueba
│   ├── test_db_connection.py  # Pruebas de conexión a la base de datos
│   ├── test_input_loader.py   # Carga de datos de entrada
│   ├── test_jira_connection.py# Pruebas de conexión a Jira
│   └── __pycache__/           # Archivos compilados de Python
├── tests/                  # Pruebas del proyecto
│   ├── integration/        # Pruebas de integración
│   └── unit/               # Pruebas unitarias


## Instalación

### Requisitos

- **Python 3.11**
- **Docker** y **Docker Compose**
- **PostgreSQL**

### Pasos

1. Clona el repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd backend

2. Crea un archivo .env basado en el ejemplo proporcionado en el proyecto.

3. Instala las dependencias:
    `pip install -r requirements.txt`

4. Inicia los servicios con Docker Compose:
    `docker-compose up --build`

Endpoints Principales
Archivos Excel
* `POST /excel/upload`: Subir un archivo Excel.
* `GET /excel/list`: Listar archivos Excel disponibles.

Tickets de Jira
* `GET /jira/issues`: Obtener tickets de Jira según filtros.

Casos de Prueba
* `POST /test-cases/generate`: Generar casos de prueba basados en un archivo Excel y tickets de Jira.

Configuración
Variables de Entorno
El archivo `.env` contiene las siguientes configuraciones:

* JIRA_API_BASE: URL base de la API de Jira.
* POSTGRES_HOST: Host de la base de datos PostgreSQL.
* POSTGRES_PORT: Puerto de la base de datos PostgreSQL.
* POSTGRES_NAME: Nombre de la base de datos.
* POSTGRES_USER: Usuario de la base de datos.
* POSTGRES_PASSWORD: Contraseña de la base de datos.
* OPENAI_API_KEY<vscode_annotation details='%5B%7B%22title%22%3A%22hardcoded-credentials%22%2C%22description%22%3A%22Embedding%20credentials%20in%20source%20code%20risks%20unauthorized%20access%22%7D%5D'></vscode_annotation>: Clave de API para OpenAI.

Base de Datos
La base de datos PostgreSQL se configura automáticamente al iniciar el contenedor db en Docker Compose.

Scripts Auxiliares
* `init_db.py`: Inicializa la base de datos.
* `test_jira_connection.py`: Verifica la conexión con Jira.
* `test_db_connection.py`: Verifica la conexión con la base de datos.

Pruebas
Ejecuta las pruebas unitarias e integración con:\
    `pytest tests/`

Desarrollo
Ejecutar en Local
1. Inicia el backend:
    `uvicorn app.api.main:app --reload`
2. Accede a la documentación interactiva en:
    `http://localhost:8000/docs`

Docker
Construcción y Ejecución
Construye y ejecuta el contenedor con:
    `docker-compose up --build`

Servicios
* API Backend: Disponible en http://localhost:8000.
* Base de Datos PostgreSQL: Disponible en localhost:5432.
* PgAdmin: Disponible en http://localhost:5050.