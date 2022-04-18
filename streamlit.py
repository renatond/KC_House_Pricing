from email.policy import default
from faulthandler import disable
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sea
from sympy import appellf1
import streamlit as st
import plotly.express as px
import folium
from folium import *
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import geopandas
from datetime import datetime



# ================================================
# Settings
# ================================================

# Geofile definition
url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
geofile = geopandas.read_file(url)

# pandas config
pd.set_option('display.float_format', lambda x: '%.1f' % x)

st.set_page_config(layout='wide')
# streamlit config


# hide_dataframe_row_index = """
#             <style>
#             .row_heading.level0 {display:none}
#             .blank {display:none}
#             </style>
#             """

# # Inject CSS with Markdown
# st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

# ================================================
# Load Data
# ================================================


@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)
    data['date'] = pd.to_datetime(data['date'])

    return data


data = get_data('Datasets/kc_house_data.csv')

# ==============================================
# Data transformation
# ==============================================

data['m2_living'] = data['sqft_living'] * 0.092903
data['m2_lot'] = data['sqft_lot'] * 0.092903
data['price_m2'] = data['price']/(data['sqft_lot'] * 0.092903)

attributes = ['price', 'bedrooms', 'm2_living',
              'm2_lot', 'condition', 'grade', 'zipcode']


median_by_region = data[attributes].groupby('zipcode').median().reset_index()
median_by_region.columns = ['zipcode', 'median_price', 'median_bedrooms', 'median_m2_living',
                            'median_m2_lot', 'median_condition', 'median_grade']

data = pd.merge(data, median_by_region, on='zipcode', how='inner')

data = data.drop(['sqft_living', 'sqft_living15',
                 'sqft_lot', 'sqft_lot15'], axis=1)

# Opportunities dataset =========================
opp = data[(data['price'] < data['median_price']) &
           (data['condition'] > data['median_condition']) &
           (data['m2_lot'] > data['median_m2_lot']) &
           (data['m2_living'] > data['median_m2_living'])].reset_index()

# descriptive statistics ========================

# Average metrics
ids_per_zipcode = data[['id', 'zipcode']].groupby(
    'zipcode').count().reset_index()
metrics_per_zipcode = data[['price', 'm2_living', 'price_m2', 'zipcode']].groupby(
    'zipcode').mean().reset_index()

# merge
avg_stats = pd.merge(ids_per_zipcode, metrics_per_zipcode,
                     on='zipcode', how='inner')

avg_stats.columns = ['Zipcode', 'Total Houses',
                     'Price', 'Living Area', 'Price/m2']

# Statistic Descriptive
num_attributes = data.select_dtypes(include=['int64', 'float64'])
num_attributes = num_attributes.drop('id', axis=1)
mean_ = pd.DataFrame(num_attributes.apply(np.mean))
median_ = pd.DataFrame(num_attributes.apply(np.median))
std_ = pd.DataFrame(num_attributes.apply(np.std))

max_ = pd.DataFrame(num_attributes.apply(np.max))
min_ = pd.DataFrame(num_attributes.apply(np.min))

descriptive_stats = pd.concat(
    [max_, min_, mean_, median_, std_], axis=1).reset_index()

descriptive_stats.columns = ['Attributes', 'Max',
                             'Min', 'Mean', 'Median', 'Std. Deviation']

yr_built_list = data['yr_built'].unique()
min_year_built = int(data['yr_built'].min())
max_year_built = int(data['yr_built'].max())

min_price = int( data['price'].min() )
max_price = int( data['price'].max() )
avg_price = int(data['price'].mean())
median_price = int(data['price'].median())

# ================================================
# Sidebar filters
# ================================================

st.sidebar.title('Filters')

