# -*- coding: utf-8 -*-
"""scrapping_ev.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1O8pS5nGG2IPZZdp-_rGz754xRDcSekHs

### 1. Importando as bibliotecas
"""

#!pip install pandas
#!pip install selenium
#!pip install sqlalchemy

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by  import By
from datetime import datetime
import sqlalchemy as db
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

"""### 2. Acessando a página"""

chrome_options = Options()
chrome_options.add_argument("--disable-notifications")

navegador = webdriver.Chrome(options=chrome_options)

navegador.get('https://www.estantevirtual.com.br/')

"""### 3. Navegando até a página de livros mais vendidos do dia"""

#Clicando na página de livros mais vendidos
navegador.find_element(By.XPATH, '//*[@id="ev-header"]/div[3]/div/nav/ul[2]/li[3]/a').click()

#Clicando em mais vendidos de hoje
navegador.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div[4]/ul/li[4]').click()

#Aceitando os cookies
navegador.find_element(By.XPATH, '//*[@id="cmp-button"]').click()

#Clicando em "carregar mais livros" até o fim da página

#for i in range(6):
#    navegador.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div[5]/div/div[2]/div[2]/button').click()

for i in range(5):
    navegador.find_element(By.CSS_SELECTOR, '#__layout > div > div > div.content-mais-vendidos > div > div.box-livros-mais-vendidos > div.gradient-mask > button').click()

"""### 4. Coletando e armazenando os dados em listas"""

#Criando listas vazias

lista_posicao = []
lista_titulo = []
lista_autor = []
lista_preco = []
lista_dt = []

#Criando um laço para coletar todos os livros da página

for i in range(1,101):
    posicao = navegador.find_element(By.XPATH,f'//*[@id="__layout"]/div/div/div[5]/div/div[2]/div/div[{i}]/div[1]/div[1]/span').text
    lista_posicao.append(posicao)

    titulo = navegador.find_element(By.XPATH,f'//*[@id="__layout"]/div/div/div[5]/div/div[2]/div[1]/div[{i}]/div[2]/a[2]/span[1]/h2').text
    lista_titulo.append(titulo)

    autor = navegador.find_element(By.XPATH,f'//*[@id="__layout"]/div/div/div[5]/div/div[2]/div[1]/div[{i}]/div[2]/a[2]/span[1]/h3').text
    lista_autor.append(autor)

    preco = navegador.find_element(By.XPATH,f'//*[@id="__layout"]/div/div/div[5]/div/div[2]/div[1]/div[{i}]/div[2]/a[2]/span[2]/b').text
    lista_preco.append(preco)

    dt = datetime.now()
    lista_dt.append(dt)

"""### 5. Criando e armazenando os dados em um df"""

df_existente = pd.read_csv('../0_bases_originais/ev_mais_vendidos.csv', sep=';')
df_existente['dt'] = pd.to_datetime(df_existente['dt'], errors='coerce')
df_existente

df = pd.DataFrame(lista_posicao, columns=['posicao'])

df['titulo'] = lista_titulo
df['autor'] = lista_autor
df['preco'] = lista_preco
df['dt'] = lista_dt
df

df_consolidado = pd.concat([df_existente,df], ignore_index=True)
df_consolidado

#Tratando coluna preco
df_consolidado['preco'] = df_consolidado['preco'].str.replace('R$ ', '').str.replace(',', '.').astype(float)

#Tratando coluna dt
df_consolidado['dt'] = pd.to_datetime(df_consolidado['dt'])
df_consolidado['dt'] = df_consolidado['dt'].dt.date
df_consolidado

df_consolidado.shape

"""### 6. Salvando o df em csv, json e banco de dados"""

#Salvando em um arquivo csv
df_consolidado.to_csv('../0_bases_originais/ev_mais_vendidos.csv', sep=';', index=False, encoding='UTF-8')

#Salvando em um arquivo json
df_consolidado.to_json('../0_bases_originais/ev_mais_vendidos.json')

engine = db.create_engine('sqlite:///banco_ev.db', echo=True)
conn = engine.connect()
df_consolidado.to_sql('ev_mais_vendidos', con=conn, if_exists='replace')

# Lendo dados adicionais

metadados = pd.read_csv('../0_bases_originais/metadados.csv', sep=';')
metadados.to_sql('metadados', con=conn, if_exists='replace')
metadados.shape

# Ler dados de uma tabela em um DataFrame
df_join = pd.merge(df_consolidado, metadados, on='titulo', how='left')

df_join['posicao'] = df_join['posicao'].astype(int)

# Descartar a coluna 'autor_y'
df_join = df_join.drop(columns=['autor_y'])

# Renomear a coluna 'autor_x' para 'autor'
df_join = df_join.rename(columns={'autor_x': 'autor'})

# Exibir o DataFrame resultante
df_join

df_join.to_sql('consolidado', con=conn, if_exists='replace')

df_join.to_csv('../1_bases_tratadas/consolidado.csv', sep=';', index=False, encoding='UTF-8')

"""### 7. Fechando o navegador"""

navegador.quit()

