import unicodedata
 
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import folium
from folium.plugins import LocateControl
from supabase import create_client, Client
 
 
supabase_url = "https://qrqzmiodksobvufaqmdx.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFycXptaW9ka3NvYnZ1ZmFxbWR4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk0MzM2OTQsImV4cCI6MjA3NTAwOTY5NH0.MXWNzHQizABV0_5vS1bp__R1ozlF48G-uvQzZ9X-yOI"
supabase: Client = create_client(supabase_url, supabase_key)
 
 
components.html("""
<script>
  var link = window.parent.document.querySelector("link[rel='manifest']");
  if (!link) {
    link = window.parent.document.createElement('link');
    link.rel = 'manifest';
    window.parent.document.head.appendChild(link);
  }
  link.href = 'https://raw.githubusercontent.com/Motti2004/teste/main/manifest.json';
</script>
""", height=0, width=0)
 
 
def remover_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFKD', str(texto))
        if not unicodedata.combining(c)
    )
 
 
def filtrar_dataframe(df, busca):
    """Filtra qualquer coluna do DataFrame que contenha o termo buscado,
    ignorando maiúsculas/minúsculas e acentos."""
    if not busca:
        return df
    busca_normalizada = remover_acentos(busca).lower()
    mask = df.apply(
        lambda row: row.astype(str).apply(
            lambda x: busca_normalizada in remover_acentos(x).lower()
        ).any(),
        axis=1
    )
    return df[mask]
 
 
st.set_page_config(page_title="Leaf Search")
st.sidebar.header("Menu")
pagina = st.sidebar.radio("Escolha uma página", [
    "Mapa",
    "Sobre o projeto",
    "Árvores cadastradas",
    "Cadastro de árvore",
    "Calculo de biomasssa de carbono",
])
 
 
if pagina == "Mapa":
    st.write("""
# Mapa de árvores da Região do Higienopolis
O site e o mapa estão em fase de teste""")
    st.subheader("Bem vindo ao Leaf Search!")
    st.info("Você poderá visualizar as árvores cadastradas no bairro de Higienópolis.")
 
    busca = st.text_input("🔍 Buscar árvore (nome, gênero, família...)")
 
    df_mapa = pd.read_excel("Dados_teste.xlsx")
    df_filtrado = filtrar_dataframe(df_mapa, busca)
 
    if busca and df_filtrado.empty:
        st.warning("Nenhuma árvore encontrada com esse termo.")
    elif busca:
        st.caption(f"{len(df_filtrado)} árvore(s) encontrada(s).")
    else:
        st.caption(
            f"Mostrando todas as {len(df_filtrado)} árvores cadastradas.")
 
    figura = folium.Figure(height="1400px")
    mapa = folium.Map(
        location=[-23.546761091636284, -46.651802547369144], zoom_start=16
    ).add_to(figura)
    LocateControl(showPopup=False).add_to(mapa)
 
    # ---- Caixinha de coordenadas em tempo real ----
    nome_do_mapa = mapa.get_name()
 
    caixa_html = """
    <div id="coord-display" style="
        position:absolute; top:10px; left:60px; z-index:9999;
        background:white; padding:12px 20px; border-radius:10px;
        box-shadow:0 2px 6px rgba(0,0,0,0.4); font-family:sans-serif; font-size:20px; font-weight:bold;">
        📍 Localização: aguardando...
    </div>
    """
    mapa.get_root().html.add_child(folium.Element(caixa_html))
 
    script_coordenadas = f"""
    {nome_do_mapa}.on('locationfound', function(e) {{
        var texto_coordenadas = "📍 " + e.latlng.lat.toFixed(6) + ", " + e.latlng.lng.toFixed(6);
 
        document.getElementById('coord-display').innerHTML =
            "📍 Localização: " + e.latlng.lat.toFixed(6) + ", " + e.latlng.lng.toFixed(6);
 
        L.popup()
            .setLatLng(e.latlng)
            .setContent(texto_coordenadas)
            .openOn({nome_do_mapa});
    }});
    """
    mapa.get_root().script.add_child(folium.Element(script_coordenadas))
    # ---- Fim da caixinha de coordenadas ----
 
    for _, row in df_filtrado.iterrows():
        imagens = str(row["imagem"]).split(",")
        imagens_html = "".join(
            f'<img src="{img.strip()}" width="200"><br>' for img in imagens if img.strip()
        )
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=(f"<b>{row['id']}</b><br>"
                   f"<b>{row['vernacular']}</b><br>"
                   f"<b>{row['genus']}</b><br>"
                   f"<b>{row['family']}</b><br>"
                   f"<b>{row['notes']}</b><br>"
                   f"<b>{row['altura']}</b><br>"
                   f"<b>{row['diametro']}</b><br>"
                   f'<a href="{row["link"]}" target="_blank">Abrir ficha</a><br>'
                   f'{imagens_html}'),
            icon=folium.CustomIcon(
                "marcador de arvore.png", icon_size=(28, 28)),
        ).add_to(mapa)
 
    components.html(figura._repr_html_(), height=1400)
 
 
