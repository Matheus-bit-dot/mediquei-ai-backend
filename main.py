import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

# Permite que o GitHub Pages acesse o backend no Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurações do Atendimento
MEU_NOME = "Matheus Russi" 
SISTEMA_CONTATO = "5516999930849" 
LINK_WHATSAPP = f"https://wa.me/{SISTEMA_CONTATO}"

# Inicializa o cliente Groq buscando a chave no Render
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    texto: str

@app.post("/chat")
async def chat(request: ChatRequest):
    pergunta_usuario = request.texto
    
    # 1. Tenta ler o conhecimento local
    try:
        with open("conhecimento.txt", "r", encoding="utf-8") as f:
            contexto = f.read()[:4000]
    except FileNotFoundError:
        contexto = "Mediquei: Especialista em planos de saúde, telemedicina e redução de carência."

    # 2. Prompt do Sistema (A "alma" da IA)
    prompt_sistema = f"""
    Você é o consultor digital da Mediquei.
    Responda de forma humana, empática e breve (2 a 3 frases).
    Use o CONHECIMENTO abaixo para explicar o que o cliente perguntou e mostre como a Mediquei ajuda.
    Sempre finalize convidando o cliente para falar com o consultor {MEU_NOME}.
    O link de fechamento obrigatório é: {LINK_WHATSAPP}

    CONHECIMENTO:
    {contexto}
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": pergunta_usuario}
            ],
            temperature=0.6,
            max_tokens=300,
        )
        resposta = completion.choices[0].message.content
        return {"resposta": resposta}
    except Exception as e:
        return {"resposta": f"Olá! Tive um pequeno soluço técnico. Fale direto com o {MEU_NOME} no WhatsApp para detalhes: {LINK_WHATSAPP}"}

@app.get("/")
async def root():
    return {"status": "Mediquei IA (Llama 3.3) Online"}
