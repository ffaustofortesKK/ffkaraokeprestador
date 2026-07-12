import streamlit as st
import qrcode
from io import BytesIO
from supabase import create_client

# Configuração
url = st.secrets["URL_SUPABASE"]
key = st.secrets["KEY_SUPABASE"]
supabase = create_client(url, key)

st.set_page_config(page_title="Painel do Prestador", layout="centered")
st.title("🎤 Portal do Prestador")

if "prestador_id" not in st.session_state:
    st.session_state["prestador_id"] = None

if st.session_state["prestador_id"] is None:
    st.subheader("Login de Acesso")
    nome = st.text_input("Nome de Usuário:")
    senha = st.text_input("Senha:", type="password")
    
    if st.button("Entrar"):
        try:
            # Consulta na tabela 'prestadores'
            res = supabase.table("prestadores").select("*").eq("nome_prestador", nome).eq("senha_acesso", senha).execute()
            
            if res.data and len(res.data) > 0:
                prestador = res.data[0]
                
                # Verificação de status
                if prestador.get("status_acesso") == "ativo":
                    st.session_state["prestador_id"] = prestador["id"]
                    st.session_state["nome"] = prestador["nome_prestador"]
                    st.session_state["slug"] = prestador["slug_unico"]
                    st.rerun()
                elif prestador.get("status_acesso") == "pendente":
                    st.warning("Seu acesso ainda está em análise pelo administrador.")
                else:
                    st.error("Acesso bloqueado.")
            else:
                st.error("Credenciais inválidas!")
                
        except Exception as e:
            st.error(f"Erro no banco de dados: {str(e)}")
            st.info("Verifique se a tabela 'prestadores' foi criada no painel do Supabase.")
else:
    st.success(f"Olá, {st.session_state['nome']}!")
    url_cliente = f"https://ffkaraoke-cliente.streamlit.app/?prestador={st.session_state['slug']}"
    st.info(f"Seu link: {url_cliente}")
    
    qr = qrcode.make(url_cliente)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    st.image(buf.getvalue(), caption="QR Code do Prestador")
    
    if st.button("Sair"):
        st.session_state["prestador_id"] = None
        st.rerun()
