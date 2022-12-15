# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 08:56:33 2021

@author: IPSMX-L7NRKD03
"""

# Data load Package
#import io
from datetime import date

# Core Packages
import streamlit as st
from PIL import Image

# EDA Packages
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# Data Viz Packages
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objs as go


#####lgoos added to the dashboard
APP_TITLE = "Ogarrio Data"
img=Image.open('images\wdealogo2.png')
img1=Image.open('images\wdealogo.png')
st.set_page_config(
    page_title = APP_TITLE,
    page_icon = img1,
    layout = "wide")

img_sidebar= st.sidebar.columns(3)
img_sidebar[1].image(img,width=150)
#########################


#################### PRODUCTION DATA ####################

### csv issues onge file has well name as OG and the other and OGARRIO, changed them to Ogarrio

def prod_data(path3):
	prod_df = pd.read_csv(path3, encoding = "ISO-8859-1")
	#prod_df = prod_df.loc[:, ~prod_df.columns.str.contains('^Unnamed')]
	#prod_df.columns = [x.lower() for x in prod_df.columns]
	prod_df['Date'] = pd.to_datetime(prod_df['Date'])
	return prod_df
	
prod = prod_data(r'data\DAILYPROD.csv')
st.cache(prod)

############################Well Data##########################################

def prod_data(path4):
	wells_df = pd.read_csv(path4, encoding = "ISO-8859-1")
	#prod_df = prod_df.loc[:, ~prod_df.columns.str.contains('^Unnamed')]
	#prod_df.columns = [x.lower() for x in prod_df.columns]
	#prod_df['Date'] = pd.to_datetime(prod_df['Date'])
	return wells_df
	
wells = prod_data(r'data\ogarrio_wells.csv')
st.cache(wells)

#################### MAPA Y TABLA ####################





st.cache()
with st.sidebar.expander('Well Selector'):
    pozos = prod['Well'].unique()
    filt_pozos = st.selectbox('Select a well', pozos)
    #pozo = campo[campo['terminacion'] == filt_pozos]
tab1, tab2, tab3 = st.tabs(["Ogarrio Well Maps", "Ogarrio Production Graphs", "Calculations"])

with tab1:
   with st.container():
    #################### EXPANDER 1 - CHECK RAW DATA ####################
    with st.expander('Raw Data'):
        st.subheader('Data Loaded')
        st.write(wells)


    with st.expander('Ogarrio Wells with coordinates'):
        coords = wells[['Well','Lat', 'Long']]
        coords['Lat'] = pd.to_numeric(coords['Lat'])
        coords['Long'] = pd.to_numeric(coords['Long'])
        coords = coords.dropna()

        for_map = wells.copy()
        for_map = for_map[['Well', 'Estatus', 'Pera/Macropera', 'Bateria', 'Long', 'Lat', 'Macropera', 'PT', 'Tipo']]
        map_filt = for_map.dropna()
        st.dataframe(map_filt)
   
         #################### location map ####################  
   with st.expander('Well Location'):
        map_pozos_loc = px.scatter_mapbox(wells, lat="Lat", lon="Long", hover_name="Well", zoom=7.5, color='Estatus', color_discrete_sequence=px.colors.qualitative.Alphabet)
        map_pozos_loc.update_layout(mapbox_style="stamen-terrain", margin={"r":0,"t":0,"l":0,"b":0}, height=300, width=800, showlegend=False)
        map_pozos_loc.update_layout(showlegend=True)
        st.plotly_chart(map_pozos_loc)
   del prod['Date']
   df1 =  prod.groupby('Well').sum()     
   prod_wells =  pd.merge(df1, wells, on='Well')
   #df['Date'] = pd.to_datetime(df['Date'])
   #prod_wells = df.groupby(['Well', pd.Grouper(key='Date')]).agg({'Qneto':sum,'Qbruto':sum,'Fagua':sum,'Qagua':sum,'Qgasform':sum,'Qgastotal':sum,'Qgasiny':sum})
   #st.dataframe(prod_wells)
# Space out the maps so the first one is 2x the size of the other three
   c1, c2, c3 = st.columns((0.15, .15, .15))
   with c1:
        with st.expander('Oil Production'): 
            fig2 = px.scatter_mapbox(prod_wells, lat="Lat", lon="Long",  hover_data=["Well","Qbruto","Qneto"],
                                    color = 'Estatus', size ="Qneto" ,zoom=8,width= 420,  height=300)
            fig2.update_layout(mapbox_style="stamen-terrain")
            fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            fig2.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01,bgcolor='rgba(0,0,0,0)',))
            st.plotly_chart(fig2, use_column_width=True)
   with c2:
        with st.expander('Gas Production'): 
            fig3 = px.scatter_mapbox(prod_wells, lat="Lat", lon="Long", hover_data=["Well","Qgasform","Qgastotal","Qgasiny"],
                                    color = 'Estatus', size ="Qgastotal" ,zoom=8,width= 420, height=300)
            fig3.update_layout(mapbox_style="stamen-terrain")
            fig3.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            fig3.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01,bgcolor='rgba(0,0,0,0)',))
            st.plotly_chart(fig3, use_column_width=True)

   with c3:
        with st.expander('Water Production'):
            fig4 = px.scatter_mapbox(prod_wells, lat="Lat", lon="Long", hover_data=["Well","Fagua","Qagua"],
                                    color = 'Estatus', size ="Qagua" ,zoom=8,width= 420,  height=300)
            fig4.update_layout(mapbox_style="stamen-terrain")
            fig4.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            fig4.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01,bgcolor='rgba(0,0,0,0)',))
            st.plotly_chart(fig4,  use_column_width=True)
        
 

with tab2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
   
