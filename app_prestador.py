import streamlit as st
from supabase import create_client

# Configuração
url = st.secrets["URL_SUPABASE"]
key = st.secrets["KEY_SUPABASE"]
supabase = create_client(url, key)

st.set_page_config(page_title="Portal FF Karaoke", layout="wide")

# Inicialização de sessão
if "prestador" not in st.session_state:
    st.session_state["prestador"] = None

# --- TELA DE REGISTRO E DEMONSTRAÇÃO ---
if st.session_state["prestador"] is None:
    st.title("🎤 Portal FF Karaoke - Teste Grátis")
    st.write("Cadastre-se para solicitar acesso completo.")
    
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome de Usuário:")
        tel = st.text_input("TEL:")
        if st.button("SOLICITAR ACESSO COMPLETO"):
            # Lógica de inserção no banco
            dados = {"nome_prestador": nome, "codigo_express": tel, "status_acesso": "pendente", "senha_acesso": "1234", "slug_unico": nome.lower()}
            supabase.table("prestadores").insert(dados).execute()
            st.session_state["prestador"] = {"status": "pendente", "nome": nome}
            st.rerun()

    # DEMONSTRAÇÃO (Sempre visível para quem não logou)
    st.subheader("Modo Demonstração (4 Músicas)")
    demo_musicas = ["Música Demo 1", "Música Demo 2", "Música Demo 3", "Música Demo 4"]
    for m in demo_musicas:
        st.write(f"▶️ {m}")

# --- TELA DO PAINEL (APÓS CADASTRO) ---
else:
    p = st.session_state["prestador"]
    st.title(f"Bem-vindo, {p['nome']}!")
    
    if p['status'] == "pendente":
        st.warning("⚠️ Você está no modo demonstração. Solicite a liberação ao Admin para ter acesso total.")
        # Exibe apenas as 4 músicas demo
    else:
        st.success("✅ Acesso Total Liberado!")
        # Exibe a lista completa de músicas
