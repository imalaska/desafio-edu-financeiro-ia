import json
import pandas as pd
import requests
import streamlit as st

# ============ CONFIGURAÇÃO ============
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3" 

# ============ CARREGAR DADOS ============
try:
    perfil = json.load(open('data/perfil_investidor.json', encoding='utf-8'))
    transacoes = pd.read_csv('data/transacoes.csv')
    historico = pd.read_csv('data/historico_atendimento.csv')
    produtos = json.load(open('data/produtos_financeiros.json', encoding='utf-8'))
except FileNotFoundError:
    st.error("Erro: Arquivos de dados não encontrados.")
    st.stop()

# ============ CONTEXTO ============
contexto = f"""
DADOS DO CLIENTE:
Nome: {perfil['nome']} | Idade: {perfil['idade']} | Perfil: {perfil['perfil_investidor']}
Objetivo: {perfil['objetivo_principal']}
Patrimônio: R$ {perfil['patrimonio_total']} | Reserva: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

PRODUTOS (PARA EXEMPLO):
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

SYSTEM_PROMPT = f"""
Você é o Edu, Educador Financeiro.
1. Ensine conceitos financeiros usando os dados do cliente.
2. NUNCA recomende compra de ativos específicos.
3. Responda em no máximo 3 parágrafos curtos.
CONTEXTO:
{contexto}
"""

def perguntar_ollama(msg):
    try:
        data = {"model": MODELO, "prompt": f"{SYSTEM_PROMPT}\nUSER: {msg}", "stream": False}
        r = requests.post(OLLAMA_URL, json=data)
        if r.status_code == 200: return r.json()['response']
        return f"Erro Ollama: {r.status_code}"
    except: return "Erro: Verifique se o Ollama está rodando."

st.title("🎓 Edu - Finanças IA")
if prompt := st.chat_input("Dúvida financeira?"):
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            st.write(perguntar_ollama(prompt))
