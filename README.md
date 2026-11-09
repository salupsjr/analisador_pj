# 🏢 Analisador PJ - Intelligent Document Processing (IDP)

Este projeto é uma API de Processamento Inteligente de Documentos (IDP) desenvolvida para automatizar a complexa tarefa de **Análise de Firmas e Poderes** (onboarding PJ) em bancos e instituições financeiras. 

O sistema utiliza Inteligência Artificial e Visão Computacional para ler Contratos Sociais, Estatutos e Atas, extrair dados críticos de forma estruturada (JSON) e aplicar regras de negócio determinísticas para validação contra fraudes ou inconsistências.

## 🚀 Tecnologias Utilizadas

* **Backend:** Python 3, FastAPI, Uvicorn
* **Validação e Tipagem:** Pydantic (Structured Outputs)
* **Extração de Texto (PDF):** PyMuPDF (Nível industrial, com leitura profunda de rodapés e carimbos)
* **Motor Cognitivo (LLM):** DeepSeek V3 (Via API do OpenRouter)
* **Arquitetura:** MVC / Service Pattern

## 🧠 Como Funciona o Motor

O diferencial deste projeto não é apenas a extração via IA, mas sim a esteira de **Regras de Negócio** programada no motor (Python). O sistema não confia cegamente no LLM.

**Validações Automáticas Implementadas:**
1. **Regra Matemática de Cotas:** O sistema soma autonomamente a participação de todos os sócios extraídos pela IA. Se o valor fugir da margem aceitável (90% a 100%), um alerta de validação é gerado no JSON final.
2. **Regra de Procuração Tácita:** Se o documento não citar explicitamente a outorga de procurações, mas conceder poderes judiciais/extrajudiciais aos administradores (e não houver vedação), o motor sobrepõe a IA e aprova a emissão de procurações com base em práticas de mercado.
3. **Herança de Governança:** Se a forma de assinatura para procurações for omissa, o sistema herda automaticamente as regras de governança dos administradores principais (ex: assinaturas em conjunto ou isoladas).

## 💻 Como Rodar o Projeto Localmente

1. Clone o repositório:
```bash
git clone https://github.com/salupsjr/analisador_pj
cd analisador_pj


Crie e ative um ambiente virtual (venv):

Bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
Instale as dependências:

Bash
pip install -r requirements.txt
Configure a variável de ambiente:
Crie um arquivo .env na raiz do projeto e insira a sua chave do OpenRouter:

Snippet de código
OPENROUTER_API_KEY=sua_chave_aqui
Inicie o servidor FastAPI:

Bash
uvicorn app.main:app --reload
Acesse o Swagger UI interativo em: http://localhost:8000/docs para fazer o upload dos PDFs e testar a extração.

Desenvolvido por Salustiano Souza Pires Junior (Jr) como projeto de portfólio. É proibido o uso comercial deste código sem autorização.


---

Pronto! Assim que você subir esse `README.md`, o seu repositório vai ter uma "vitrine" de respeito. 