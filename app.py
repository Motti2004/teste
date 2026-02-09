import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from supabase import create_client, Client

supabase_url=("https://qrqzmiodksobvufaqmdx.supabase.co")
supabase_key=("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFycXptaW9ka3NvYnZ1ZmFxbWR4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk0MzM2OTQsImV4cCI6MjA3NTAwOTY5NH0.MXWNzHQizABV0_5vS1bp__R1ozlF48G-uvQzZ9X-yOI")

supabase: Client = create_client(supabase_url, supabase_key)

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
        input_altura = st.text_input("Altura(m)", placeholder="Exemplo: 9, 3.5, 1.80, etc..")
        input_diametro = st.text_input("Diametro(cm)", placeholder="Exemplo: 10, 40, 80, etc. .")
        input_caracteristicas = st.text_input("Características", placeholder="Ex: formato da folha, cor da flor, como é o fruto e etc.")
        input_coordenadas = st.text_input("Coordenadas", placeholder="Exemplo: -23.5... e -46.8...")

        foto = st.file_uploader(
            "Envie uma foto da árvore (altura, diametro, folha, flor, fruto e árvore):",
            type=["jpg", "png", "jpeg"]
        )

        botão_submit = form.form_submit_button("Confirmar")

    if botão_submit:
        foto_url = None

        if foto is not None:
            try:
                bucket_name = "Fotos das arvores"  
                file_name = f"{input_name.strip()}_{foto.name.strip()}"

                supabase.storage.from_(bucket_name).upload(
                    file_name,
                    foto.getvalue(),
                    file_options={"content-type": foto.type}
                    )


                foto_url = supabase.storage.from_(bucket_name).get_public_url(file_name)

            except Exception as e:
                st.error(f"Erro ao enviar imagem para o Supabase Storage: {e}")

        data = {
            "nome": input_name,
            "email": input_email,
            "telefone": input_telefone,
            "altura": input_altura,
            "diametro": input_diametro,
            "caracteristicas": input_caracteristicas,
            "coordenadas": input_coordenadas,
            "foto": foto_url
        }

        try:
            response = supabase.from_("arvores_cadastradas").insert(data).execute()
            st.success("Árvore cadastrada com sucesso! Enviada para análise e marcada no mapa.")
            st.write("Retorno do Supabase:", response)

        except Exception as e:
            st.error(f"Erro ao cadastrar árvore: {e}")

elif pagina == "Calculo de biomasssa de carbono":
    num_1 = st.number_input(label="Digite o diametro da árvore", format="%0f")
    num_2 = st.number_input(label="Digite a altura da árvore", format="%0f")

    if st.button(label="calcular", use_container_width=True):
        resultado = 0.0334330 * (num_1 ** 2.397902) * (num_2 ** 0.426536)
        st.write(f"O resultado de biomassa é: {resultado}")
