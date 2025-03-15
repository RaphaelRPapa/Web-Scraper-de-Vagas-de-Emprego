import os
import pandas as pd
import re
from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import csv

# Configuração da API do OpenAI
os.environ["OPENAI_API_KEY"] = "API_KEY"  # Insira sua chave API aqui
client = OpenAI()

def gerar_url_busca():
    termo_pesquisado = input("Digite o tipo de vaga que deseja buscar: ")
    termo_codificado = urllib.parse.quote(termo_pesquisado)
    num_paginas = 70
    return termo_codificado, num_paginas

def buscar_vagas_catho():
    termo_codificado, num_paginas = gerar_url_busca()
    base_url = f"https://www.catho.com.br/vagas/{termo_codificado}/"

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    with open('vagas.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Título', 'Empresa', 'Localização', 'Data de Publicação', 'Faixa Salarial', 'Descrição', 'URL da Vaga'])

        for page in range(1, num_paginas + 1):
            url_busca = f"{base_url}?page={page}"
            print(f"Buscando na URL: {url_busca}")

            driver.get(url_busca)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "search-result-custom_jobItem__OGz3a")))
            vagas = driver.find_elements(By.CLASS_NAME, "search-result-custom_jobItem__OGz3a")

            for vaga in vagas:
                try:
                    titulo = vaga.find_element(By.TAG_NAME, "h2").text.replace("\n", " ")
                    empresa = vaga.find_element(By.CLASS_NAME, "sc-sLsrZ").text.replace("\n", " ")
                    localizacao = vaga.find_element(By.TAG_NAME, "button").text.replace("\n", " ")
                    data_publicacao = vaga.find_element(By.TAG_NAME, "time").text.replace("\n", " ")
                    faixa_salarial = vaga.find_element(By.CLASS_NAME, "custom-styled_salaryText__oSvPo").text.replace("\n", " ") if vaga.find_elements(By.CLASS_NAME, "custom-styled_salaryText__oSvPo") else "Não especificado"
                    descricao = vaga.find_element(By.CLASS_NAME, "job-description").text.replace("\n", " ") if vaga.find_elements(By.CLASS_NAME, "job-description") else "Descrição não disponível"
                    url_vaga = vaga.find_element(By.TAG_NAME, "a").get_attribute("href")

                    writer.writerow([titulo, empresa, localizacao, data_publicacao, faixa_salarial, descricao, url_vaga])
                except Exception as e:
                    print(f"Erro ao extrair dados da vaga: {e}")

    driver.quit()
    print("Dados salvos em vagas.csv com sucesso!")

# Função para pré-processar texto e extrair palavras-chave e tecnologias mencionadas
def extrair_palavras_chave(texto):
    stop_words = {"de", "da", "do", "em", "para", "e", "o", "a", "os", "as", "um", "uma", "com", "por", "que", "não", "na", "no", "nas", "nos"}
    palavras = str(texto).lower().split()
    palavras_filtradas = [p for p in palavras if p.isalnum() and p not in stop_words]
    return palavras_filtradas

# Função para extrair tecnologias e experiência usando expressões regulares
def extrair_tecnologias_anos(texto):
    tecnologias = re.findall(r'\b(Java|Python|SQL|HTML|CSS|JavaScript|React|Node\.js|Angular)\b', texto, re.IGNORECASE)
    anos_experiencia = re.findall(r'(\d+)\s*anos?\s*de\s*experiência', texto, re.IGNORECASE)
    anos_experiencia = [int(ano) for ano in anos_experiencia] if anos_experiencia else [0]
    return tecnologias, max(anos_experiencia, default=0)

def analisar_vagas():
    # Carregar a base de dados
    df = pd.read_csv('vagas.csv')

    # Análise Descritiva
    analise_descritiva = {
        "Número total de vagas": len(df),
        "Distribuição de empresas": df['Empresa'].value_counts().head(10).to_dict(),
        "Localizações mais comuns": df['Localização'].value_counts().head(10).to_dict()
    }

    # Processar colunas e extrair palavras-chave, tecnologias e experiência
    df['Palavras_Chave_Titulo'] = df['Título'].apply(extrair_palavras_chave)
    df['Palavras_Chave_Descricao'] = df['Descrição'].apply(extrair_palavras_chave)
    df['Tecnologias'], df['Anos_Experiencia'] = zip(*df['Descrição'].apply(extrair_tecnologias_anos))

    # Análise de Frequência das Palavras e Tecnologias
    todas_palavras = [palavra for lista in df['Palavras_Chave_Titulo'] + df['Palavras_Chave_Descricao'] for palavra in lista]
    frequencia_palavras = pd.Series(todas_palavras).value_counts()

    todas_tecnologias = [tec for lista in df['Tecnologias'] for tec in lista]
    frequencia_tecnologias = pd.Series(todas_tecnologias).value_counts()

    media_experiencia = df['Anos_Experiencia'].mean()

    # Gerar relatório com as análises
    with open('relatorio_insights.txt', 'w') as f:
        f.write("Análise Descritiva das Vagas:\n")
        f.write(f"Número total de vagas: {analise_descritiva['Número total de vagas']}\n")
        f.write("Distribuição de empresas:\n")
        for empresa, contagem in analise_descritiva['Distribuição de empresas'].items():
            f.write(f" - {empresa}: {contagem}\n")
        f.write("Localizações mais comuns:\n")
        for localizacao, contagem in analise_descritiva['Localizações mais comuns'].items():
            f.write(f" - {localizacao}: {contagem}\n")

        f.write("\nHabilidades mais mencionadas nas descrições:\n")
        for palavra, contagem in frequencia_palavras.head(10).items():
            f.write(f" - {palavra}: {contagem}\n")

        f.write("\nTecnologias mais mencionadas nas descrições:\n")
        for tecnologia, contagem in frequencia_tecnologias.items():
            f.write(f" - {tecnologia}: {contagem}\n")

        f.write(f"\nAnos de experiência média requerida: {media_experiencia:.2f} anos\n")

    # Função para obter insights usando a API OpenAI
    def obter_insights(pergunta, dados):
        contexto = f"A base de dados contém as seguintes informações de vagas de TI: {dados}."
        mensagem = f"{contexto}\n\n{pergunta}"

        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": mensagem}]
        )
        return resposta.choices[0].message.content

    # Preparar os dados para enviar como contexto
    dados_contexto = df[['Título', 'Faixa Salarial', 'URL da Vaga', 'Tecnologias', 'Anos_Experiencia']].to_dict(orient='records')

    # Perguntas para obter insights do mercado de trabalho
    perguntas = [
        "Com base nas vagas apresentadas, quais habilidades estão em maior demanda? Por favor, organize as informações em tópicos com introdução e conclusão.",
        "Quais tecnologias emergentes podem ser inferidas a partir das descrições das vagas? Apresente as informações de forma estruturada.",
        "Quais tecnologias relacionadas ao desenvolvimento Java estão associadas a salários mais altos? Use listas para apresentar as informações claramente.",
    ]

    # Gerar insights e salvar no relatório
    with open('relatorio_insights.txt', 'a') as f:
        for pergunta in perguntas:
            f.write(f"\nInsights sobre a pergunta: {pergunta}\n")
            insights = obter_insights(pergunta, dados_contexto)
            f.write(insights + "\n")
            f.write(f"\n-----------------------------------------------------------\n")

# Execução das funções
buscar_vagas_catho()
analisar_vagas()
