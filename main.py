from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import brain
from database import SessionLocal, Lead

app = FastAPI()

# CONFIGURAÇÃO DE SEGURANÇA (CORS)
# Isso permite que o seu arquivo index.html consiga conversar com o servidor Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens para teste local
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc)
    allow_headers=["*"],
)

# ROTA DE CHAT: Recebe a pergunta e devolve a resposta do Gemini
@app.get("/chat")
async def chat(texto: str):
    try:
        # Chama a lógica do Gemini no arquivo brain.py
        resposta_ia = brain.gerar_resposta(texto)
        return {"resposta": resposta_ia}
    except Exception as e:
        return {"resposta": f"Ops, tive um erro técnico: {str(e)}"}

# ROTA DE LEADS: Salva os dados do cliente no banco de dados SQLite
@app.post("/salvar_lead")
async def salvar_lead(nome: str, whatsapp: str, interesse: str):
    try:
        db = SessionLocal()
        novo_lead = Lead(nome=nome, whatsapp=whatsapp, interesse=interesse)
        db.add(novo_lead)
        db.commit()
        db.refresh(novo_lead)
        db.close()
        return {"status": "sucesso", "mensagem": "Lead salvo com sucesso!"}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

# ROTA INICIAL: Apenas para testar se o servidor está vivo
@app.get("/")
async def root():
    return {"mensagem": "API Mediquei Online e Operante!"}

# Inicia o servidor se rodar como 'python main.py'
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)