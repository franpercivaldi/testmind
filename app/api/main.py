from fastapi import FastAPI
from app.api.routes import jira, upload

app = FastAPI()

app.include_router(jira.router)
app.include_router(upload.router)

@app.get("/")
def root():
    return {"msg": "TestMind API funcionando ✅"}
