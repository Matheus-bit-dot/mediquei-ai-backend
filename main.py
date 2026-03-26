from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Permite que o GitHub Pages converse com o Render
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
    return {"mensagem": "Mediquei IA Online"}

@app.post("/chat")
async def chat(request: ChatRequest):
    msg = request.texto.lower()
    
    # 1. RESPOSTAS SOBRE PLANOS E CARÊNCIA
    if any(word in msg for word in ["plano", "carência", "carencia", "preço", "valor"]):
        return {"resposta": "A Mediquei oferece planos Individuais, Familiares e Empresariais com ampla rede credenciada. A carência para consultas de rotina é zero em muitos casos! Gostaria que um consultor te enviasse a tabela de preços?"}
    
    # 2. RESPOSTAS SOBRE CONTATO/WHATSAPP (SEU NÚMERO AQUI)
    elif any(word in msg for word in ["contato", "falar com alguém", "consultor", "whatsapp", "atendimento"]):
        return {"resposta": "Você pode falar agora com nossa equipe humana! Clique no ícone do WhatsApp no canto da tela ou chame direto no número: (16) 99993-0849."}

    # 3. RESPOSTAS SOBRE A EMPRESA
    elif any(word in msg for word in ["vende", "o que é", "quem são"]):
        return {"resposta": "Somos a Mediquei, uma plataforma focada em democratizar o acesso à saúde através de tecnologia e orientação médica ágil."}

    # 4. RESPOSTA PARA DÚVIDAS GERAIS (SEU NÚMERO AQUI TAMBÉM)
    else:
        return {"resposta": f"Entendi que você tem dúvidas sobre '{request.texto}'. Como sou uma IA de triagem, o ideal é encaminhar seu caso para um de nossos especialistas. Clique no botão verde do WhatsApp ou nos chame no (16) 99993-0849!"}
