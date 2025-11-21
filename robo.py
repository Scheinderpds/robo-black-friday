import requests
from bs4 import BeautifulSoup
import webbrowser
import os

# --- CONFIGURAÇÕES ---
PRECO_MAXIMO = 3000.00
NOME_ARQUIVO = "Relatorio_Ofertas_Final.html"

# Imagens Garantidas
IMAGEM_DETETIVE = "https://img.icons8.com/color/480/sherlock-holmes.png"
IMAGEM_PADRAO_NOTEBOOK = "https://img.icons8.com/fluency/240/laptop.png"

urls = [
    "https://lista.mercadolivre.com.br/notebook-ryzen-5-8gb-ssd",
    "https://lista.mercadolivre.com.br/notebook-intel-i5-8gb-ssd"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def limpar_preco(texto_preco):
    try:
        return float(texto_preco.replace("R$", "").strip().replace(".", "").replace(",", "."))
    except:
        return 0.0

print("="*60)
print(f"🤖 ROBÔ FINAL: Gerando relatório com separação de cores...")
print("="*60)

# --- CSS (ESTILOS) DO SITE ---
estilos_css = """
<style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f4f8; margin: 0; padding: 30px; }
    .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
    h1 { color: #1565c0; text-align: center; margin-bottom: 10px; }
    
    .header-img { display: block; margin: 0 auto 10px auto; width: 150px; height: auto; filter: drop-shadow(0 5px 5px rgba(0,0,0,0.2)); }
    .resumo { text-align: center; margin-bottom: 30px; font-size: 18px; color: #555; font-weight: 500; }
    
    table { width: 100%; border-collapse: separate; border-spacing: 0 15px; } /* Mais espaço entre linhas */
    th { background-color: #263238; color: white; padding: 15px; text-align: left; border-radius: 5px; }
    td { padding: 15px; vertical-align: middle; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    
    /* --- CORES DOS TIMES --- */
    .linux-row td { background-color: #e8f5e9; border: 1px solid #c8e6c9; } /* Verde */
    .windows-row td { background-color: #e3f2fd; border: 1px solid #bbdefb; } /* Azul */
    
    tr:hover td { transform: scale(1.01); transition: all 0.2s ease; box-shadow: 0 8px 15px rgba(0,0,0,0.1); cursor: pointer; }
    
    .prod-foto { width: 100px; height: 100px; object-fit: contain; padding: 5px; background: white; border-radius: 10px; }
    .preco { color: #2e7d32; font-weight: 900; font-size: 1.3em; white-space: nowrap; }
    
    .btn { display: inline-block; background: linear-gradient(45deg, #ff3d00, #ff9100); color: white; padding: 10px 25px; text-decoration: none; border-radius: 50px; font-weight: bold; box-shadow: 0 4px 10px rgba(255, 61, 0, 0.3); transition: transform 0.2s; white-space: nowrap; }
    .btn:hover { transform: translateY(-2px); }
    
    .sistema-tag { font-size: 0.9em; font-weight: bold; display: block; margin-top: 5px; }
</style>
"""

# --- INÍCIO DO HTML ---
html_content = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Relatório SCH Final</title>
    {estilos_css}
</head>
<body>
    <div class="container">
        <img src="{IMAGEM_DETETIVE}" alt="Detetive" class="header-img">
        <h1>Caçador de Notebooks SCH</h1>
        <p class="resumo">🎯 Buscando máquinas novas até <b>R$ {PRECO_MAXIMO:.2f}</b></p>
        
        <table>
            <thead>
                <tr>
                    <th width="120">Foto</th>
                    <th>Modelo e Sistema</th>
                    <th width="150">Preço</th>
                    <th width="100">Ação</th>
                </tr>
            </thead>
            <tbody>
"""

contador = 0
for url in urls:
    try:
        print(f"🔎 Lendo página: {url[:35]}...")
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        produtos = soup.find_all('div', class_='poly-card__content')
        
        for produto in produtos:
            try:
                # Foto
                img_url = IMAGEM_PADRAO_NOTEBOOK
                try:
                    img_tag = produto.find('img')
                    link_encontrado = img_tag.get('data-src') or img_tag.get('src')
                    if link_encontrado and "http" in link_encontrado:
                        img_url = link_encontrado
                except:
                    pass 
                
                titulo = produto.find('a', class_='poly-component__title').get_text()
                link = produto.find('a', class_='poly-component__title')['href']
                preco_texto = produto.find('span', class_='andes-money-amount__fraction').get_text()
                preco_num = limpar_preco(preco_texto)
                
                titulo_lower = titulo.lower()
                
                if (0 < preco_num <= PRECO_MAXIMO) and ("recondicionado" not in titulo_lower) and ("usado" not in titulo_lower):
                    contador += 1
                    
                    # --- AQUI ESTÁ A DIFERENCIAÇÃO DE CORES ---
                    if any(x in titulo_lower for x in ["linux", "ubuntu", "keepos", "gutta"]):
                        # É LINUX
                        texto_sistema = "🐧 LINUX (Economia)"
                        classe_linha = 'class="linux-row"'
                        cor_texto = "#2e7d32" # Verde escuro
                    else:
                        # É WINDOWS
                        texto_sistema = "💻 WINDOWS"
                        classe_linha = 'class="windows-row"'
                        cor_texto = "#1565c0" # Azul escuro
                    
                    html_content += f"""
                    <tr {classe_linha}>
                        <td><img src="{img_url}" alt="Notebook" class="prod-foto"></td>
                        <td>
                            <strong>{titulo}</strong>
                            <span class="sistema-tag" style="color:{cor_texto}">{texto_sistema}</span>
                        </td>
                        <td class="preco">R$ {preco_num:.2f}</td>
                        <td><a href="{link}" target="_blank" class="btn">Ver Oferta 🔥</a></td>
                    </tr>
                    """
                    print(f"✅ {texto_sistema}: {titulo[:20]}...")
            except:
                continue
    except Exception as e:
        print(f"Erro geral: {e}")

html_content += """
            </tbody>
        </table>
        <p style="text-align:center; color:#ccc; margin-top:30px;">Desenvolvido por SCH em Python 🐍</p>
    </div>
</body>
</html>
"""

with open(NOME_ARQUIVO, "w", encoding="utf-8") as f:
    f.write(html_content)

print("-" * 60)
print(f"🚀 Tudo pronto! Relatório Visual Final aberto.")
webbrowser.open('file://' + os.path.realpath(NOME_ARQUIVO))