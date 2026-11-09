from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.rotas import router

app = FastAPI(
    title="Analisador PJ - IDP",
    version="1.5",
    description="Arquitetura Profissional Modularizada"
)

# ==========================================
# LIBERAÇÃO DE CORS (Para o Frontend funcionar)
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite que qualquer site local acesse a API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conecta as rotas
app.include_router(router)

@app.get("/")
def raiz():
    return {"status": "Motor online. CORS liberado para o Frontend."}