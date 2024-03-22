import streamlit as st
import pandas as pd

# Função para carregar dados dos usuários
def load_usuarios():
    try:
        df = pd.read_excel("Tools.xlsx")  # Substitua "Tools.xlsx" pelo caminho correto do arquivo
    except FileNotFoundError:
        st.error(f"Arquivo 'Tools.xlsx' não encontrado.")
        df = pd.DataFrame(columns=["usuario", "senha"])
    return df

# Função para autenticar usuário
def authenticate(username, password):
    usuarios_df = load_usuarios()
    if usuarios_df is None:
        return False

    user_data = usuarios_df[usuarios_df['usuario'] == username]
    if not user_data.empty:
        stored_password = user_data.iloc[0]['senha']
        if str(stored_password) == str(password):
            return True
    return False

def main():
    st.title("🔒")

    if 'logged_in_tools' not in st.session_state:
        st.session_state['logged_in_tools'] = False

    if not st.session_state['logged_in_tools']:
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            if authenticate(username, password):
                st.session_state['logged_in_tools'] = True
                st.success("Autenticação bem-sucedida!")
            else:
                st.error("Usuário ou senha incorretos. Tente novamente.")
        return

    # Exibe o restante da página apenas se o usuário estiver autenticado corretamente
    file_options = ['teladecadastro.xlsx', 'usuarios.xlsx', 'usuariosinfracoes.xlsx']
    selected_file = st.selectbox("Selecione um arquivo", file_options)

    if selected_file:
        df = pd.read_excel(selected_file)

        st.write("### Dados do arquivo selecionado:")
        st.write(df)

        st.sidebar.subheader("Opções:")
        column_to_delete = st.sidebar.selectbox("Selecione a coluna para excluir", df.columns)
        entry_to_delete = st.sidebar.text_input(f"{column_to_delete} do Cadastro para Excluir")
        if st.sidebar.button("Excluir Cadastro"):
            df = delete_entry(df, column_to_delete, entry_to_delete)
            st.success("Cadastro excluído com sucesso!")

            # Salva as alterações no arquivo Excel
            df.to_excel(selected_file, index=False)

            # Atualiza o DataFrame lido do arquivo Excel
            df = pd.read_excel(selected_file)

        st.write("### Dados Após Exclusão:")
        st.write(df)

def delete_entry(df, column_to_delete, entry_to_delete):
    if entry_to_delete:
        df = df[df[column_to_delete] != entry_to_delete]
    return df

if __name__ == "__main__":
    main()