elif pagina == "Árvores cadastradas":
    st.subheader("Árvores cadastradas")
    df_lista = pd.read_excel("Dados_teste.xlsx")
    st.dataframe(df_lista)
 
 
elif pagina == "Sobre o projeto":
    st.subheader("Sobre o projeto")
    st.info(
        "O projeto tem como objetivo desenvolver um aplicativo com capacidade de "
        "informar e mapear as plantas localizadas ao redor da Universidade "
        "Presbiteriana Mackenzie. Sendo motivado pelo propósito de trazer "
        "conhecimento sobre o meio ambiente e incentivar a participação da "
        "população por meio da ciência cidadã."
    )
    st.subheader("Regras para cadastrar a sua árvore")
    st.info("- Registro de informações (complete todas as informações de forma coerente "
            "e no devido lugar para não misturar as informações.)")
    st.info("- Altura e Diâmetro (para fazer a comparação de altura e diâmetro é "
            "recomendável utilizar uma régua ou algo como referência.)")
    st.info("- Fotos (as fotos devem estar em boa resolução e sem estar tremidas ou borradas.)")
    st.info("- Coordenadas (para encontrar as coordenadas é necessário entrar no "
            "aplicativo de localização e clicar no local desejado.)")
 
    st.info("Passo 1: abra o aplicativo de localização.")
    st.image("Passo 1.jpeg", width=300)
    st.info("Passo 2: selecione a área desejada.")
    st.image("Passo 2.jpeg", width=300)
    st.info("Passo 3: verifique se as coordenadas estão na barra de pesquisa ou no ícone "
            "de marcador de localização na aba de baixo do mapa, e copie as coordenadas.")
    st.image("Passo 3.jpeg", width=300)
 
 
elif pagina == "Cadastro de árvore":
    st.subheader("Cadastre a sua árvore")
    st.info(
        "Aqui você poderá cadastrar a sua árvore e enviá-la para ser analisada "
        "pelo herbário da Universidade Mackenzie de São Paulo."
    )
 
    with st.form(key="árvore", clear_on_submit=True) as form:
        input_name = st.text_input(
            "Nome: ", placeholder="Insira seu nome aqui.")
        input_email = st.text_input(
            "Email: ", placeholder="Insira seu email aqui.")
        input_telefone = st.text_input(
            "Telefone: ", placeholder="Insira seu número de telefone aqui.")
        input_altura = st.text_input(
            "Altura(m)", placeholder="Exemplo: 9, 3.5, 1.80, etc.")
        input_diametro = st.text_input(
            "Diâmetro(cm)", placeholder="Exemplo: 10, 40, 80, etc.")
        input_caracteristicas = st.text_input(
            "Características", placeholder="Ex: formato da folha, cor da flor, como é o fruto etc."
        )
        input_coordenadas = st.text_input(
            "Coordenadas", placeholder="Exemplo: -23.5... e -46.8...")
 
        foto = st.file_uploader(
            "Envie uma foto da árvore (altura, diâmetro, folha, flor, fruto e árvore):",
            type=["jpg", "png", "jpeg"],
        )
 
        botao_submit = st.form_submit_button("Confirmar")
 
    if botao_submit:
        foto_url = None
 
        if foto is not None:
            try:
                bucket_name = "Fotos das arvores"
                file_name = f"{input_name.strip()}_{foto.name.strip()}"
 
                supabase.storage.from_(bucket_name).upload(
                    file_name,
                    foto.getvalue(),
                    file_options={"content-type": foto.type},
                )
                foto_url = supabase.storage.from_(
                    bucket_name).get_public_url(file_name)
 
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
            "foto": foto_url,
        }
 
        try:
            response = supabase.from_(
                "arvores_cadastradas").insert(data).execute()
            st.success(
                "Árvore cadastrada com sucesso! Enviada para análise e marcada no mapa.")
            st.write("Retorno do Supabase:", response)
        except Exception as e:
            st.error(f"Erro ao cadastrar árvore: {e}")
 
 
elif pagina == "Calculo de biomasssa de carbono":
    num_1 = st.number_input(
        label="Digite o diâmetro da árvore em centimetros(cm)", format="%0f")
    num_2 = st.number_input(
        label="Digite a altura da árvore em metros(m)", format="%0f")
 
    if st.button(label="Calcular", use_container_width=True):
        resultado = 0.0334330 * (num_1 ** 2.397902) * (num_2 ** 0.426536)
        st.write(f"O resultado de biomassa é: {resultado:.2f}kg")
