import streamlit as st
from supabase import create_client

# Configuração de Conexão (Usa as mesmas chaves do seu Admin)
url = st.secrets["URL_SUPABASE"]
key = st.secrets["KEY_SUPABASE"]
supabase = create_client(url, key)

st.set_page_config(page_title="F.F Karaoke - Pedido", page_icon="🎤")

st.title("🎤 F.F KARAOKE")
st.subheader("Faça o seu pedido")

# Formulário de entrada
with st.form("pedido_form", clear_on_submit=True):
    nome = st.text_input("Seu Nome:")
    musica = st.text_input("Nome da Música:")
    
    # Botão de envio
    if st.form_submit_button("Enviar Pedido"):
        if nome and musica:
            # Envia para a tabela 'pedidos_pendentes' que o Admin vai ler
            supabase.table("pedidos_pendentes").insert({
                "cantor": nome, 
                "musica": musica, 
                "status": "pendente"
            }).execute()
            st.success(f"Pedido de {nome} enviado com sucesso! Aguarde sua vez.")
        else:
            st.error("Por favor, preencha o seu nome e a música.")

# Rodapé simples
st.markdown("---")
st.write("Sistema de Karaoke F.F - Gestão Eficiente")
