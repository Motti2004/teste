import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import sqlite3
import os
from database import criar_tabela, inserir_arvore
criar_tabela()
df = pd.read_excel("Dados_teste.xlsx")
st.set_page_config(page_title="Leaf Search")
st.sidebar.header("Menu")
pagina = st.sidebar.radio("Escolha uma página", [
                          "Mapa", "Sobre o projeto", "Árvores cadastradas", "Cadastro de árvore", "Calculo de biomasssa de carbono"])
if pagina == "Mapa":
    st.write("""
# Mapa de árvores da Região do Higienopolis
O site e o mapa estão em fase de teste""")
    st.subheader("Bem vindo ao Leaf Search!")
    st.info("Você poderá visualizar as árvores cadastradas no bairro de Higienópolis.")
    with open("Teste_de_árvore.html", "r", encoding="utf-8") as t:
       Teste_html = t.read()
    components.html(Teste_html, height=600)

elif pagina == "Árvores cadastradas":
    st.subheader("Árvores cadastradas")
    df = pd.read_excel("Dados_teste.xlsx")
    st.dataframe(df)

elif pagina == "Sobre o projeto":
    st.subheader("Sobre o projeto")
    st.info("O projeto tem como objetivo desenvolver um aplicativo com capacidade de informar e mapear as plantas localizadas ao redor da Universidade Presbiteriana Mackenzie. Sendo motivado pelo propósito de trazer conhecimento sobre o meio ambiente e incentivar a participação da população por meio da ciência cidadã. ")
    st.subheader("Regras para cadastrar a sua árvore")
    st.info("- Registro de informações (complete todas as informacões de forma coerente e no devido lugar para não misturar as informações.)")
    st.info("- Altura e Diametro (para fazer a comparação de altura e Diametro é recomendavel utilizar uma régua ou algo para referencia.)")
    st.info("- Fotos (as fotos devem estar de boa resolução e sem estar tremidas ou borradas.)")
    st.info("- Coordenadas (para encontrar as coordenadas é necessario entrar no aplicativo de localização e clicar no local desjado.) ")
    st. info("Passo 1: abra o aplicativo de localização.")
    st.image("Passo 1.jpeg", width=300)
    st.info("Passo 2: selecione a area desejada.")
    st.image("Passo 2.jpeg", width=300)
    st.info("Passo 3: verificar se as coordenadas estão na barra de pesquisa ou estão no icone de marcador localização que esta na aba de baixo do mapa e copie as coordenadas.")
    st.image("Passo 3.jpeg", width=300)


elif pagina == "Cadastro de árvore":
    st.subheader("Cadastre a sua árvore")
    st.info("Aqui você podera cadastrar a sua arvore e manda-la para ser analisada pelo herbario da Universiade Mackenzie de São Paulo.")
    form = st.form(key="árvore", clear_on_submit=True)
    with form:
        input_name = st.text_input("Nome: ", placeholder="Insira seu nome aqui.")
        input_email = st.text_input("Email: ", placeholder="Insira seu email aqui.")
        input_telefone = st.text_input("Telefone: ", placeholder="Insira seu número de telefone aqui.")
        input_altura = st.text_input("Altura", placeholder="Insira a altura estimada da árvores.")
        input_diametro = st.text_input("Diametro", placeholder="Insira a diametro estimada da árvores.")
        foto = st.file_uploader("Envie uma foto da altura e diametro (com alguma referencia para ter uma comparação e medida): ", type=["jpg","png","jpeg"])
        input_caracteristicas = st.text_input("Características", placeholder="Insira as caracteristicas como formatoda folha, cor da flor, como é o fruto e etc.")
        input_coordenadas = st.text_input("Coordenadas", placeholder="Insira as coordenadas da árvore. exemplo: -23.5... e -46.8...")
        foto = st.file_uploader("Envie uma foto da árvore (se apresenta a flor e fruto também mande a foto ): u", type=["jpg","png","jpeg"])
        botão_submit = form.form_submit_button("Confirmar")
        foto_path = None
        if botão_submit:
            if foto is not None:
                os.makedirs("fotos", exist_ok=True)
                foto_path= os.path.join("fotos", foto.name)
                with open (foto_path, "wb") as f:
                    f.write(foto.getbuffer())
            inserir_arvore(input_name, input_email, input_telefone, input_altura, input_diametro, input_caracteristicas, input_coordenadas, foto_path)
            st.success("Árvore cadastrada com sucesso! Enviada para análise para ser marcada no mapa.")

elif pagina == "Calculo de biomasssa de carbono":
    num_1= st.number_input(label="Digite o diametro da árvore", format="%0f")
    num_2= st.number_input(label="Digite a altura da árvore ", format="%0f")
    colunas = st.columns(1)
    with colunas[0]:
        if st.button(label="calcular", use_container_width=True):
            resultado= 0.0334330*(num_1**2.397902)*(num_2**0.426536)
            st.write(f"O resultado de biomassa é: {resultado}")