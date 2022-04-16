# ==================
# Libraries
# ==================

import pandas as pd
import numpy as np
import plotly.express as px
import time
from multiprocessing import Pool

# Supress scientific notation
pd.set_option('display.float_format', lambda x: '%.1f' % x)

def create_recent_only_ds(data):
    # Create dataset with unique IDs, keeping the most recent acordingly to 'date'

    data_recent_only = data.sort_values(
        'date', ascending=True).drop_duplicates(subset='id', keep='last')
    data_recent_only.shape

    return None

def correct_datetimes(data):
    # Correcting date formats
    data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
    data['yr_built'] = pd.to_datetime(data['yr_built'], format='%Y')
    data['yr_built'] = data['yr_built'].dt.year

    return None

def treat_outliers(data):
    # 33 Bedroom house outlier analysis

    # Houses in the same region, with no waterfront, bigger living area, fewer bedrooms are costing more than the refered house.
    # By analysing houses within the same caracteristics and 3 bedroom, seems reasonable that 33 was a typo that should be only 3.

    data = data.sort_values('bedrooms', ascending=False).reset_index()
    data.loc[0, 'bedrooms'] = 3

    return data

def create_new_attributes(data):# Not used
    # Create Condition status based on condition level
    # if 'condition' <=2, ‘bad’
    # if 'condition' = 3 or 4, ‘regular’
    # if 'condition' =>5, ‘good’

    data['condition_type'] = data['condition'].apply(
        lambda x: 'bad' if x <= 2 else 'regular' if x <= 4 else 'good')

    # Drop unescessary columns

    data = data.drop(['sqft_living15', 'sqft_lot15'], axis=1)

    # Defining Price Range and Price Range lvl

    data['price_range'] = data['price'].apply(lambda x: 'up to $321950' if x < 321950 else
                                              '$321950 to $450000' if x < 450000 else
                                              '$450000 to $645000' if x < 645000 else
                                              'from $645000')

    data['price_cat'] = data['price'].apply(lambda x: 0 if x < 321950 else
                                            1 if x < 450000 else
                                            2 if x < 645000 else
                                            3)

    # Getting Geographical Info

    # Create lat + long column
    data['latlong'] = data[['lat', 'long']].apply(
        lambda x: str(x['lat']) + ',' + str(x['long']), axis=1)

    return data

def get_geographic_data(data):
    import defs_newatt

    # Create new attribute empty columns
    data['neighbourhood'] = 'NA'
    data['city'] = 'NA'
    data['state'] = 'NA'

    df = data[['id', 'latlong']].head(100)
    p = Pool(4)

    start = time.process_time()
    df[['neighbourhood', 'city', 'state']] = p.map(
        defs_newatt.get_data, df.iterrows())
    end = time.process_time()

    data = pd.merge(data, df, on='id', how='inner')

    print('Time Elapsed: {}', end - start)

    return data

def descriptive_statistics_analysis(data):

    attributes = ['price', 'bedrooms', 'sqft_living',
                  'sqft_lot', 'condition', 'grade', 'zipcode']

    mean_by_region = data[attributes].groupby('zipcode').mean().reset_index()
    median_by_region = data[attributes].groupby('zipcode').median().reset_index()
    max_by_region = data[attributes].groupby('zipcode').max().reset_index()
    min_by_region = data[attributes].groupby('zipcode').min().reset_index()
    std_by_region = data[attributes].groupby('zipcode').std().reset_index()

    median_by_region.columns = ['zipcode', 'median_price', 'median_bedrooms', 'median_sqft_living',
                                'median_sqft_lot', 'median_condition', 'median_grade']

    oldest_listed = data['date'].min()
    newest_listed = data['date'].max()
    max_price = data['price'].max()
    min_price = data['price'].min()
    num_bedrooms = sorted(data['bedrooms'].unique())
    price_median = data['price'].median()

    data = pd.merge(data, median_by_region, on='zipcode', how='inner')
    
    return data

def data_overview(data):
    data_map = px.scatter_mapbox(data,
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

    return data_map

def opp_overview(data):
  
    opp = data[(data['price'] < data['median_price']) &
             (data['condition'] > data['median_condition']) &
             (data['sqft_lot'] > data['median_sqft_lot']) &
             (data['sqft_living'] > data['median_sqft_living'])]

    opp_map = px.scatter_mapbox(opp,
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

    return opp_map


if __name__ == '__main__':
    # ==================
    # Extraction
    # ==================

    # load dataset
    data = pd.read_csv('Datasets/kc_house_data.csv')

    # ==================
    # Transformation
    # ==================

    # Treat outliers
    treat_outliers(data)

    # Correct date format
    correct_datetimes(data)

    # crete new attributes
    create_new_attributes(data)

    # make descriptive analysis
    descriptive_statistics_analysis(data)
    data = descriptive_statistics_analysis(data)

    # ==================
    # Load
    # ==================

    # draw maps and dashboard
    fig1 = data_overview(data)
    fig1.show()
    fig2 = opp_overview(data)
    fig2.show()