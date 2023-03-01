import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
)


#image_path = 'C:/Users/muril/Documents/Repos/ftc/dataset/'
image = Image.open('logo.jpg')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""") #cria a faixa fina

st.write("# Curry Company Growth Dashboaard")
st.markdown(
   """ 
        Growth Dashboard foi construído para acompanhar as métricas de crescimento dos entregadores e restaurantes.
        ### Como utilizar o growth dashboard?
    - Visao empresa:
        - Visão gerencial: Métricas gerais de comportamento.
        - Visão tática: Indicadores semanais de crescimento.
        - Visao Geográfica: Insights de geolocalização.
    - Visão entregador: 
        - Acompanhamento dos indicadores semanais de crescimento
    - Visão restaturante: 
        - Indicadores semanais de crescimento dos restaurantes
     #### Ask for help
        - Time datascience no discord
        - @muriloperalta
   """)

