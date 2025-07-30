from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import jira, upload, test_cases

app = FastAPI()

app.include_router(jira.router)
app.include_router(upload.router)
app.include_router(test_cases.router)


# Lista de orígenes permitidos
origins = [
    "http://localhost:5173",  # tu frontend local
    # "https://tu-dominio.com",  // si lo publicás en prod
]

# Activar middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # o ['*'] si querés permitir todos
    allow_credentials=True,
    allow_methods=["*"],     # podés restringir si querés
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"msg": "TestMind API funcionando ✅"}
