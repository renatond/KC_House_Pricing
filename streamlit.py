import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import folium
from streamlit_folium import folium_static
from folium.plugins   import MarkerCluster
import geopandas

url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
#================================================
# Settings
#================================================
geofile = geopandas.read_file( url )

# pandas config
pd.set_option('display.float_format', lambda x: '%.1f' % x)

# streamlit config
st.set_page_config( layout = 'wide')

#================================================
# Load Data
#================================================



@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)
    data['date'] = pd.to_datetime(data['date'])

    return data

data = get_data('Datasets/kc_house_data.csv')

#==============================================
# Data transformation
#==============================================

data['m2_living'] = data['sqft_living'] * 0.092903
data['price_m2'] = data['price']/( data['sqft_lot'] * 0.092903)

attributes = ['price', 'bedrooms', 'sqft_living',
                  'sqft_lot', 'condition', 'grade', 'zipcode']


median_by_region = data[attributes].groupby('zipcode').median().reset_index()
median_by_region.columns = ['zipcode', 'median_price', 'median_bedrooms', 'median_sqft_living',
                             'median_sqft_lot', 'median_condition', 'median_grade']

data = pd.merge(data, median_by_region, on='zipcode', how='inner')

# Opportunities dataset =========================
opp = data[(data['price'] < data['median_price']) &
         (data['condition'] > data['median_condition']) &
         (data['sqft_lot'] > data['median_sqft_lot']) &
         (data['sqft_living'] > data['median_sqft_living'])].reset_index()

# descriptive statistics ========================

# Average metrics
df1 = data[['id', 'zipcode']].groupby( 'zipcode' ).count().reset_index()
df2 = data[['price','sqft_living','price_m2', 'zipcode']].groupby( 'zipcode').mean().reset_index()

# merge
df = pd.merge( df1, df2, on='zipcode', how='inner' )

df.columns = ['ZIPCODE', 'TOTAL HOUSES', 'PRICE', 'SQRT LIVING',
              'PRICe/M2']

# Statistic Descriptive
num_attributes = data.select_dtypes( include=['int64', 'float64'] )
num_attributes = num_attributes.drop('id', axis=1)
media = pd.DataFrame( num_attributes.apply( np.mean ) )
mediana = pd.DataFrame( num_attributes.apply( np.median ) )
std = pd.DataFrame( num_attributes.apply( np.std ) )

max_ = pd.DataFrame( num_attributes.apply( np.max ) ) 
min_ = pd.DataFrame( num_attributes.apply( np.min ) ) 

df1 = pd.concat([max_, min_, media, mediana, std], axis=1 ).reset_index()

df1.columns = ['attributes', 'max', 'min', 'mean', 'median', 'std'] 

#================================================
# Sidebar filters
#================================================

# dataset columns ===============================

f_attributes = st.sidebar.multiselect('Select columns:', data.columns)

all_attributes = st.sidebar.checkbox( 'Select all columns', True)

if all_attributes:
    f_attributes = sorted(data.columns)
 
else:
    f_attributes = f_attributes

# number of bedrooms ============================

f_bedrooms =st.sidebar.multiselect(
     'Number of bedrooms: ',
     sorted(data['bedrooms'].unique()), 1)

all_bedrooms = st.sidebar.checkbox( 'Select all')

if all_bedrooms:
    f_bedrooms = sorted(data['bedrooms'].unique())
    #st.header (f_bedrooms)
else:
    f_bedrooms = f_bedrooms
    #st.header (f_bedrooms)

# price range ===================================

price_min = int(data['price'].min())
price_max = int(data['price'].max())
price_avg = int(data['price'].mean())
price_median = int(data['price'].median())

price_slider = st.sidebar.slider('Price Range',
                                price_min,
                                price_max,
                                price_median)

# waterfront ===================================

f_waterfront = st.sidebar.checkbox( 'Waterfront')

if f_waterfront:
    _waterfront = 1
else:
    _waterfront = 0


#==============================================
# filtered data transformation
#==============================================

