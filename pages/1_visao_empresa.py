#Importando bibliotecas
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

#bibliotecas necessárias
import pandas as pd
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title='Visão Empresa', layout='wide')

#========================
# Funções
#========================
def country_maps(df1):
    df_aux = df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index()
        
    map = folium.Map()

    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'], location_info['Delivery_location_longitude']]).add_to(map)
    
    folium_static(map, width= 1024, height=600)


#----------------------------------------
def order_share_by_week(df1):
        
    df_aux01 = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    df_aux02 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()
    
    df_aux = pd.merge(df_aux01, df_aux02, how='inner')
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']

    fig = px.line(df_aux, x='week_of_year', y='order_by_deliver')
            
    return fig

#----------------------------------------
def order_by_week (df1):        

    cols = ['ID', 'week_of_year']

    df_aux = df1.loc[:, cols].groupby('week_of_year').count().reset_index()

    fig = px.line(df_aux, x='week_of_year', y='ID')
        
    return fig

#----------------------------------------
def traffic_order_city(df1):
    df_aux = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
                
    fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City') #size é o tamanho e color é a cor
                
    return fig

#----------------------------------------
def traffic_order_share(df1):
    ## 3. Distribuição dos pedidos por tipo de tráfego
    df_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]

    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum() # transforma o número das entregas por densidade demografica  em porcentagem

    fig = px.pie(df_aux, values='entregas_perc', names='Road_traffic_density') # plota a pizza (sem eixo)
    return  fig



def order_metric(df1):
    cols = ['ID',  'Order_Date'] # seleção de colunas
            
    # seleção de linhas
    df_aux = df1.loc[:, cols].groupby('Order_Date').count().reset_index()

    # desenhar gráfico de linhas
    # Plotly
    
    fig = px.bar(df_aux, x='Order_Date', y='ID')
            
    return fig


def clean_code(df1):

    """ Esta função tem a responsabilidade  de limpar o dataframe
    
    Tipos de limpeza:
    1. Remoção dos dados NaN
    2. Mudança do tipo de colunas de dados
    3. Retirada de espaços vazios das variáveis
    4. Criação de coluna week_of_year para análise
    5. Formatação da coluna de datas
    
    Input: Dataframe
    Output: Dataframe
    """

    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :]

    linhas_selecionadas = (df1['City'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :]

    linhas_selecionadas = (df1['Festival'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :]

    linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :]

    linhas_selecionadas = (df1['Weatherconditions'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :]

    linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :]

    ## Removendo os espaços das strings

    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

    ## Convertendo as colunas para o formato correto

    # Conversao de texto/categoria/string para numeros inteiros


    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )

    # Conversao de texto/categoria/strings para numeros decimais
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )

    # Conversao de texto para data
    df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format='%d-%m-%Y' )

    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )

    # Limpando a coluna de time taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min)') [1]) 
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)
    
    # criando week of year
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    
    return df1

#=====================Início da Estrutura Lógica do Código==================================
# Importando Dataset
#=====================
df = pd.read_csv('train.csv')

#=====================
# Limpando os dados
#=====================
df1 = clean_code(df)



#===============================
# BARRA LATERAL
#===============================
st.header('Market Place - Visão Cliente')


image_path = 'logo.jpg'
image= Image.open(image_path)
st.sidebar.image(image, width=312) #tamanho escolhido

st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""") #cria a faixa fina

st.sidebar.markdown('## Selecione uma data limte')

date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=pd.datetime(2022, 4, 13),
    min_value=pd.datetime(2022, 2, 11),
    max_value=pd.datetime(2022, 4, 6),
    format='DD-MM-YYY')


st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito?',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown("""---""")

# Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]


#===============================
# Layout no streamlit
#===============================

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        #Order Metric
        st.markdown('# Orders By Day')
        fig = order_metric(df1)
        st.plotly_chart(fig, use_container_width=True)
        
        
            
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            fig = traffic_order_share(df1)
            st.header('Traffic Order Share')
            st.plotly_chart(fig, use_container_width=True)
            
            
                
        
        with col2:
            st.header('Traffic Order City')
            fig = traffic_order_city(df1)
            st.plotly_chart(fig, use_container_width=True)
            
            
                
    
with tab2:
    with st.container():
        st.markdown('# Order By Week')
        fig = order_by_week(df1)
        st.plotly_chart(fig, use_container_width=True)
        
    with st.container():
        st.markdown('# Order Share By Week')
        fig = order_share_by_week(df1)
        st.plotly_chart(fig, use_container_width=True)
        
        
            
        
    
with tab3:
    st.markdown('# Country Maps')
    country_maps(df1)
    
    
    
    
    
    









