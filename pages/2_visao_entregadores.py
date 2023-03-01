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

st.set_page_config(page_title='Visão Entregadores', layout='wide')

#========================
# Funções
#========================


def top_delivers(df1, top_asc):
    df3 = df1.loc[:, ['Delivery_person_ID', 'Time_taken(min)', 'City' ]].groupby(['City','Delivery_person_ID']).mean().sort_values(['City','Time_taken(min)'], ascending=top_asc).reset_index()

    df_aux1 = df3.loc[df3['City'] == 'Metropolitian', :].head(10)
    df_aux2 = df3.loc[df3['City'] == 'Urban', :].head(10)
    df_aux3 = df3.loc[df3['City'] == 'Semi-Urban', :].head(10)

    df4 = pd.concat([df_aux1, df_aux2, df_aux3]).reset_index(drop=True)
                
    return df4

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

#==================
# Importing dataset
#==================
df = pd.read_csv('train.csv')

# Cleaning dataset
df1 = clean_code(df)




#===============================
# BARRA LATERAL
#===============================
st.header('Market Place - Visão Entregadores')


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

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '--', '--'])

with tab1:
    with st.container():
        st.title('Overall Metrics')
        
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
            
            # 1. A maior idade dos entregadores
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric('Maior Idade', maior_idade)
                        
        with col2:
            # 2. A menor idade dos entregadores
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Menor Idade', menor_idade)
            
        with col3:
            # 3. A melhor condição de veículo        
            melhor_carro = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric('Melhor Condição de Veículo', melhor_carro)
            
        with col4:
            # 4. A pior condição de veículo 
            pior_carro = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric('Pior Condição de Veículo', pior_carro)
    
    with st.container(): 
        st.markdown("""---""")
        st.title('Avaliações')
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### Avaliações médias por entregador')
            cols = ['Delivery_person_Ratings', 'Delivery_person_ID']
            avaliacao_media = df1.loc[:, cols].groupby('Delivery_person_ID').mean().reset_index()
            
            st.dataframe(avaliacao_media)


            
        with col2:
            st.markdown('##### Avaliação média por trânsito')
            df_avg_rating_by_traffic =( df1.loc[:, ['Delivery_person_Ratings','Road_traffic_density' ]]
                                          .groupby('Road_traffic_density')
                                          .agg({'Delivery_person_Ratings': ['mean', 'std']})) # agregando informações numa única tabela
                    
            df_avg_rating_by_traffic.columns = ['delivery_mean', 'delivery_std'] # renomeando colunas agregadas
            df_avg_rating_by_traffic.reset_index()
            
            st.dataframe(df_avg_rating_by_traffic)
            
            st.markdown('##### Avaliação média por clima')
            cols = ['Delivery_person_Ratings', 'Weatherconditions']

            avaliacao_media_clima = df1.loc[:, cols].groupby('Weatherconditions').mean().reset_index()
            st.dataframe(avaliacao_media_clima)
    
    with st.container():
        st.markdown("""---""")
        st.title('Agilidade de Entrega')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('##### Top entregadores mais rápidos')
            df4 = top_delivers(df1, top_asc=True)
            st.dataframe(df4)
        
            
        with col2:
            st.markdown('##### Top entregadores mais lentos')
            df4 = top_delivers(df1, top_asc=False)
            st.dataframe(df4)
            
            
        