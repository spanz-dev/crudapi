import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Quando fizermos o deploy, alteramos a variável no ambiente. Localmente usa o localhost.
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="CRUD Itens", layout="centered")
st.title("📦 Gestão de Stock - Dashboard CRUD")

# --- Painel de Operações ---
st.subheader("Adicionar / Modificar Item")
with st.form("form_item", clear_on_submit=True):
    id_item = st.number_input("ID do Item (Necessário apenas para Atualizar/Apagar)", min_value=0, step=1, value=0)
    nome = st.text_input("Nome do Produto")
    preco = st.number_input("Preço Unitário", min_value=0.0, format="%.2f")
    descricao = st.text_area("Descrição do Produto")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        btn_criar = st.form_submit_button("Criar Registo")
    with col2:
        btn_atualizar = st.form_submit_button("Atualizar Registo")
    with col3:
        btn_deletar = st.form_submit_button("Apagar Registo", type="primary")

# Lógica das Ações do CRUD consumindo a API FastAPI
if btn_criar:
    payload = {"nome": nome, "preco": preco, "descricao": descricao}
    res = requests.post(f"{API_URL}/items/", json=payload)
    if res.status_code == 200:
        st.success("Item adicionado com sucesso!")
    else:
        st.error("Erro ao adicionar item.")

if btn_atualizar and id_item > 0:
    payload = {"nome": nome, "preco": preco, "descricao": descricao}
    res = requests.put(f"{API_URL}/items/{id_item}", json=payload)
    if res.status_code == 200:
        st.success(f"Item ID {id_item} atualizado com sucesso!")
    else:
        st.error(f"Não foi possível atualizar o item {id_item}.")

if btn_deletar and id_item > 0:
    res = requests.delete(f"{API_URL}/items/{id_item}")
    if res.status_code == 200:
        st.success(f"Item ID {id_item} removido do banco.")
    else:
        st.error(f"Erro ao tentar remover o item {id_item}.")

# --- Visualização dos Dados ---
st.subheader("📋 Inventário em Tempo Real")
try:
    resposta_get = requests.get(f"{API_URL}/items/")
    if resposta_get.status_code == 200:
        lista_itens = resposta_get.json()
        if lista_itens:
            st.dataframe(lista_itens, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum item localizado no banco de dados.")
except Exception:
    st.error("A API de dados está inacessível no momento.")