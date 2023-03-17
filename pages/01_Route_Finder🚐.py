import streamlit as st
import sql_query.sql_queries as sql
import folium
from streamlit_folium import folium_static
import requests
import os
from dotenv import load_dotenv
import pandas as pd
from PIL import Image
load_dotenv()

st.set_page_config(
     page_title="Find your route",
     page_icon="🚐",
     layout="wide",
     initial_sidebar_state="expanded",
     
 )

st.write("""
        <style>
        /* Define the style for the h2 headings */
        h2 {
            color: brown;
        }
        </style>
        """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🏔️ CAMPI QUI PUGUI! 🏖️</h1>", unsafe_allow_html=True)
st.markdown('---')
st.markdown("<h2 style='text-align: center;'>Let's find your perfect roadtrip! </h2>", unsafe_allow_html=True)


picture_map = Image.open('images/road_picture.jpeg')
st.image(picture_map,use_column_width=True)

#Request the address of the starting point.
st.markdown(f"<h2 style='text-align: center;'>Where are you starting from?</h2>", unsafe_allow_html=True)
input_address = st.text_input('Write your place name with the format: City, Region. And click Search.','Sant Pol de Mar, Barcelona')
gkey=os.getenv('google_key')

#Store variables so they are kept each session.
if 'start_point' not in st.session_state:
    st.session_state['start_point'] = {}
if 'possible_spots' not in st.session_state:
    st.session_state['possible_spots'] = pd.DataFrame({})


if st.button("Search you coordinates!"):

    try:
    
        # Get the latitude and longitude of the address imput by the user
        start_point = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={input_address}&key={gkey}').json()['results'][0]['geometry']['location']
        st.session_state['start_point'] = start_point
        start_lat = start_point['lat']
        start_lng = start_point['lng']
        
        # Display the selection
        try:
            st.markdown(f"<h4 style='text-align: left;'>The coordinates of {input_address} are ({start_lat}, {start_lng})</h4>", unsafe_allow_html=True)
            starting_point_map = folium.Map((start_lat,start_lng),zoom_start=10)
            folium.Marker(location=(start_lat,start_lng),popup=input_address).add_to(starting_point_map)
            folium_static(starting_point_map)
        except:
            st.markdown(f"<h4 style='text-align: left;'>Sorry! We didn't finde the coordinates for this place: {input_address}</h4>", unsafe_allow_html=True)
            pass
    except:
        st.markdown(f"<h4 style='text-align: left;'>Not even requesting</h4>", unsafe_allow_html=True)
        pass




st.write('---')

# Request the selection of region

st.markdown(f"<h2 style='text-align: center;'>What region in Spain you would like to visit?</h2>", unsafe_allow_html=True)
community = st.multiselect(
    '',
    ['Cantabria', 'Cataluña', 'Valencia', 'Galicia', 'Navarra',
       'Extremadura', 'Aragon', 'Castilla-Leon', 'Andalucia',
       'Pais Vasco', 'La Rioja', 'Castilla-La Mancha', 'Asturias',
       'Baleares', 'Madrid', 'Murcia'],'Cantabria')

# Display the selection
st.markdown(f"<h4 style='text-align: left;'>Your selection:</h4>", unsafe_allow_html=True)

try:
    result_community = ''
    for i in community:
        result_community + i + '. '
    st.markdown(f"<h3 style='text-align: left;'>{result_community}</h3>", unsafe_allow_html=True)
except:
    pass
    




st.write('---')


# Request the kind of places the user would like to visit

st.markdown(f"<h2 style='text-align: center;'>What kind of places do you want to visit?</h2>", unsafe_allow_html=True)

category = st.multiselect('',
    ['natural parks', 'museums', 'castles', 'beaches', 'monuments',
       'historic sites', 'villages', 'towns', 'cities', 'markets',
       'festivals', 'wineries', 'cathedrals', 'palaces', 'mountains',
       'traditional restaurant', 'cave'],'beaches')

# Display the selection
st.markdown(f"<h4 style='text-align: left;'>Your selection:</h4>", unsafe_allow_html=True)

try:
    result_category = ''
    for i in category:
        result_category + i + '. '
    st.markdown(f"<h3 style='text-align: left;'>{result_category}</h3>", unsafe_allow_html=True)
except:
    pass


st.write('---')

# Request the minimum rating desired

st.markdown(f"<h2 style='text-align: center;'>Select the minimum rating you want the places to have</h2>", unsafe_allow_html=True)


rating = st.slider(
    '',
    min_value=1.0, max_value=5.0,step=0.1,value=4.0)

# Display the selection

st.markdown(f"<h4 style='text-align: left;'>Your minimum rating:</h4>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: left;'>{rating}</h3>", unsafe_allow_html=True)

st.write('---')


# Request the type of night spots

st.markdown(f"<h2 style='text-align: center;'>Where would you like to spend the night with your camper?</h2>", unsafe_allow_html=True)

night_category = st.multiselect('',
    ['Parking lot day/night','Camping', 'Picnic area',
       'Free motorhome area', 'Daily parking lot only ',
       'Private car park for campers ', 'Paying motorhome area',
       'Surrounded by nature', 'Rest area', 'Extra services',
       'Off road (4x4)', 'On the farm (farm',
       'Service area without parking', 'Homestays accommodation'],'Surrounded by nature')

# Display the selection

st.markdown(f"<h4 style='text-align: left;'>Your selection:</h4>", unsafe_allow_html=True)

try:
    result_night_category = ''
    for i in night_category:
        result_night_category + i + '. '
    st.markdown(f"<h3 style='text-align: left;'>{result_night_category}</h3>", unsafe_allow_html=True)
except:
    pass


st.write('---')

# Request the distance between spots

st.markdown(f"<h2 style='text-align: center;'>How far apart do you want your night spots?</h2>", unsafe_allow_html=True)


max_dist = st.slider(
    '',
    min_value=20, max_value=200, step=20,value=40)

st.markdown(f"<h4 style='text-align: left;'>Your distance between night spots:</h4>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: left;'>{max_dist} km.</h3>", unsafe_allow_html=True)

st.write('---')


# Store each selection in a dictionary

dict_filters = {
                'community':community,
                'category':category,
                'rating':rating,
                'night_category':night_category,
                'max_dist':max_dist
                }


# Activate the functions based on the filters selected by the user

if st.button("Let's GO!"):
    possible_locations = sql.select_location_filters(dict_filters)
    possible_spots = sql.select_spot_filter(dict_filters)
    possible_spots = sql.count_location(possible_locations,possible_spots)
    possible_spots = sql.assign_candidates(possible_spots,dict_filters)
    possible_spots = possible_spots[possible_spots['candidate']==1]
    st.session_state['possible_spots'] = possible_spots

    # Display the results 
    try:

        st.markdown(f"<h2 style='text-align: left;'>🚐 Here you have all the spots we found! 🚐</h2>", unsafe_allow_html=True)
            # Define the map
        map_possible_locations = folium.Map(location=[possible_locations['lat'].mean(), possible_locations['lon'].mean()], zoom_start=8)

            #Call the function that adds the location to a folium grup
        locations_group = sql.locations_group(possible_locations)
            
        map_possible_locations.add_child(locations_group)
        
  
        
    except:
        st.text('Sorry, there was a problem creating the map.')
        pass

    # Prepare the dataframe with the spots
    df_selected = possible_spots[['night_category','address', 'rating', 'url']]
    # Rename columns
    df_selected.reset_index(inplace=True)
    df_selected.columns = ['ID','Category', 'Address', 'Rating', 'Url']
    

    # Create a markdown string to center the DataFrame
    centered_dataframe = f'<div style="display: flex; justify-content: center;">{df_selected.to_html(index=False)}</div>'

    # Render the centered DataFrame using the st.markdown() function
    st.markdown(centered_dataframe, unsafe_allow_html=True) 
    st.markdown('---')
    try:
        # Call the function that plots the route between night spots.
        route_map = sql.plot_route(st.session_state['start_point'],possible_spots,gkey)
        map_possible_locations.add_child(route_map)
       
    except:
        print('Sorry, there was a problem finding good spots')
        pass
    
    try:

        #Display the map 
        folium.LayerControl(collapsed=False, position="topleft").add_to(map_possible_locations)
        folium_static(map_possible_locations,width=1100,height=800)


    except:
        print('error amb la carrega del mapa')
        pass    
    

        
 
            

     
    