# Data Overview Filters
data_overview_filters = st.sidebar.expander(label='Data Overview Filters')
with data_overview_filters:

    # dataset columns ===============================
    data_selection = data.columns.tolist()
    data_selection.append('ALL')
    default_att = ['id', 'price', 'bedrooms',
                   'bathrooms', 'm2_living', 'm2_lot', 'zipcode']

    columns_containter = data_overview_filters.container()
    all_attributes = data_overview_filters.checkbox(
        'Select all columns', True)

    if all_attributes:
        s_attributes = columns_containter.multiselect("Select one or more options:",
                                                      data_selection, 'ALL')
        f_attributes = data.columns.tolist()
    else:
        s_attributes = columns_containter.multiselect("Select one or more options:",
                                                      data_selection, default_att)
        if 'ALL' in s_attributes:
            f_attributes = data.columns.tolist()
        else:
            f_attributes = s_attributes

    # zipcode selection ============================
    zipcode_selection = data['zipcode'].unique().tolist()
    zipcode_selection.append('ALL')

    zipcode_container = data_overview_filters.container()
    all_zipcodes = data_overview_filters.checkbox('Select all zipcodes', True)

    if all_zipcodes:
        s_zipcodes = zipcode_container.multiselect('Select zipcodes:',
                                                   zipcode_selection, 'ALL')
        f_zipcodes = data['zipcode'].unique().tolist()
    else:
        s_zipcodes = zipcode_container.multiselect("Select one or more options:",
                                                   zipcode_selection, 'ALL')
        if 'ALL' in s_zipcodes:
            f_zipcodes = data['zipcode'].unique().tolist()
        else:
            f_zipcodes = s_zipcodes

    # number of bedrooms ============================
    bedrooms_selection = sorted(data['bedrooms'].unique().tolist())
    bedrooms_selection.append('ALL')

    bedrooms_container = data_overview_filters.container()
    all_bedrooms = data_overview_filters.checkbox('Select all bedrooms')

    if all_bedrooms:
        s_bedrooms = bedrooms_container.multiselect('Select the numbers of bedrooms:',
                                                    bedrooms_selection, 'ALL')
        f_bedrooms = sorted(data['bedrooms'].unique().tolist())
    else:
        s_bedrooms = bedrooms_container.multiselect('Select the numbers of bedrooms:',
                                                    bedrooms_selection, 2)
        if 'ALL' in s_bedrooms:
            f_bedrooms = sorted(data['bedrooms'].unique().tolist())
        else:
            f_bedrooms = s_bedrooms

    # number of bedrooms ============================
    bathrooms_selection = sorted(data['bathrooms'].unique().tolist())
    bathrooms_selection.append('ALL')

    bathrooms_container = data_overview_filters.container()
    all_bathrooms = data_overview_filters.checkbox('Select all bathrooms')

    if all_bathrooms:
        s_bathrooms = bathrooms_container.multiselect('Select the numbers of bathrooms:',
                                                    bathrooms_selection, 'ALL')
        f_bathrooms = sorted(data['bathrooms'].unique().tolist())
    else:
        s_bathrooms = bathrooms_container.multiselect('Select the numbers of bathrooms:',
                                                    bathrooms_selection, 2)
        if 'ALL' in s_bathrooms:
            f_bathrooms = sorted(data['bathrooms'].unique().tolist())
        else:
            f_bathrooms = s_bathrooms

    # price range ===================================

    price_slider = data_overview_filters.slider('Price Range',
                                                min_price,
                                                min_price,
                                                median_price)

    # waterfront ===================================

    wf1, wf2 = data_overview_filters.columns((1, 1))

    wf_yes = wf1.checkbox('Waterfront', True)
    wf_no = wf2.checkbox('No Waterfront', True)

    if wf_yes & wf_no:
        f_waterfront = [0, 1]
    elif wf_yes and not wf_no:
        f_waterfront = [1]
    else:
        f_waterfront = [0]

analysis_filters = st.sidebar.expander(label='Analyis Filters')
with analysis_filters:
    f_bedrooms_analysis = analysis_filters.slider('Max number of bedrooms', data['bedrooms'].min(), data['bedrooms'].max(), data['bedrooms'].max())
    f_bathrooms_analysis = analysis_filters.slider('Max number of bathrooms', data['bathrooms'].min(), data['bathrooms'].max(), data['bathrooms'].max())
    f_floors = analysis_filters.slider('Max number of floors', data['floors'].min(), data['floors'].max(), data['floors'].max())

# ==============================================
# filtered data transformation
# ==============================================

filtered_data = data[(data['price'] < price_slider) &
                     (data['bedrooms'].isin(f_bedrooms)) &
                     (data['waterfront'].isin(f_waterfront))]

