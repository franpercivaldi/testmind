from fastapi import FastAPI
from app.api.routes import jira

app = FastAPI()
app.include_router(jira.router)

@app.get("/")
def root():
    return {"msg": "TestMind API funcionando ✅"}
