from fastapi import FastAPI
from app.api.rotas import router

app = FastAPI(
    title="Analisador PJ - IDP",
    version="1.5",
    description="Arquitetura Profissional Modularizada"
)

# Conecta as rotas do arquivo rotas.py
app.include_router(router)

@app.get("/")
def raiz():
    return {"status": "Motor online. Arquitetura MVC configurada."}