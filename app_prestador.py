import streamlit as st
from supabase import create_client

# Configuração (Use a Service Role Key que começa com ey...)
url = st.secrets["URL_SUPABASE"]
key = st.secrets["KEY_SUPABASE"]
supabase = create_client(url, key)

st.set_page_config(page_title="Painel FF Karaoke", layout="centered")

# --- Lógica de Inicialização ---
if "prestador" not in st.session_state:
    st.session_state["prestador"] = None

# --- TELA DE LOGIN/CADASTRO ---
if st.session_state["prestador"] is None:
    st.title("🎤 Portal do Prestador")
    st.subheader("Solicite seu acesso")
    
    nome = st.text_input("Nome de Usuário:")
    tel = st.text_input("TEL (Código Express):")
    
    if st.button("SOLICITAR PEDIDO"):
        slug = nome.lower().replace(" ", "-")
        dados = {
            "nome_prestador": nome,
            "codigo_express": tel,
            "slug_unico": slug,
            "senha_acesso": "1234",
            "status_acesso": "pendente"
        }
        try:
            # Upsert garante que se o usuário já existir, ele não trava o banco
            supabase.table("prestadores").upsert(dados, on_conflict="slug_unico").execute()
            st.session_state["prestador"] = {"slug": slug}
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao solicitar: {e}")

# --- TELA DO PAINEL ---
else:
    try:
        slug_usuario = st.session_state["prestador"]["slug"]
        
        # Busca pelo slug (mais seguro)
        res = supabase.table("prestadores").select("*").eq("slug_unico", slug_usuario).execute()
        
        if res.data:
            p = res.data[0]
            status = p['status_acesso']
            
            st.markdown(f"## 🎤 Bem-vindo, {p['nome_prestador']}")
            
            # Controle de Acesso (Modo Demo)
            limite = 4 if status == 'pendente' else None
            
            if status == 'pendente':
                st.warning("⚠️ MODO DEMONSTRAÇÃO: Apenas 4 músicas disponíveis. Aguarde a liberação do Admin.")
            else:
                st.success("✅ ACESSO COMPLETO LIBERADO")

            # Inputs do Painel
            nome_cantor = st.text_input("Nome do Cantor:")
            musica = st.text_input("Nome da Música:")
            
            if st.button("★ ADICIONAR À LISTA LOCAL"):
                if musica:
                    supabase.table("pedidos_pendentes").insert({
                        "id_prestador": p['id'],
                        "nome_cantor": nome_cantor,
                        "musica": musica
                    }).execute()
                    st.rerun()

            # Exibição da Fila
            st.subheader("FILA DE REPRODUÇÃO ATUAL:")
            query = supabase.table("pedidos_pendentes").select("*").eq("id_prestador", p['id'])
            if limite:
                query = query.limit(limite)
            
            pedidos = query.execute().data
            for i, item in enumerate(pedidos):
                st.write(f"{i+1}. {item.get('musica', 'Sem nome')}")

            st.divider()
            if st.button("Sair"):
                st.session_state["prestador"] = None
                st.rerun()
        else:
            st.error("Erro ao carregar dados do perfil.")
            
    except Exception as e:
        st.error(f"Erro de Conexão: {e}")
