import streamlit as st
import sql_query.sql_queries as sql
import folium
from streamlit_folium import folium_static
import requests
import os
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

#Request the address of the starting point.
st.markdown(f"<h2 style='text-align: left;'>Where are you starting from?</h2>", unsafe_allow_html=True)
input_address = st.text_input('Format: City, Region.')
gkey=os.getenv('google_key')

if 'start_point' not in st.session_state:
    st.session_state['start_point'] = {}
if 'possible_spots' not in st.session_state:
    st.session_state['possible_spots'] = pd.DataFrame({})


if st.button("Search you coordinates!"):

    try:
    
        # Get the latitude and longitude from the first result in the response
        start_point = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={input_address}&key={gkey}').json()['results'][0]['geometry']['location']
        st.session_state['start_point'] = start_point
        start_lat = start_point['lat']
        start_lng = start_point['lng']
        try:
            st.markdown(f"<h4 style='text-align: left;'>The coordinates of {input_address} are ({start_lat}, {start_lng})</h4>", unsafe_allow_html=True)
        except:
            st.markdown(f"<h4 style='text-align: left;'>Sorry! We didn't finde the coordinates for this place: {input_address}</h4>", unsafe_allow_html=True)
            pass
    except:
        pass




st.write('---')

st.markdown(f"<h2 style='text-align: left;'>What region in Spain you would like to visit?</h2>", unsafe_allow_html=True)
community = st.multiselect(
    '',
    ['Cantabria', 'Cataluña', 'Valencia', 'Galicia', 'Navarra',
       'Extremadura', 'Aragon', 'Castilla-Leon', 'Andalucia',
       'Pais Vasco', 'La Rioja', 'Castilla-La Mancha', 'Asturias',
       'Baleares', 'Madrid', 'Murcia'],'Cataluña')

st.markdown(f"<h4 style='text-align: left;'>Your selection:</h4>", unsafe_allow_html=True)

try:
    result_community = ''
    for i in community:
        result_community + i + '. '
    st.markdown(f"<h3 style='text-align: left;'>{result_community}</h3>", unsafe_allow_html=True)
except:
    pass
    




st.write('---')



st.markdown(f"<h2 style='text-align: left;'>What kind of places do you want to visit?</h2>", unsafe_allow_html=True)

category = st.multiselect('',
    ['natural parks', 'museums', 'castles', 'beaches', 'monuments',
       'historic sites', 'villages', 'towns', 'cities', 'markets',
       'festivals', 'wineries', 'cathedrals', 'palaces', 'mountains',
       'traditional restaurant', 'cave'],'beaches')

st.markdown(f"<h4 style='text-align: left;'>Your selection:</h4>", unsafe_allow_html=True)

try:
    result_category = ''
    for i in category:
        result_category + i + '. '
    st.markdown(f"<h3 style='text-align: left;'>{result_category}</h3>", unsafe_allow_html=True)
except:
    pass


st.write('---')

st.markdown(f"<h2 style='text-align: center;'>Select the mínimum rating you want the places to have</h2>", unsafe_allow_html=True)


rating = st.slider(
    '',
    min_value=1.0, max_value=5.0,step=0.1)

st.markdown(f"<h4 style='text-align: left;'>Your minimum rating:</h4>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: left;'>{rating}</h3>", unsafe_allow_html=True)

st.write('---')


st.markdown(f"<h2 style='text-align: left;'>Where would you like to spend the night with your camper?</h2>", unsafe_allow_html=True)

night_category = st.multiselect('',
    ['Parking lot day/night','Camping', 'Picnic area',
       'Free motorhome area', 'Daily parking lot only ',
       'Private car park for campers ', 'Paying motorhome area',
       'Surrounded by nature', 'Rest area', 'Extra services',
       'Off road (4x4)', 'On the farm (farm',
       'Service area without parking', 'Homestays accommodation'],'Surrounded by nature')

st.markdown(f"<h4 style='text-align: left;'>Your selection:</h4>", unsafe_allow_html=True)

try:
    result_night_category = ''
    for i in night_category:
        result_night_category + i + '. '
    st.markdown(f"<h3 style='text-align: left;'>{result_night_category}</h3>", unsafe_allow_html=True)
except:
    pass


st.write('---')


st.markdown(f"<h2 style='text-align: center;'>How far apart do you want your night spots?</h2>", unsafe_allow_html=True)


max_dist = st.slider(
    '',
    min_value=20, max_value=200, step=20)

st.markdown(f"<h4 style='text-align: left;'>Your distance between night spots:</h4>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: left;'>{max_dist} km.</h3>", unsafe_allow_html=True)

st.write('---')




dict_filters = {
                'community':community,
                'category':category,
                'rating':rating,
                'night_category':night_category,
                'max_dist':max_dist
                }



if st.button("Let's GO!"):
    possible_locations = sql.select_location_filters(dict_filters)
    possible_spots = sql.select_spot_filter(dict_filters)
    possible_spots = sql.count_location(possible_locations,possible_spots)
    possible_spots = sql.assign_candidates(possible_spots,dict_filters)
    possible_spots = possible_spots[possible_spots['candidate']==1]
    st.session_state['possible_spots'] = possible_spots


    try:

        st.markdown(f"<h2 style='text-align: left;'>🚐 Here you have all the spots we found! 🚐</h2>", unsafe_allow_html=True)
        # Define the map
        map_possible_locations = folium.Map(location=[possible_locations['lat'].mean(), possible_locations['lon'].mean()], zoom_start=8)

        # Define the colors for each category
        location_colors = {
            'natural parks': 'green',
            'museums': 'lightblue',
            'castles': 'purple',
            'beaches': 'blue',
            'monuments': 'gray',
            'historic sites': 'cadetblue',
            'villages': 'pink',
            'towns': 'red',
            'cities': 'darkred',
            'markets': 'lightgray',
            'festivals': 'beige',
            'wineries': 'darkgreen',
            'cathedrals': 'darkpurple',
            'palaces': 'lightred',
            'mountains': 'brown',
            'traditional restaurant': 'red',
            'cave': 'brown'
        }
        locations_group = folium.FeatureGroup(name='Locations')

        # Add the markers to the group
        for index, row in possible_locations.iterrows():
            locations_group.add_child(folium.Marker(
                location=[row['lat'], row['lon']],
                icon=folium.Icon(color=location_colors[row['category']],icon='circle'),
                popup=row['Name']))
        
        map_possible_locations.add_child(locations_group)

        # Show the map

        
    except:
        pass
    df_selected = possible_spots[['night_category','address', 'rating', 'url']]
    df_selected.columns = ['Category', 'Address', 'Rating', 'Url'] # Rename columns

    st.dataframe(df_selected)
    
    try:
        route_map = sql.plot_route(st.session_state['start_point'],possible_spots,gkey)
        map_possible_locations.add_child(route_map)
       
    except:
        pass
    
    try:
        folium.LayerControl(collapsed=False, position="topleft").add_to(map_possible_locations)
        folium_static(map_possible_locations)


    except:
        pass
    

        
 
            

     
    

