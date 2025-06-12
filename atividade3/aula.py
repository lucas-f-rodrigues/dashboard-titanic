import streamlit as st
import pandas as pd
import plotly.express as px

# Função para carregar os dados com cache
@st.cache_data
def load_data():
    return pd.read_csv('titanic3.csv', sep=";")

# Carregar dados
df = load_data()

# Filtros da barra lateral
st.sidebar.title("Filtros")

sexos_disponiveis = df['sex'].dropna().unique()
classes_disponiveis = sorted(df['pclass'].dropna().unique())
opcoes_sobrevivencia = [0, 1]

sexo_selecionado = st.sidebar.multiselect("Sexo", options=sexos_disponiveis, default=sexos_disponiveis)
classe_selecionada = st.sidebar.multiselect("Classe (pclass)", options=classes_disponiveis, default=classes_disponiveis)
sobrevivencia_selecionada = st.sidebar.multiselect("Sobrevivência", options=opcoes_sobrevivencia, default=opcoes_sobrevivencia)

# Aplicar filtros
df_filtrado = df[
    df['sex'].isin(sexo_selecionado) &
    df['pclass'].isin(classe_selecionada) &
    df['survived'].isin(sobrevivencia_selecionada)
]

# Título
st.title("Quem Sobreviveu no Titanic?")
st.subheader("1. Visão Geral dos Dados")

# Número de passageiros filtrados
st.write(f"Número total de passageiros: {df_filtrado.shape[0]}")

# Taxa de sobrevivência
taxa_sobrevivencia = (
    df_filtrado['survived']
    .value_counts(normalize=True)
    .rename({0: 'Não Sobreviveu', 1: 'Sobreviveu'})
)
st.write("Taxa de sobrevivência:")
st.write(taxa_sobrevivencia.map(lambda x: f"{x:.1%}"))

# Dados ausentes
st.subheader("2. Dados Ausentes")
dados_ausentes = df_filtrado.isnull().sum()
percentual_ausente = (dados_ausentes / df_filtrado.shape[0]) * 100
tabela_ausencia = pd.DataFrame({'Total': dados_ausentes, 'Percentual': percentual_ausente})
st.dataframe(tabela_ausencia[tabela_ausencia['Total'] > 0])

# Análises Visuais
st.subheader("3. Análises Visuais")

# Gráfico: Sobrevivência por Sexo
st.write("Sobrevivência por Sexo")
fig_sexo = px.histogram(
    df_filtrado, x='sex', color='survived', barmode='group',
    category_orders={"survived": [0, 1]},
    labels={'survived': 'Sobreviveu'}
)
st.plotly_chart(fig_sexo)

# Gráfico: Sobrevivência por Classe
st.write("Sobrevivência por Classe (pclass)")
fig_classe = px.histogram(
    df_filtrado, x='pclass', color='survived', barmode='group',
    category_orders={"pclass": [1, 2, 3]},
    labels={'survived': 'Sobreviveu'}
)
st.plotly_chart(fig_classe)

# Gráfico: Sobrevivência por Sexo e Classe
st.write("Sobrevivência por Sexo e Classe")
fig_sexo_classe = px.histogram(
    df_filtrado, x='sex', color='survived', barmode='group',
    facet_col='pclass',
    category_orders={"pclass": [1, 2, 3]},
    labels={'survived': 'Sobreviveu'}
)
st.plotly_chart(fig_sexo_classe)
