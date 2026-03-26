import os
from groq import Groq

# --- CONFIGURAÇÃO DE SEGURANÇA ---
# O código agora busca a chave no "sistema" (ambiente). 
# Isso impede que o GitHub bloqueie seu arquivo.
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Se você estiver testando no seu PC e não configurou a variável de ambiente ainda,
# você pode colocar a chave aqui temporariamente, MAS NÃO MANDE PARA O GITHUB ASSIM.
if not GROQ_API_KEY:
    GROQ_API_KEY = "COLOQUE_SUA_CHAVE_AQUI_APENAS_PARA_TESTE_LOCAL"

# --- CONFIGURAÇÃO UNIFICADA DO ATENDIMENTO ---
MEU_NOME = "Matheus Russi" 
SISTEMA_CONTATO = "5516999930849" 
LINK_WHATSAPP = f"https://wa.me/{SISTEMA_CONTATO}"

# Inicializa o cliente Groq
client = Groq(api_key=GROQ_API_KEY)

def gerar_resposta(pergunta_usuario):
    try:
        # Tenta ler o arquivo de conhecimento
        with open("conhecimento.txt", "r", encoding="utf-8") as f:
            contexto = f.read()[:4000]
    except FileNotFoundError:
        contexto = "Mediquei: Telemedicina 24h e benefícios de saúde."

    prompt_sistema = f"""
    Você é o consultor digital da Mediquei.
    Responda de forma humana e breve (2 a 3 frases).
    Use o CONHECIMENTO abaixo para explicar o que o cliente perguntou.
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
        return completion.choices[0].message.content
    except Exception as e:
        return f"Olá! Fale com {MEU_NOME} no WhatsApp para detalhes: {LINK_WHATSAPP}"