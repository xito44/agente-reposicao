import streamlit as st
import requests
import pandas as pd

def consultar_estoque(api_key):
    url = "https://bling.com.br/Api/v3/estoques/saldos"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()['data']
        df_estoque = pd.json_normalize(data)
        df_estoque = df_estoque[['produto.codigo', 'saldo']]
        df_estoque.columns = ['SKU', 'estoque_atual']
        return df_estoque
    else:
        st.error(f"Erro ao consultar o Bling: {response.status_code}")
        return pd.DataFrame()