filtered_data = data[(data['price'] < price_slider) &
                    (data['bedrooms'].isin(f_bedrooms)) &
                    (data['waterfront'] == _waterfront)]

filtered_opp_data = opp[(opp['price'] < price_slider) &
                        (opp['bedrooms'].isin(f_bedrooms)) &
                        (opp['waterfront'] == _waterfront)]

df = data[f_attributes]

#==============================================
# Data Overview
#==============================================

st.title( 'House Rocket Company')
st.markdown(' Welcome to House Rocet Data Analysis')
st.header ( 'Data overview')

st.dataframe(df, height=200)

c1, c2 = st.columns((1, 1) )  

c1.header( 'Average Values' )
c1.dataframe( df, height=200 )

c2.header( 'Descriptive Analysis' )
c2.dataframe( df1, height=200 )

display_filtered_data = st.checkbox( 'Display filtered data')

if display_filtered_data:
    st.dataframe(filtered_data, height=200)

# Draw map

data_map = px.scatter_mapbox(filtered_data,
                            lat='lat',
                            lon='long',
                            color='price',
                            size='price',
                            hover_name='id',
                            hover_data=['price'],
                            color_discrete_sequence=['darkgreen'],
                            # color_continuous_scale=px.colors.cyclical.IceFire,
                            zoom=9,
                            height=300)

data_map.update_layout(mapbox_style='open-street-map')
data_map.update_layout(height=600, margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
st.plotly_chart(data_map, use_container_width=True)

display_opp_data = st.checkbox( 'Display current opportunities')

opp_map = px.scatter_mapbox(filtered_opp_data,
                            lat='lat',
                            lon='long',
                            color='price',
                            size='price',
                            hover_name='id',
                            hover_data=['price'],
                            color_discrete_sequence=['darkgreen'],
                            # color_continuous_scale=px.colors.cyclical.IceFire,
                            zoom=9,
                            height=300)

opp_map.update_layout(mapbox_style='open-street-map')
opp_map.update_layout(height=600, margin={'r': 0, 't': 0, 'l': 0, 'b': 0})

if display_opp_data:
    st.dataframe(filtered_opp_data, height=200)
    st.plotly_chart(opp_map, use_container_width=True)

#==============================================
# Density Overview
#==============================================

st.title( 'Region Overview' )

c1, c2 = st.columns( ( 1, 1 ) )
c1.header( 'Portfolio Density' )


df = data.sample( 10 )

# Base Map - Folium 
density_map = folium.Map( location=[data['lat'].mean(), 
                          data['long'].mean() ],
                          default_zoom_start=15 ) 

marker_cluster = MarkerCluster().add_to( density_map )
for name, row in df.iterrows():
    folium.Marker( [row['lat'], row['long'] ], 
        popup='Sold R${0} on: {1}. Features: {2} sqft, {3} bedrooms, {4} bathrooms, year built: {5}'.format( row['price'],
                                     row['date'],
                                     row['sqft_living'],
                                     row['bedrooms'],
                                     row['bathrooms'],
                                     row['yr_built'] ) ).add_to( marker_cluster )


with c1:
    folium_static( density_map )

# Region Price Map
c2.header( 'Price Density' )

df = data[['price', 'zipcode']].groupby( 'zipcode' ).mean().reset_index()
df.columns = ['ZIP', 'PRICE']

#df = df.sample( 10 )

geofile = geofile[geofile['ZIP'].isin( df['ZIP'].tolist() )]

region_price_map = folium.Map( location=[data['lat'].mean(), 
                               data['long'].mean() ],
                               default_zoom_start=15 ) 


region_price_map.choropleth( data = df,
                             geo_data = geofile,
                             columns=['ZIP', 'PRICE'],
                             key_on='feature.properties.ZIP',
                             fill_color='YlOrRd',
                             fill_opacity = 0.7,
                             line_opacity = 0.2,
                             legend_name='AVG PRICE' )

with c2:
    folium_static( region_price_map )