filtered_opp_data = opp[(opp['price'] < price_slider) &
                        (opp['bedrooms'].isin(f_bedrooms)) &
                        (opp['waterfront'].isin(f_waterfront))]

df = data[f_attributes]

# ==============================================
# Data Overview
# ==============================================

st.title( 'House Rocket Company')
st.markdown(' Welcome to House Rocet Data Analysis')
st.header ( 'Data overview')
float_columns = data.select_dtypes( include=[ 'float64'] ).columns

columns_list = ["id","bathrooms","bedrooms","condition","date","floors","grade","lat","long","m2_living","median_bedrooms","median_condition","median_grade","median_price","median_sqft_living","median_sqft_lot","price","price_m2","sqft_above","sqft_basement","view","waterfront","yr_built","yr_renovated","zipcode"]

st.dataframe(df.style.format(subset=float_columns, formatter="{:.2f}"), height=200)

c1, c2 = st.columns((1, 1) )

c1.header( 'Average Values' )
c1.dataframe( df.style.format(subset=float_columns, formatter="{:.2f}"), height=200 )

c2.header( 'Descriptive Analysis' )
c2.dataframe( descriptive_stats, height=200 )

display_filtered_data = st.checkbox( 'Display filtered data')

if display_filtered_data:
    st.dataframe(filtered_data.style.format(subset=float_columns, formatter="{:.2f}"), height=200)

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

display_opp_data = st.checkbox('Display current opportunities')

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

# ==============================================
# Density Overview
# ==============================================

st.title('Region Overview')

c1, c3, c2 = st.columns((10, 1, 10))
c1.header('Portfolio Density')

df = data.sample(1000)

# Base Map - Folium
density_map = folium.Map(location=[data['lat'].mean(),
                                   data['long'].mean()],
                         default_zoom_start=15)

marker_cluster = MarkerCluster().add_to(density_map)
for name, row in df.iterrows():
    folium.Marker([row['lat'], row['long']],
                  popup=folium.Popup('Price R${0}, since {1}, Features: {2} sqft, {3} bedrooms, {4} bathrooms, year built: {5}'.format(row['price'],
                  row['date'],
                  row['m2_living'],
                  row['bedrooms'],
                  row['bathrooms'],
                  row['yr_built']),
                  min_width=500)).add_to(marker_cluster)

with c1:
    folium_static(density_map, width=550)

# Region Price Map
c2.header('Price Density')

df = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
df.columns = ['ZIP', 'PRICE']

geofile = geofile[geofile['ZIP'].isin(df['ZIP'].tolist())]

region_price_map = folium.Map(location=[data['lat'].mean(),
                                        data['long'].mean()],
                              default_zoom_start=15)

region_price_map.choropleth(data=df,
                            geo_data=geofile,
                            columns=['ZIP', 'PRICE'],
                            key_on='feature.properties.ZIP',
                            fill_color='YlOrRd',
                            fill_opacity=0.7,
                            line_opacity=0.2,
                            legend_name='AVG PRICE')

with c2:
    folium_static(region_price_map, width=550)

# ==============================================
# Metrics Overview
# ==============================================

c1, c2 = st.columns((1,1))

# Houses per bedrooms
c1.header( 'Houses per bedrooms' )
df = data[data['bedrooms'] <= f_bedrooms_analysis]
# fig = px.histogram( df, x='bedrooms', nbins=19 )
# c1.plotly_chart( fig, use_containder_width=True )

dataframe = data[['bathrooms','id']].groupby('bathrooms').count().reset_index()
dataframe.columns = ['bathrooms', 'QTD.']

fig = sea.countplot(data=df, x='bedrooms')
st.pyplot(fig.get_figure())

# Houses per bathrooms
c2.header( 'Houses per bathrooms' )
df = dataframe[dataframe['bathrooms'] <= f_bathrooms_analysis]
rows = df.shape[0]
fig = px.bar( df.head(rows), x='bathrooms', y='QTD.', text_auto=True, color='bathrooms', color_continuous_scale=px.colors.sequential.YlOrRd )
fig.update_layout(bargap=0.2)
st.plotly_chart( fig, use_containder_width=True )
