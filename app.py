import streamlit as st
import pandas as pd

st.title("Agente Inteligente de Reposição")

estoque_file = st.file_uploader("📦 Estoque atual (CSV)", type="csv")
vendas_file = st.file_uploader("📈 Histórico de vendas (CSV)", type="csv")

if estoque_file and vendas_file:
    df_estoque = pd.read_csv(estoque_file)
    df_vendas = pd.read_csv(vendas_file)

    demanda = df_vendas.groupby("SKU")["quantidade"].mean()
    df_estoque["demanda_diaria"] = df_estoque["SKU"].map(demanda)

    prazo_reposicao = 45  # dias
    df_estoque["repor"] = (df_estoque["demanda_diaria"] * prazo_reposicao) - df_estoque["estoque_atual"]
    df_estoque["repor"] = df_estoque["repor"].clip(lower=0).round()

    st.subheader("📋 Produtos para Reposição")
    st.dataframe(df_estoque[df_estoque["repor"] > 0][["SKU", "repor"]])

    csv = df_estoque.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Baixar planilha de reposição", csv, file_name="reposicao.csv", mime="text/csv")
