from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import google.generativeai as genai
import json

# Configurar a API do Gemini
genai.configure(api_key="SUA_KEY") 
model = genai.GenerativeModel("gemini-2.0-flash-exp")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Requisicao(BaseModel):
    tema: str = "Matemática"
    nivel: str = "5º ano"

def extrair_json_limpo(texto: str) -> str:
    texto = texto.strip()
    if texto.startswith("```") and texto.endswith("```"):
        texto = texto.strip("`").strip()
        if texto.startswith("json"):
            texto = texto[4:].strip()
    return texto

@app.post("/gerar_questao")
def gerar_questao(req: Requisicao):
    prompt = f"""
Você é um gerador de questões objetivas (múltipla escolha) para o Ensino Fundamental.
Você é especializado em: Língua Portuguesa, Matemática, História, Geografia, Ciências (Física, Química, Biologia), Educação Física, Artes, Inglês, Filosofia e Sociologia.

Gere uma nova questão de {req.tema}, voltada para alunos do {req.nivel}, em formato JSON **sem markdown ou texto explicativo**, respeitando o modelo abaixo.

Tente variar o conteúdo: explore bem a dinâmica da matéria. 
Instruções obrigatórias:
- Evite repetir qualquer questão já utilizada anteriormente na sessão.
- Evite gerar questões muito semelhantes às anteriores. Varie o contexto, o estilo do enunciado e o foco do conteúdo.
- Aumente gradualmente o nível de dificuldade das questões dentro da série escolar especificada em "{req.nivel}".
- Explore diferentes tipos de abordagem dentro do tema proposto, incluindo aplicações práticas, situações-problema, interpretação e análise de conteúdo.

Responda apenas com o JSON válido como este modelo:

{{
  "titulo": "Título da Questão (até 100 caracteres)",
  "materia": "{req.tema}",
  "nivel": "Fácil",
  "enunciado": "Texto completo da pergunta (até 280 caracteres)",
  "alternativas": [
    {{
      "texto": "Texto da alternativa A (até 100 caracteres)",
      "correta": true/false
    }},
    {{
      "texto": "Texto da alternativa B (até 100 caracteres)",
      "correta": true/false
    }},
    {{
      "texto": "Texto da alternativa C (até 100 caracteres)",
      "correta": true/false
    }},
    {{
      "texto": "Texto da alternativa D (até 100 caracteres)",
      "correta": true/false
    }}
  ],
  "justificativa": "Explicação concisa da resposta correta (até 150 caracteres)"
}}
"""
    try:
        response = model.generate_content(prompt)
        texto_limpo = extrair_json_limpo(response.text)
        questao_json = json.loads(texto_limpo)
        return questao_json
    except Exception as e:
        return JSONResponse(content={"erro": str(e), "resposta_bruta": response.text}, status_code=500)
