import streamlit as st
from supabase import create_client

# Configuração
url = st.secrets["URL_SUPABASE"]
key = st.secrets["KEY_SUPABASE"]
supabase = create_client(url, key)

st.set_page_config(page_title="Painel FF Karaoke", layout="centered")

# --- Lógica de Inicialização ---
if "prestador" not in st.session_state:
    st.session_state["prestador"] = None

# --- TELA DE CADASTRO / LOGIN ---
if st.session_state["prestador"] is None:
    st.title("🎤 Portal do Prestador")
    st.subheader("Solicite seu acesso")
    
    nome = st.text_input("Nome de Usuário:")
    tel = st.text_input("TEL (Código Express):")
    
    if st.button("SOLICITAR PEDIDO"):
        dados = {
            "nome_prestador": nome,
            "codigo_express": tel,
            "slug_unico": nome.lower().replace(" ", "-"),
            "senha_acesso": "1234",
            "status_acesso": "pendente"
        }
        try:
            supabase.table("prestadores").insert(dados).execute()
            st.success("Pedido enviado! Aguarde a aprovação.")
        except:
            st.error("Erro: Prestador já cadastrado.")

# --- TELA DO PAINEL (CONFORME SUA IMAGEM) ---
else:
    p = st.session_state["prestador"]
    st.markdown("## 🎤 FILA DE REPRODUÇÃO - GRUPO FF KARAOKE")
    
    # Lógica de limite de músicas
    limite = 4 if p['status'] == 'pendente' else None
    
    # Campo de Entrada (conforme imagem)
    nome_cantor = st.text_input("Nome do Cantor:")
    musica = st.text_input("Nome da Música (Pesquisa automática):")
    
    if st.button("★ ADICIONAR À LISTA LOCAL"):
        # Aqui você insere na tabela de pedidos com id_prestador
        st.write("Música adicionada!")

    # Exibição da Fila
    st.subheader("FILA DE REPRODUÇÃO ATUAL:")
    query = supabase.table("pedidos_pendentes").select("*").eq("id_prestador", p['id'])
    if limite:
        query = query.limit(limite)
    pedidos = query.execute().data
    
    for i, item in enumerate(pedidos):
        st.write(f"{i+1}. {item.get('musica')}")

    # Painel de Controle (Validar/Recusar)
    st.divider()
    st.write("### SISTEMA EM SINTONIA CLOUD")
    col1, col2 = st.columns(2)
    with col1: st.button("✅ Validar")
    with col2: st.button("🗑️ Recusar")

    if p['status'] == 'pendente':
        st.warning("⚠️ MODO DEMONSTRAÇÃO: Apenas 4 músicas exibidas. Entre em contato para liberação total.")
