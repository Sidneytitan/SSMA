import streamlit as st
import pandas as pd

# Função para carregar os usuários do arquivo Excel
def load_users(filename):
    try:
        df = pd.read_excel(filename)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar os usuários: {e}")
        return None

# Função para verificar o login
def login(username, password, users_df):
    if users_df is not None:
        if username in users_df["usuario"].values:
            user_row = users_df[users_df["usuario"] == username]
            if user_row["senha"].iloc[0] == password:
                return True
    return False

# Função para salvar os usuários no arquivo Excel
def save_users(df, filename):
    try:
        df.to_excel(filename, index=False)
    except Exception as e:
        st.error(f"Erro ao salvar os usuários: {e}")

def app():
    st.title("Login")

    # Carregar os usuários existentes
    users_df = load_users("teladecadastro.xlsx")

    # Exibir formulário de login
    username = st.text_input("Nome de usuário")
    password = st.text_input("Senha", type="password")

    # Verificar o login quando o botão for pressionado
    if st.button("Login"):
        if login(username, password, users_df):
            st.success("Login bem-sucedido!")
            # Se o login for bem-sucedido, exibir a página de cadastro de usuários
            show_user_registration_page()
        else:
            st.error("Credenciais inválidas. Por favor, tente novamente.")

def show_user_registration_page():
    st.title("Cadastro de Usuários")

    # Definir rótulos personalizados para os arquivos Excel
    planilhas = {
        "usuarios.xlsx": "Acesso de Ocorrência",
        "usuariosinfracoes.xlsx": "Acesso Infrações"
    }

    # Selecionar a planilha para cadastro
    planilha_selecionada = st.selectbox("Selecione a planilha para cadastro:", list(planilhas.values()))

    # Mapear o rótulo selecionado para o nome real do arquivo Excel
    planilha = [key for key, value in planilhas.items() if value == planilha_selecionada][0]

    # Carregar os usuários existentes ou criar um DataFrame vazio
    users_df = load_users(planilha)
    if users_df is None:
        users_df = pd.DataFrame(columns=["usuario", "senha"])

    # Campos de entrada para nome de usuário e senha
    new_username = st.text_input("Novo Usuário")
    new_password = st.text_input("Nova Senha", type="password")

    # Botão para cadastrar novo usuário
    if st.button("Cadastrar"):
        if new_username.strip() == "" or new_password.strip() == "":
            st.error("Por favor, insira um nome de usuário e senha válidos.")
        elif "usuario" in users_df.columns and new_username in users_df["usuario"].values:
            st.error("Este nome de usuário já existe. Por favor, escolha outro.")
        else:
            # Adicionar novo usuário ao DataFrame
            new_user = pd.DataFrame({"usuario": [new_username], "senha": [new_password]})
            users_df = pd.concat([users_df, new_user], ignore_index=True)
            # Salvar os usuários atualizados
            save_users(users_df, planilha)
            st.success("Novo usuário cadastrado com sucesso!")

if __name__ == "__main__":
    app()
