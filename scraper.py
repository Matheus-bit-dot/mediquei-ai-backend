import requests
from bs4 import BeautifulSoup

def extrair_dados_mediquei():
    urls = ["https://www.mediquei.com/", "https://www.mediquei.com/corporativo"]
    conhecimento = ""
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Limpa o texto do site
        conhecimento += soup.get_text(separator=' ', strip=True)
    
    with open("conhecimento.txt", "w", encoding="utf-8") as f:
        f.write(conhecimento)
    return "Base de conhecimento atualizada!"

if __name__ == "__main__":
    extrair_dados_mediquei()