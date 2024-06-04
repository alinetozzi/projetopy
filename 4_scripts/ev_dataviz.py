# Importando as bibliotecas

import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# Estabelecendo conexão com banco de dados SQLite

conn = sqlite3.connect('banco_ev.db')
df = pd.read_sql_query('SELECT * FROM consolidado', con=conn)

# Configurando a largura da página

st.set_page_config(layout="wide")

# Configurando o logo da página

logo = 'logo_book_trend.png'
st.logo(logo,link=None, icon_image=None)

# Configurando cabeçalho da página

st.markdown('<h1 style="color:#7ED957;">Book Trends </h1>', unsafe_allow_html=True)
st.subheader('O _Book Trends_ é uma aplicação que coleta dados dos 100 livros mais vendidos do dia na Estante Virtual.')
st.markdown(' ')

# Configurando o número de colunas para os filtros da página

f1, f2, f3 = st.columns(3)

# Definindo as variáveis com o valor filtrado

f_data = f1.selectbox('Data de coleta', df['dt'].drop_duplicates(), index=1)
f_gen = f2.selectbox('Gênero do(a) autor(a)', df['genero'].drop_duplicates(), index=None)
f_nac = f3.selectbox('Nacionalidade do(a) autor(a)', df['nacionalidade_autor'].drop_duplicates(), index=None)

st.divider()

# Filtrando os dados do DF

df_filtrado = df[df['dt']==f_data]

if f_gen != None:
    df_filtrado = df_filtrado[df_filtrado['genero']==f_gen]

if f_nac != None:
    df_filtrado = df_filtrado[df_filtrado['nacionalidade_autor']==f_nac]

# Inserindo cards de resumo

col1, col2, col3 = st.columns(3)

col1.metric(label="Preço de venda por livro", value=round(df_filtrado['preco'].mean(),2))
col2.metric(label="Média de páginas por livro", value=round(df_filtrado['paginas'].mean(),0))
col3.metric(label="Total de gêneros", value=df_filtrado['ano_publicacao'].drop_duplicates().count())
col1.metric(label="Total de autores", value=df_filtrado['autor'].drop_duplicates().count())
col2.metric(label="Total de nacionalidades", value=df_filtrado['nacionalidade_autor'].drop_duplicates().count())
col3.metric(label="Ano de publicação mais recente", value=df_filtrado['ano_publicacao'].max())

st.divider()

# Inserindo tabela com o Top 5

st.subheader('Lista com os 5 livros mais comprados')
filtro_colunas = ['posicao','titulo','autor','preco','nacionalidade_autor','genero','paginas','ano_publicacao'] 
top5 = df_filtrado[df_filtrado['posicao']<6]
top5 = top5[filtro_colunas]
top5_rename = {'titulo': 'Título',
                       'autor': 'Autor', 
                       'preco': 'Preço',
                       'nacionalidade_autor':'Nacionalidade do autor',
                       'genero':'Gênero',
                       'paginas':'Páginas',
                       'ano_publicacao':'Ano de publicação'}
top5_renomeado = top5.rename(columns=top5_rename)
st.dataframe(top5,hide_index=True)

st.divider()

# Preferências por nacionalidade do autor

st.subheader('Preferências por nacionalidade do autor')
fig1, fig2 = st.columns(2)

# Gráfico 1
posicao_nacionalidade = df_filtrado.groupby('nacionalidade_autor')['posicao'].mean().reset_index()
posicao_nacionalidade = posicao_nacionalidade.sort_values(by='posicao', ascending=True)

with fig1:
    fig1_chart = px.bar(posicao_nacionalidade, x='nacionalidade_autor', y='posicao',title='Posição média por nacionalidade do autor')
    st.plotly_chart(fig1_chart)

# Gráfico 2
count_nac = df_filtrado['nacionalidade_autor'].value_counts().reset_index()
count_nac.columns = ['nacionalidade_autor', 'count']

with fig2:
    fig2_chart = px.pie(count_nac,values='count', names='nacionalidade_autor', title='Quantidade de livros por nacionalidade do autor')
    st.plotly_chart(fig2_chart)

st.divider()

# Preferências por gênero da obra

st.subheader('Preferências por gênero da obra')
fig1, fig2 = st.columns(2)

# Gráfico 1
posicao_genero = df_filtrado.groupby('genero')['posicao'].mean().reset_index()
posicao_genero = posicao_genero.sort_values(by='posicao', ascending=True)

with fig1:
    fig1_chart = px.bar(posicao_genero, x='genero', y='posicao',title='Posição média por gênero da obra')
    st.plotly_chart(fig1_chart)

# Gráfico 2
count_gen = df_filtrado['genero'].value_counts().reset_index()
count_gen.columns = ['genero', 'count']

with fig2:
    fig2_chart = px.pie(count_gen,values='count', names='genero', title='Quantidade de livros por gênero da obra')
    st.plotly_chart(fig2_chart)

st.divider()

# Gráficos de distribuição de preço

st.subheader('Distribuição de preço')

col1, col2 = st.columns(2)

# Gráfico 1
with col1:
    fig1 = px.histogram(df_filtrado, x='preco')
    st.plotly_chart(fig1)

# Gráfico 2
with col2:
    fig2 = px.box(df_filtrado, y='preco')
    st.plotly_chart(fig2)

st.divider()

# Gráficos de distribuição de preço

st.subheader('Preço médio por nacionalidade, gênero, número de páginas e ano de publicação')
fig1, fig2 = st.columns(2)

# Preço médio por nacionalidade do autor
preco_nacionalidade = df_filtrado.groupby('nacionalidade_autor')['preco'].mean().reset_index()
preco_nacionalidade = preco_nacionalidade.sort_values(by='preco', ascending=False)

with fig1:
    fig1_chart = px.bar(preco_nacionalidade, x='nacionalidade_autor', y='preco',title='Preço médio por nacionalidade do autor')
    st.plotly_chart(fig1_chart)

# Preço médio por gênero da obra
preco_genero = df_filtrado.groupby('genero')['preco'].mean().reset_index()
preco_genero = preco_genero.sort_values(by='preco', ascending=False)

with fig2:
    fig2_chart = px.bar(preco_genero, x='genero', y='preco',title='Preço médio por gênero da obra')
    st.plotly_chart(fig2_chart)

# Preço médio por número de páginas do livro
preco_paginas = df_filtrado.groupby('paginas')['preco'].mean().reset_index()
preco_paginas = preco_paginas.sort_values(by='preco', ascending=False)

with fig1:
    fig3_chart = px.histogram(preco_paginas, x='paginas', y='preco',title='Preço médio por número de páginas do livro')
    st.plotly_chart(fig3_chart)

# Preço médio por ano de publicação
preco_ano = df_filtrado.groupby('ano_publicacao')['preco'].mean().reset_index()
preco_ano = preco_ano.sort_values(by='preco', ascending=False)

with fig2:
    fig4_chart = px.histogram(preco_ano, x='ano_publicacao', y='preco',title='Preço médio por ano de publicação')
    st.plotly_chart(fig4_chart)
