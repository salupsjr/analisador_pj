import os
import json
import fitz
from openai import OpenAI
import google.generativeai as genai
from dotenv import load_dotenv
from app.models.schemas import DocumentoSocietario

load_dotenv()
client_openrouter = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
modelo_visao = genai.GenerativeModel("gemini-flash-lite-latest")

def processar_documento(conteudo_pdf: bytes) -> dict:
    documento = fitz.open(stream=conteudo_pdf, filetype="pdf")
    texto_extraido = "".join(pagina.get_text("text") + "\n" for pagina in documento)
        
    esquema_json = DocumentoSocietario.schema_json()
    prompt = f"""
    Você é um analista de Firmas e Poderes sênior. Extraia os dados e retorne EXATAMENTE UM JSON VÁLIDO seguindo este esquema: {esquema_json}
    
    REGRAS CRÍTICAS:
    1. FORMA DE ASSINATURA: Busque a cláusula de Administração (ex: "isoladamente"). Ignore "assinatura eletrônica".
    2. NÚMEROS E MOEDA: Padrão brasileiro. Converta valores para float puro (Ex: "R$ 5.000,00" vira 5000.00). Remova %.
    3. QUADRO SOCIETÁRIO E CPFs: Cruze a tabela de cotas com o preâmbulo (início) para achar o CPF e Nome corretos. NUNCA deixe CPF vazio.
    4. NÚMERO/DATA DA JUNTA COMERCIAL: Procure pela etiqueta/carimbo da Junta em QUALQUER PÁGINA. Extraia o número de arquivamento exato. IGNORE o NIRE do cabeçalho.
    5. ADMINISTRADORES/DIRETORES: Procure a cláusula de administração. Preencha a lista 'administradores' com TODOS os nomeados (Nome, CPF e prazo do mandato, ex: 'Indeterminado' ou 'Determinado'). Inclua tanto os que são sócios quanto os não-sócios.
    6. BOOLEANOS: Todos os campos booleanos devem retornar estritamente true ou false.
    """
    
    if len(texto_extraido.strip()) > 50:
        print("-> PDF Digital detectado. Usando DeepSeek-V3 via OpenRouter...")
        prompt_completo = prompt + f"\nTEXTO DO DOCUMENTO:\n{texto_extraido}"
        
        resposta = client_openrouter.chat.completions.create(
            model="deepseek/deepseek-chat",
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": "Retorne exclusivamente JSON estruturado."}, {"role": "user", "content": prompt_completo}],
            temperature=0.0
        )
        conteudo_json = resposta.choices[0].message.content
    else:
        print("-> PDF Escaneado detectado! Usando Gemini Flash Lite (Modo Economia de Tokens)...")
        conteudo_gemini = [prompt + "\nO documento segue abaixo no formato de imagens (páginas escaneadas). Retorne APENAS o JSON."]
        
        for pagina in documento:
            pix = pagina.get_pixmap(dpi=100)
            img_bytes = pix.tobytes("jpeg")
            conteudo_gemini.append({"mime_type": "image/jpeg", "data": img_bytes})
            
        resposta = modelo_visao.generate_content(
            conteudo_gemini,
            generation_config={"response_mime_type": "application/json"}
        )
        conteudo_json = resposta.text

    dados = json.loads(conteudo_json)
    aplicar_regras_de_negocio(dados)
    return dados

def aplicar_regras_de_negocio(dados: dict):
    regras_proc = (dados.get("regras_outorga_procuracao") or "").lower()
    forma_proc = (dados.get("forma_assinatura_procuracao") or "").strip()
    poderes_amplos = any(s.get("poderes_judiciais_extrajudiciais") == True for s in dados.get("socios", []))
    proibido = "vedado" in regras_proc or "proibido" in regras_proc
    
    if dados.get("permite_outorga_procuracao") == False and poderes_amplos and not proibido:
        dados["permite_outorga_procuracao"] = True
        dados["regras_outorga_procuracao"] = "REGRA 1: Permitida tacitamente (administradores com poderes judiciais)."
        dados["quem_assina_procuracao"] = "Administradores com poderes judiciais e extrajudiciais."

    if dados.get("permite_outorga_procuracao") == True:
        if not forma_proc or forma_proc.lower() == "não informado" or "eletrônica" in forma_proc.lower():
            dados["forma_assinatura_procuracao"] = dados.get("forma_assinatura", "")
            aviso = " | REGRA 3: Forma herdada da administração."
            regras_existentes = dados.get("regras_outorga_procuracao")
            dados["regras_outorga_procuracao"] = (regras_existentes if regras_existentes else "") + aviso

    soma_cotas = round(sum(s.get("porcentagem_participacao", 0) for s in dados.get("socios", [])), 2)
    if not (90.00 <= soma_cotas <= 100.00):
        dados["ALERTA_VALIDACAO"] = f"ATENÇÃO: Soma das cotas é {soma_cotas}%. Aceitável: 90% a 100%."