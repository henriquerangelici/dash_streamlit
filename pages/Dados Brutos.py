import streamlit as st
import pandas as pd
import requests
import time 
@st.cache_data
def convert_csv(df):
    return df.to_csv(index = False).encode('utf-8')

def mensagem_sucesso():
    sucesso = st.success('Arquivo baixado com sucesso', icon = "👍")
    time.sleep(5)
    sucesso.empty()

st.title('DADOS BRUTOS')
url = 'https://labdados.com/produtos'

response = requests.get(url)
#json é tipo um dicionário para o pandas
dados = pd.DataFrame.from_dict(response.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d/%m/%Y')

with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas', list(dados.columns), list(dados.columns))

st.sidebar.title('Filtros')
with st.sidebar.expander('Nome do produto'):
    produtos = st.multiselect('Selecione os produtos', dados['Produto'].unique(), dados['Produto'].unique())
with st.sidebar.expander('Preço do produto'):
    preco = st.slider('Selecione o preço', 0, 5000, (0,5000))
with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input('Selecione a data', (dados['Data da Compra'].min(),dados['Data da Compra'].max()))
with st.sidebar.expander('Categoria do produto'):
    categoria = st.multiselect('Selecione as categorias', dados['Categoria do Produto'].unique(), dados['Categoria do Produto'].unique())

# query = '''
# (@produtos == [] or Produto in @produtos) and \
# @preco[0] <= Preço <= @preco[1] and \
# @data_compra[0] <= `Data da Compra` <= @data_compra[1] and \
# `Categoria do Produto` in @categoria
# '''
query_filters = []

if produtos:
    query_filters.append("Produto in @produtos")
if preco:
    query_filters.append("@preco[0] <= Preço <= @preco[1]")
if data_compra:
    query_filters.append("@data_compra[0] <= `Data da Compra` <= @data_compra[1]")
if categoria:
    query_filters.append("`Categoria do Produto` in @categoria")

## se não tem nada selecionado, não entrará na variável query, logo, não irá interferir no filtro
query = " and ".join(query_filters)

dados_filtrados = dados.query(query)
dados_filtrados = dados_filtrados[colunas]

st.dataframe(dados_filtrados)
st.markdown(f'Tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]}] colunas')

st.markdown('Escreva um nome para o arquivo')
coluna1, coluna2 = st.columns(2)

with coluna1:
    nome_arquivo = st.text_input('', label_visibility = 'collapsed', value = 'dados')
    nome_arquivo += '.csv'

with coluna2:
    st.download_button('Fazer download',
                       data = convert_csv(dados_filtrados),
                       file_name = nome_arquivo,
                       mime = 'text/csv',
                       on_click = mensagem_sucesso 
                       )


