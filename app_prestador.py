import streamlit as st
import qrcode
from io import BytesIO
from supabase import create_client

# Configuração
url = st.secrets["URL_SUPABASE"]
key = st.secrets["KEY_SUPABASE"]
supabase = create_client(url, key)

st.set_page_config(page_title="Grupo FF Karaoke", layout="centered")

# --- ESTILIZAÇÃO DO CABEÇALHO ---
st.markdown("<h1 style='text-align: center;'>🎤 GRUPO FF KARAOKE</h1>", unsafe_allow_html=True)

# Inicializar sessão
if "prestador" not in st.session_state:
    st.session_state["prestador"] = None

# --- LÓGICA DE LOGIN/REGISTRO ---
if st.session_state["prestador"] is None:
    tab1, tab2 = st.tabs(["Acesso Prestador", "Solicitar Cadastro"])
    
    with tab1:
        st.subheader("Login de Acesso")
        nome_login = st.text_input("Nome de Usuário:")
        senha_login = st.text_input("Senha:", type="password")
        if st.button("ENTRAR"):
            res = supabase.table("prestadores").select("*").eq("nome_prestador", nome_login).eq("senha_acesso", senha_login).execute()
            if res.data:
                p = res.data[0]
                if p["status_acesso"] == "ativo":
                    st.session_state["prestador"] = p
                    st.rerun()
                else:
                    st.warning("Aguardando aprovação do Admin.")
            else:
                st.error("Credenciais inválidas.")

    with tab2:
        st.subheader("Solicitar Novo Cadastro")
        nome_reg = st.text_input("Nome do Cantor:")
        tel_reg = st.text_input("Seu Telefone/Código:")
        if st.button("SOLICITAR PEDIDO"):
            dados = {
                "nome_prestador": nome_reg,
                "codigo_express": tel_reg,
                "slug_unico": nome_reg.lower().replace(" ", "-"),
                "senha_acesso": "1234",
                "status_acesso": "pendente"
            }
            supabase.table("prestadores").insert(dados).execute()
            st.success("Pedido enviado! Aguarde nossa liberação.")

# --- PAINEL DO PRESTADOR (APÓS LOGIN) ---
else:
    p = st.session_state["prestador"]
    st.success(f"Bem-vindo, {p['nome_prestador']}!")
    
    # UI do Painel (baseado na sua imagem)
    st.text_input("Nome do Cantor:")
    st.text_input("Nome da Música (Pesquisa automática):")
    st.button("★ ADICIONAR À LISTA LOCAL", use_container_width=True)
    
    st.subheader("FILA DE REPRODUÇÃO ATUAL:")
    st.container(height=150) # Área da fila
    
    col1, col2, col3 = st.columns(3)
    col1.button("↑ Subir")
    col2.button("↓ Descer")
    col3.button("🗑️ Remover")
    
    st.button("▶ ANUNCIAR PRÓXIMO CANTOR", use_container_width=True)
    
    # Área Cloud
    st.subheader("SISTEMA EM SINTONIA CLOUD")
    st.container(height=100)
    st.button("✅ Validar")
    
    if st.button("Sair"):
        st.session_state["prestador"] = None
        st.rerun()
