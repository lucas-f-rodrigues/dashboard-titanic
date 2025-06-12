import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados
@st.cache_data
def carregar_dados():
    dados = pd.read_csv('titanic.csv', sep=';')
    return dados

dados = carregar_dados()

st.title("🚢 Dashboard - Titanic")

# Filtros
filtro_sexo = st.selectbox("Filtrar por sexo:", options=['Todos', 'male', 'female'])
filtro_classe = st.multiselect(
    "Filtrar por classe:",
    options=sorted(dados['pclass'].dropna().unique()),
    default=sorted(dados['pclass'].dropna().unique())
)

dados_filtrados = dados.copy()

if filtro_sexo != 'Todos':
    dados_filtrados = dados_filtrados[dados_filtrados['sex'] == filtro_sexo]

if filtro_classe:
    dados_filtrados = dados_filtrados[dados_filtrados['pclass'].isin(filtro_classe)]

# Informações gerais
st.subheader("📊 Informações Gerais")

coluna1, coluna2, coluna3, coluna4 = st.columns(4)

coluna1.metric("Total de passageiros", len(dados_filtrados))

dados_filtrados = dados_filtrados.copy()
dados_filtrados['age'] = pd.to_numeric(dados_filtrados['age'], errors='coerce')

# Calcular a média 
media_idade = dados_filtrados['age'].mean()
coluna2.metric("Média de idade", f"{media_idade:.2f}" if not pd.isna(media_idade) else "N/A")

coluna3.metric("Homens", len(dados_filtrados[dados_filtrados['sex'] == 'male']))
coluna4.metric("Mulheres", len(dados_filtrados[dados_filtrados['sex'] == 'female']))

# Gráfico de pizza
st.subheader("🧍‍♂️🧍‍♀️ Proporção por sexo")

contagem_sexo = dados_filtrados['sex'].value_counts()
figura1, eixo1 = plt.subplots()
eixo1.pie(contagem_sexo, labels=contagem_sexo.index, autopct='%1.1f%%', startangle=90)
eixo1.axis('equal')
st.pyplot(figura1)

# Gráfico de barras
st.subheader("🎟️ Passageiros por classe")

contagem_classe = dados_filtrados['pclass'].value_counts().sort_index()
figura2, eixo2 = plt.subplots()
eixo2.bar(contagem_classe.index.astype(str), contagem_classe.values, color='skyblue')
eixo2.set_xlabel("Classe")
eixo2.set_ylabel("Quantidade")
eixo2.set_title("Total de passageiros por classe")
st.pyplot(figura2)
