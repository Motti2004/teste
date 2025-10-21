import pandas as pd
import os
import folium
from folium.plugins import LocateControl
df = pd.read_excel("Dados_teste.xlsx")
mapa = folium.Map(location=[-23.546761091636284,-46.651802547369144], zoom_start=16)
LocateControl().add_to(mapa)
for _, row in df.iterrows():
    imagens = str(row["imagem"]).split(",")
    imagens_html = "".join([f'<img src="{img.strip()}" width="200"><br>' for img in imagens if img.strip()])
    icone_path = os.path.join(os.path.dirname(__file__),"icone de jequitibá.png")
    icone_personalizado=folium.CustomIcon(icone_path, icon_size=(50,50))

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
            icon=icone_personalizado
        ).add_to(mapa)
mapa.save("Teste_de_árvore.html")

print("Mapa gerado! Abra o arquivo 'Teste_de_árvore.html' no navegador")