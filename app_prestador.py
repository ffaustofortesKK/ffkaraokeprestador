import streamlit as st
from supabase import create_client

# Configuração
url = st.secrets["URL_SUPABASE"]
key = st.secrets["KEY_SUPABASE"]
supabase = create_client(url, key)

st.set_page_config(page_title="Painel FF Karaoke", layout="centered")

if "prestador" not in st.session_state:
    st.session_state["prestador"] = None

if st.session_state["prestador"] is None:
    st.title("🎤 Portal do Prestador")
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
            supabase.table("prestadores").insert(dados).execute()
            st.session_state["prestador"] = {"nome": nome}
            st.rerun()
        except Exception as e:
            st.session_state["prestador"] = {"nome": nome}
            st.rerun()

else:
    # CORREÇÃO: Usar .from_("prestadores") para garantir que a tabela seja localizada no schema public
    try:
        nome_usuario = st.session_state["prestador"]["nome"]
        
        # A forma mais robusta de chamar a tabela no Supabase-py
        res = supabase.table("prestadores").select("*").eq("nome_prestador", nome_usuario).execute()
        
        if res.data:
            p = res.data[0]
            status = p['status_acesso']
            
            st.markdown(f"## 🎤 Bem-vindo, {p['nome_prestador']}")
            
            limite = 4 if status == 'pendente' else None
            
            if status == 'pendente':
                st.warning("⚠️ MODO DEMONSTRAÇÃO: Apenas 4 músicas disponíveis.")
            else:
                st.success("✅ ACESSO COMPLETO LIBERADO")

            # Interface de inserção
            nome_cantor = st.text_input("Nome do Cantor:")
            musica = st.text_input("Nome da Música:")
            
            if st.button("★ ADICIONAR À LISTA LOCAL"):
                # Validação importante: garantir que id_prestador exista
                supabase.table("pedidos_pendentes").insert({
                    "id_prestador": p['id'],
                    "nome_cantor": nome_cantor,
                    "musica": musica
                }).execute()
                st.success("Música adicionada!")
                st.rerun()

            st.subheader("FILA DE REPRODUÇÃO ATUAL:")
            query = supabase.table("pedidos_pendentes").select("*").eq("id_prestador", p['id'])
            if limite:
                query = query.limit(limite)
            
            pedidos = query.execute().data
            for i, item in enumerate(pedidos):
                st.write(f"{i+1}. {item.get('musica', 'Sem nome')}")

        else:
            st.error("Usuário não encontrado. Saindo...")
            if st.button("Sair"):
                st.session_state["prestador"] = None
                st.rerun()

    except Exception as e:
        st.error(f"Erro na conexão com Banco de Dados: {e}")
        st.write("Verifique se a tabela 'prestadores' existe no schema 'public'.")
