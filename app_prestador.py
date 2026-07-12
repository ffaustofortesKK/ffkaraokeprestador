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
        try:
            dados = {
                "nome_prestador": nome,
                "codigo_express": tel,
                "slug_unico": nome.lower().replace(" ", "-"),
                "senha_acesso": "1234",
                "status_acesso": "pendente"
            }
            res = supabase.table("prestadores").insert(dados).execute()
            # Salva o nome para tentar autenticar
            st.session_state["prestador"] = {"nome": nome}
            st.success("Pedido enviado! Aguarde a aprovação do Administrador.")
            st.rerun()
        except:
            st.error("Erro: Este prestador já solicitou acesso ou ocorreu um erro.")

# --- TELA DO PAINEL (VERIFICAÇÃO DE PORTARIA) ---
else:
    # Passo 1: Busca o status real no banco de dados
    nome_usuario = st.session_state["prestador"]["nome"]
    res = supabase.table("prestadores").select("*").eq("nome_prestador", nome_usuario).execute()
    
    if res.data:
        p = res.data[0] # Dados atualizados do prestador
        status = p['status_acesso']
        
        st.markdown(f"## 🎤 Bem-vindo, {p['nome_prestador']}")
        
        # Modo Demonstração vs Modo Completo
        limite = 4 if status == 'pendente' else None
        
        if status == 'pendente':
            st.warning("⚠️ MODO DEMONSTRAÇÃO: Apenas 4 músicas disponíveis. Aguarde a liberação do Admin.")
        else:
            st.success("✅ ACESSO COMPLETO LIBERADO")

        # --- INTERFACE (Conforme sua imagem YYY.png) ---
        nome_cantor = st.text_input("Nome do Cantor:")
        musica = st.text_input("Nome da Música:")
        
        if st.button("★ ADICIONAR À LISTA LOCAL"):
            st.write("Música adicionada à fila!")

        st.subheader("FILA DE REPRODUÇÃO ATUAL:")
        query = supabase.table("pedidos_pendentes").select("*").eq("id_prestador", p['id'])
        if limite:
            query = query.limit(limite) # Aplica o limite se for pendente
        
        pedidos = query.execute().data
        for i, item in enumerate(pedidos):
            st.write(f"{i+1}. {item.get('musica', 'Música sem nome')}")

        st.divider()
        st.write("### SISTEMA EM SINTONIA CLOUD")
        col1, col2 = st.columns(2)
        with col1: st.button("✅ Validar")
        with col2: st.button("🗑️ Recusar")
    else:
        st.error("Prestador não encontrado. Tente logar novamente.")
        if st.button("Sair"):
            st.session_state["prestador"] = None
            st.rerun()
