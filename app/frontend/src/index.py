import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd
API_URL = "http://127.0.0.1:5000/"


def find_zips_for_city(city):
    response = requests.get(API_URL, params={'zips_for_city': city})
    return response.json()


def find_zips():
    response = requests.get(API_URL, params={'zipcodes'})


def find_cities_for_zip(zipcode):
    response = requests.get(API_URL, params={'cities_for_zip': zipcode})
    return response.json()

# def venue_ratings(venues    , requires_rating = False):
#     if requires_rating:
#         venues = [venue for venue in venues if venue['rating'] != -99]
#     return [venue['rating'] for venue in venues]


# price = st.sidebar.slider(min_value = 1,
#                             max_value = 2,
#                             step = 1,
#                             label = 'price')
st.header('Cities')
# cities = find_cities_for_zip('')
# zipcodes = find_zips()

# def venue_locations(venues):
#     return [venue['location'] for venue in venues if venue.get('location') ]


# scatter = go.Scatter(x = find_zips(venues, True),
#         y = venue_ratings(venues, True),
#         hovertext = venue_names(venues, True), mode = 'markers')

# locations = venue_locations(venues)


# fig = go.Figure(scatter)
# # st.plotly_chart(fig)
# st.map(pd.DataFrame(locations))
