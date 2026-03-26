from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Permite que o seu site no GitHub acesse o servidor no Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    texto: str

@app.get("/")
async def root():
    return {"mensagem": "API Mediquei Online e Operante!"}

@app.post("/chat")
async def chat(request: ChatRequest):
    user_message = request.texto.lower()
    
    # Lógica simples de resposta (Você pode integrar com OpenAI/Gemini aqui depois)
    if "vende" in user_message:
        resposta_final = "A Mediquei é uma plataforma de orientação em saúde. No momento, oferecemos consultoria digital e auxílio em dúvidas médicas básicas."
    elif "oi" in user_message or "olá" in user_message:
        resposta_final = "Olá! Como posso ajudar você hoje?"
    else:
        resposta_final = "Entendi. Poderia me dar mais detalhes sobre sua dúvida de saúde?"

    return {"resposta": resposta_final}
