from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.extrator_ia import processar_documento

router = APIRouter()

@router.post("/extrair")
async def extrair_dados(arquivo: UploadFile = File(...)):
    if not arquivo.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Apenas PDF permitido.")
    
    try:
        conteudo_pdf = await arquivo.read()
        dados = processar_documento(conteudo_pdf)
        return dados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")