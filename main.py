import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurações do Consultor
MEU_NOME = "Matheus Russi" 
SISTEMA_CONTATO = "5516999930849" 
# Link com mensagem automática para facilitar para o cliente
LINK_WHATSAPP = f"https://wa.me/{SISTEMA_CONTATO}?text=Olá+Matheus,+estava+no+chat+da+Mediquei+e+gostaria+de+uma+consultoria."

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    texto: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        with open("conhecimento.txt", "r", encoding="utf-8") as f:
            contexto = f.read()[:4000]
    except FileNotFoundError:
        contexto = "Mediquei: Especialista em planos de saúde e telemedicina 24h."

    # PROMPT REVISADO: Removida saudação confusa e ajustado formato do link
    prompt_sistema = f"""
    Você é o assistente virtual da Mediquei, trabalhando diretamente para o consultor {MEU_NOME}.
    
    DIRETRIZES DE ESTILO:
    - Nunca diga "ajudar você e o Matheus". Diga "ajudar você a encontrar o melhor plano com o suporte do especialista {MEU_NOME}".
    - Respostas curtas (máximo 3 frases).
    - Quando o usuário perguntar sobre doenças (como Anemia Falciforme), explique que a Mediquei busca redes com especialistas (hematologistas) e agiliza o processo.
    - Sobre horários: Destaque que a telemedicina é 24 horas, 7 dias por semana.
    
    FORMATO DE LINK OBRIGATÓRIO:
    Sempre que oferecer contato, use exatamente este formato Markdown:
    [Falar com o consultor Matheus Russi]({LINK_WHATSAPP})
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": prompt_sistema + "\nCONHECIMENTO:\n" + contexto},
                {"role": "user", "content": request.texto}
            ],
            temperature=0.5,
        )
        return {"resposta": completion.choices[0].message.content}
    except Exception:
        return {"resposta": f"Para detalhes específicos, recomendo [clicar aqui para falar com Matheus Russi]({LINK_WHATSAPP})."}

@app.get("/")
async def root():
    return {"status": "Mediquei IA Ativa"}
