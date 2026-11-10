import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega a chave do arquivo .env
load_dotenv()

# Configura a biblioteca do Google com a sua chave
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Buscando modelos do Google Gemini disponíveis...\n")

try:
    total = 0
    # O loop percorre todos os modelos que a sua chave tem acesso
    for modelo in genai.list_models():
        # Filtra para mostrar preferencialmente os modelos de geração de conteúdo (texto/visão)
        if 'generateContent' in modelo.supported_generation_methods:
            print(f"ID: {modelo.name}")
            print(f"Descrição: {modelo.description}\n")
            total += 1
            
    print(f"Total de modelos de geração encontrados: {total}")

except Exception as e:
    print(f"Erro ao buscar modelos. Detalhe: {e}")
    print("Verifique se a sua GEMINI_API_KEY está correta no arquivo .env")