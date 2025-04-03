import streamlit as st
import pandas as pd
from db.database import get_db
from db.crud import get_all_items, add_item, update_item, delete_item
from utils.nomes_bonitos import nomes_bonitos

# ✨ Função auxiliar para normalizar nomes
def normalizar_nome(nome: str) -> str:
    return nome.strip().upper()

# Inicia sessão com o banco
db = next(get_db())

# Carrega os dados do banco apenas se ainda não estiver em cache
if "df_raw" not in st.session_state:
    st.session_state.df_raw = get_all_items(db)

if "checked_itens" not in st.session_state:
    st.session_state.checked_itens = set()

# Abas principais
aba1, aba2, aba3 = st.tabs(["✅ Checklist", "🛠 Adicionar/Editar/Remover", "📊 Visualização Final"])

with aba1:
    st.title("📦 Checklist da Mudança")

    for i, row in st.session_state.df_raw.iterrows():
        nome_caps = row['objeto']
        nome_bonito = nomes_bonitos.get(nome_caps, nome_caps.title())
        key = f"check_{i}_{nome_caps}"

        checked = st.checkbox(
            f"{row['quantidade']}x {nome_bonito}",
            key=key,
            value=nome_caps in st.session_state.checked_itens
        )

        if checked:
            st.session_state.checked_itens.add(nome_caps)
        else:
            st.session_state.checked_itens.discard(nome_caps)

    st.markdown("---")
    st.success(f"{len(st.session_state.checked_itens)} de {len(st.session_state.df_raw)} itens marcados como armazenados.")

    if st.button("🔄 Limpar todos os checks"):
        st.session_state.checked_itens.clear()
        st.rerun()

with aba2:
    st.title("🛠 Adicionar, Editar ou Remover Itens")

    opcoes = ["Adicionar", "Editar", "Remover"]
    operacao = st.selectbox("O que você deseja fazer?", opcoes)

    todos_itens = list(st.session_state.df_raw['objeto'].dropna().unique())

    if operacao == "Adicionar":
        novo_nome = st.text_input("Digite o nome do novo item (em letras maiúsculas):", "")
        nova_qtd = st.number_input("Quantidade", min_value=1, value=1, step=1)
        nova_desc = st.text_input("Descrição (opcional):", "")
        valor_str = st.text_input("Valor (opcional) (somente números inteiros):")
        novo_valor = int(valor_str) if valor_str.strip().isdigit() else None

        if st.button("Salvar Novo Item"):
            if not novo_nome.strip():
                st.warning("⚠️ O nome do item não pode estar vazio.")
            else:
                novo_item = {
                    'objeto': normalizar_nome(novo_nome),
                    'quantidade': nova_qtd,
                    'descricao': nova_desc or None,
                    'valor': novo_valor
                }
                add_item(db, novo_item)
                st.success("Item adicionado com sucesso!")
                st.session_state.df_raw = get_all_items(db)
                st.rerun()

    elif operacao == "Editar":
        item_selecionado = st.selectbox("Selecione o item que deseja editar", todos_itens)
        item_data = st.session_state.df_raw[st.session_state.df_raw['objeto'] == item_selecionado]

        qtd_atual = int(item_data['quantidade'].values[0])
        desc_atual = item_data['descricao'].values[0] or ""
        valor_atual = item_data['valor'].values[0]
        valor_str = str(int(valor_atual)) if pd.notna(valor_atual) else ""

        nova_qtd = st.number_input("Nova quantidade", min_value=1, value=qtd_atual, step=1)
        nova_desc_input = st.text_input("Nova descrição (opcional):", desc_atual)
        nova_desc = nova_desc_input.strip() or None
        novo_valor_str = st.text_input("Novo valor (opcional):", valor_str)
        novo_valor = int(novo_valor_str) if novo_valor_str.strip().isdigit() else None

        if st.button("Salvar Alteração"):
            novos_dados = {
                "quantidade": nova_qtd,
                "descricao": nova_desc,
                "valor": novo_valor
            }
            update_item(db, item_selecionado, novos_dados)
            st.success("Item atualizado com sucesso!")
            st.session_state.df_raw = get_all_items(db)
            st.rerun()

    elif operacao == "Remover":
        item_selecionado = st.selectbox("Selecione o item que deseja remover", todos_itens)

        if st.button("Remover Item"):
            delete_item(db, item_selecionado)
            st.success("Item removido com sucesso!")
            st.session_state.df_raw = get_all_items(db)
            st.rerun()

with aba3:
    st.title("📊 Visualização Final")
    st.dataframe(st.session_state.df_raw, use_container_width=True)
