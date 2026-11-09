import os
import json
import fitz
from openai import OpenAI
from dotenv import load_dotenv
from app.models.schemas import DocumentoSocietario

# Carrega a chave do arquivo .env secretamente
load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def processar_documento(conteudo_pdf: bytes) -> dict:
    # 1. Extração de Texto
    documento = fitz.open(stream=conteudo_pdf, filetype="pdf")
    texto_extraido = "".join(pagina.get_text("text") + "\n" for pagina in documento)
        
    esquema_json = DocumentoSocietario.schema_json()
    prompt = f"""
    Você é um analista de Firmas e Poderes sênior.
    Extraia os dados do documento societário e retorne EXATAMENTE UM JSON VÁLIDO seguindo este esquema: {esquema_json}
    
    ATENÇÃO - REGRAS DE EXTRAÇÃO:
    1. FORMA DE ASSINATURA: Busque a cláusula de Administração. A forma de assinatura refere-se a governança (ex: "isoladamente", "em conjunto por dois diretores"). Ignore totalmente menções a "assinatura eletrônica", "gov.br" ou "certificado digital".
    
    TEXTO DO DOCUMENTO:
    {texto_extraido}
    """
    
    # 2. Chamada da IA
    resposta = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Retorne exclusivamente JSON estruturado."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )
    
    dados = json.loads(resposta.choices[0].message.content)
    
    # 3. Regras de Negócio
    aplicar_regras_de_negocio(dados)
    
    return dados

def aplicar_regras_de_negocio(dados: dict):
    # Proteção contra NoneType
    regras_proc_raw = dados.get("regras_outorga_procuracao")
    regras_proc = (regras_proc_raw if regras_proc_raw else "").lower()
    
    forma_proc_raw = dados.get("forma_assinatura_procuracao")
    forma_proc = (forma_proc_raw if forma_proc_raw else "").strip()

    # Regra 1: Procuração
    poderes_amplos = any(s.get("poderes_judiciais_extrajudiciais") == True for s in dados.get("socios", []))
    proibido = "vedado" in regras_proc or "proibido" in regras_proc
    
    if dados.get("permite_outorga_procuracao") == False and poderes_amplos and not proibido:
        dados["permite_outorga_procuracao"] = True
        dados["regras_outorga_procuracao"] = "REGRA 1: Permitida tacitamente (administradores com poderes judiciais)."
        dados["quem_assina_procuracao"] = "Administradores com poderes judiciais e extrajudiciais."

    # Regra 3: Assinatura Procuração
    if dados.get("permite_outorga_procuracao") == True:
        if not forma_proc or forma_proc.lower() == "não informado" or "eletrônica" in forma_proc.lower():
            dados["forma_assinatura_procuracao"] = dados.get("forma_assinatura", "")
            aviso = " | REGRA 3: Forma herdada da administração."
            regras_existentes = dados.get("regras_outorga_procuracao")
            dados["regras_outorga_procuracao"] = (regras_existentes if regras_existentes else "") + aviso

    # Regra 2: Matemática
    soma_cotas = round(sum(s.get("porcentagem_participacao", 0) for s in dados.get("socios", [])), 2)
    if not (90.00 <= soma_cotas <= 100.00):
        dados["ALERTA_VALIDACAO"] = f"ATENÇÃO: Soma das cotas é {soma_cotas}%. Aceitável: 90% a 100%."