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
import numpy as np

st.set_page_config(page_title='Visão Restaurantes', layout='wide')
#========================
# Funções
#========================
def avg_std_time_on_traffic(df1):
        
    cols = ['City', 'Time_taken(min)','Road_traffic_density']
    df_aux = df1.loc[:, cols].groupby(['City','Road_traffic_density']).agg({'Time_taken(min)': ['mean','std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    
    fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time',
                              color='std_time', color_continuous_scale='RdBu',
                              color_continuous_midpoint=np.average(df_aux['std_time']))
                
    return fig

def avg_std_time_graph(df1):
            
    cols = ['City', 'Time_taken(min)']
    df_aux = df1.loc[:, cols].groupby(['City']).agg({'Time_taken(min)': ['mean','std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar( name='Control',
                                 x=df_aux['City'],
                                 y=df_aux['avg_time'],
                                 error_y=dict( type='data', array=df_aux['std_time'])))
    fig.update_layout(barmode='group')
                
    return fig


def avg_std_time_delivery(df1, festival, op):
    """ Esta função calcula o tempo médio e o desvio padrão para o tempo de entrega.
                    Parâmetros:
                        Input:
                        - df: dataframe com os dados necessários para o cálculo
                        - op: tipo de operação que precisa ser calculado
                            'avg_time': calcula o tempo médio
                            'std_time': calcula o desvio padrão do tempo
                        Output:
                        - df: dataframe com duas colunas e uma linha
    """            
    cols = ['Festival', 'Time_taken(min)']
    df_aux = df1.loc[:, cols].groupby(['Festival']).agg({'Time_taken(min)': ['mean','std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    df_aux = np.round(df_aux.loc[df_aux['Festival'] == festival, op],2)
                
    return df_aux


def distance(df1, fig):
    if fig == False:
        cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude' ]
        df1['distance'] = df1.loc[:, cols].apply(lambda x: haversine ( (x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
            
        avg_distance = np.round(df1['distance'].mean(), 2)  
        return avg_distance
    
    else:
        cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude' ]
        df1['distance'] = df1.loc[:, cols].apply(lambda x: haversine ( (x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
            
        
        avg_distance = df1.loc[:,['City', 'distance']].groupby('City').mean().reset_index()
        fig = go.Figure(data=[ go.Pie( labels=avg_distance['City'], values=avg_distance['distance'], pull=[0, 0.1, 0])])

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

#==================
# Importing dataset
#==================
df = pd.read_csv('train.csv')


# Cleaning dataset
df1 = clean_code(df)


#===============================
# BARRA LATERAL
#===============================
st.header('Market Place - Visão Restaurantes')


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
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            delivery_unique = df1.loc[:, 'Delivery_person_ID'].nunique()
            col1.metric('Entregadores únicos', delivery_unique)
            
        with col2:
            avg_distance = distance(df1, fig=False)
            col2.metric('Média de distânca', avg_distance)
            
            
        with col3:
            df_aux = avg_std_time_delivery(df1, 'Yes', 'avg_time')
            col3.metric('Tempo médio de entrega', df_aux)
            
        with col4:
            df_aux = avg_std_time_delivery(df1, 'Yes', 'std_time')
            col4.metric('Desvio Padrão Médio', df_aux)
            
        with col5:
            df_aux = avg_std_time_delivery(df1, 'No', 'avg_time')
            col5.metric('Tempo médio de entrega c/ Festival', df_aux)
                    
        with col6:
            df_aux = avg_std_time_delivery(df1, 'No', 'std_time')
            col6.metric('Desvio padrão média de entrega', df_aux)
                        
        
    with st.container():
        st.markdown("""---""")
        col1, col2 = st. columns(2)
        
        with col1:
            fig = avg_std_time_graph(df1)
            st.plotly_chart(fig)
            
        with col2:
            
            cols = ['City', 'Time_taken(min)','Type_of_order']
            df_aux = df1.loc[:, cols].groupby(['City','Type_of_order']).agg({'Time_taken(min)': ['mean','std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()

            st.dataframe( df_aux )
                   
        
        
    with st.container():
        
        st.markdown("""---""")
        st.title( "Distribuição do Tempo" )
            
        col1, col2 = st.columns(2)
        with col1:                  
            fig = distance(df1, fig=True)
            st.plotly_chart(fig)

#                         
        with col2:
            fig = avg_std_time_on_traffic(df1)
            st.plotly_chart(fig)