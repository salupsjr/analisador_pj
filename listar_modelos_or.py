import requests

url = "https://openrouter.ai/api/v1/models"
resposta = requests.get(url)

if resposta.status_code == 200:
    dados = resposta.json()
    print(f"Total de modelos encontrados no OpenRouter: {len(dados['data'])}\n")
    
    for modelo in dados["data"]:
        # Imprime o ID (nome que vai no código) e o nome comercial do modelo
        print(f"ID: {modelo['id']} | Nome: {modelo['name']}")
else:
    print("Erro ao buscar modelos.")