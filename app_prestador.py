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

# Inicializar sessão de login
if "prestador_id" not in st.session_state:
    st.session_state["prestador_id"] = None

if st.session_state["prestador_id"] is None:
    st.subheader("Login de Acesso")
    nome = st.text_input("Nome de Usuário:")
    senha = st.text_input("Senha:", type="password")
    
    if st.button("Entrar"):
        try:
            # Consulta no banco
            res = supabase.table("prestadores").select("*").eq("nome_prestador", nome).eq("senha_acesso", senha).execute()
            
            if res.data:
                # ... (resto do seu código de sucesso) ...
                prestador = res.data[0]
                # ...
            else:
                st.error("Credenciais inválidas ou prestador não encontrado.")
                
        except Exception as e:
            st.error(f"Erro no banco de dados: {str(e)}")
            st.write("Verifique se o nome da tabela e das colunas estão exatamente iguais aos que estão no Supabase.")
        
        if res.data:
            prestador = res.data[0]
            
            # Verificação de status de acesso
            if prestador.get("status_acesso") == "ativo":
                st.session_state["prestador_id"] = prestador["id"]
                st.session_state["nome"] = prestador["nome_prestador"]
                st.session_state["slug"] = prestador["slug_unico"]
                st.rerun()
            elif prestador.get("status_acesso") == "pendente":
                st.warning("Seu acesso ainda está em análise pelo administrador. Por favor, aguarde a confirmação do pagamento.")
            else:
                st.error("Acesso bloqueado. Contacte o suporte.")
        else:
            st.error("Credenciais inválidas!")
else:
    st.success(f"Olá, {st.session_state['nome']}!")
    
    # Gerar link do prestador
    url_cliente = f"https://ffkaraoke-cliente.streamlit.app/?prestador={st.session_state['slug']}"
    
    st.info(f"Seu link de pedidos: {url_cliente}")
    
    # Gerar QR Code
    qr = qrcode.make(url_cliente)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    st.image(buf.getvalue(), caption="Imprima este QR Code para seus clientes")
    
    if st.button("Sair"):
        st.session_state["prestador_id"] = None
        st.rerun()
