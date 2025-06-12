import pandas as pd
import streamlit as st
import plotly.express as px

# Carregar os nossos datasets
df_titanic = pd.read_csv("titanic3.csv", sep=";")

total_pasageiros = len(df_titanic)
print(total_pasageiros)

porcentagem_sobreviventes = (df_titanic["survived"] == 1).sum() * 100 / total_pasageiros
porcentagem_nao_sobreviventes = (df_titanic["survived"] == 0).sum() * 100 / total_pasageiros

df_nulos = df_titanic.count() * 100 / total_pasageiros

taxa_sobrevivencia_F = ((df_titanic["survived"] == 1) & (df_titanic["sex"] == "female")).sum() * 100 / len(df_titanic[df_titanic["sex"] == "female"])
print(taxa_sobrevivencia_F)