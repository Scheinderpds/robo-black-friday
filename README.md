# 🕵️‍♂️ Caçador de Notebooks - Black Friday Edition

Projeto desenvolvido durante o 1º semestre de Análise e Desenvolvimento de Sistemas (ADS).
O objetivo é monitorar preços de notebooks no Mercado Livre e identificar as melhores oportunidades custo-benefício automaticamente.

## 🚀 Funcionalidades

- **Web Scraping:** Coleta dados reais do Mercado Livre (Título, Preço, Link e Imagem).
- **Filtro Inteligente:** Ignora produtos usados ou recondicionados.
- **Análise de Sistema:** Identifica se o notebook é Linux (Time Verde 🐧) ou Windows (Time Azul 💻).
- **Relatório Visual:** Gera um dashboard em HTML automático com as ofertas encontradas.

## 🛠️ Tecnologias Utilizadas

- Python 3.14
- Biblioteca `requests` (Conexão HTTP)
- Biblioteca `BeautifulSoup4` (Extração de dados)
- HTML5 & CSS3 (Front-end do relatório)

## 📸 Como funciona
O script varre a internet, aplica as regras de negócio (Preço Máximo R$ 3.000) e gera um arquivo HTML interativo para visualização.

---
*Desenvolvido por Scheneider Pereira dos Santos
