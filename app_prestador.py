import streamlit as st
from supabase import create_client

# Configuração (Use suas chaves nos Secrets do Streamlit)
url = st.secrets["URL_SUPABASE"]
key = st.secrets["KEY_SUPABASE"]
supabase = create_client(url, key)

st.set_page_config(page_title="Portal do Prestador", layout="centered")
st.title("🎤 Portal do Prestador")
st.subheader("Login de Acesso")

# Campos conforme sua imagem
nome = st.text_input("Nome de Usuário:")
tel = st.text_input("TEL:")

if st.button("SOLICITAR PEDIDO"):
    if nome and tel:
        try:
            # Cria o prestador com status 'pendente'
            # O campo slug_unico é gerado automaticamente baseado no nome
            dados = {
                "nome_prestador": nome,
                "codigo_express": tel,
                "slug_unico": nome.lower().replace(" ", "-"),
                "senha_acesso": "1234", # Senha padrão inicial
                "status_acesso": "pendente"
            }
            
            supabase.table("prestadores").insert(dados).execute()
            st.success("Pedido enviado! Aguarde a liberação do administrador.")
            
        except Exception as e:
            st.error("Erro ao enviar pedido. Verifique se este nome já foi solicitado.")
    else:
        st.warning("Por favor, preencha todos os campos.")
