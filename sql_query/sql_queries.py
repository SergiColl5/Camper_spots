
import sqlalchemy as alch
import os 
from dotenv import load_dotenv
import pandas as pd
from geopy.distance import distance
import googlemaps
import folium
from googlemaps import convert
import numpy as np

# Loading env variables
load_dotenv()


# Connection to database
password = os.getenv("password_sql")
username= "root"
dbName = "camper"
host = "127.0.0.1"
port = "3306"
connectionData=f"mysql+pymysql://{username}:{password}@{host}:{port}/{dbName}"


engine = alch.create_engine(connectionData)



def uploading_csv_named(name):
    ''' This function takes a name, 
        reads the csv with that name and uploads it to sql as'''
    try:
        population_cities = pd.read_csv(f'data_hidden/{name}.csv')
        population_cities.to_sql(name,engine,if_exists='replace', index= False)
        print(f'The {name} files has been uploaded to SQL successfully.')
    except:
        print(f'There was an error during your {name} update')


def upload_dataframe_with_name(df,name):
    ''' This function takes a dataframe and a name, 
        reads the dataframe and uploads it under the name we input'''
    try:
        df.to_sql(name,engine,if_exists='replace', index= False)
        print(f'The "{name}" file has been uploaded to SQL successfully.')
    except:
        print(f'There was an error during your "{name}" update')

def selecting_table(name):
    '''Receives a name of a table in SQL and returns that table'''

    return pd.read_sql_query(f'''select * from {name};''',engine)

def select_location_filters(dict_):

    '''Takes a dictionary with the params to filter the locations table in SQL'''

    category = "', '".join(dict_['category'])
    community = "', '".join(dict_['community'])
    rating = dict_['rating']
    
    
    return pd.read_sql_query(f'''select * 
                                from locations 
                                where community in ('{community}')
                                and category in ('{category}')
                                and Rating > {rating};''',engine)

def select_spot_filter(dict_):

    '''Takes a dictionary with the params to filter the spots table in SQL'''

    category = "', '".join(dict_['category'])
    community = "', '".join(dict_['community'])
    rating = dict_['rating']
    night_category = "', '".join(dict_['night_category'])
    return pd.read_sql_query(f'''select *
                            from spots 
                            where community in ('{community}')
                            and rating > {rating}
                            and night_category in ('{night_category}');''',engine)

def count_location (df_locations,df_spots):
    '''Takes two tables: Locations and spots,
    returns an updated spots table with an added column that
     contains the count of nearby interesting locations '''
    
    # Create the new column
    df_spots['count_locations_nearby']=0

    #Iterate through the spots dataframe and defining the coordinates for each row
    for item, row in df_spots.iterrows():
        df_spot_coord = (row['lat'],row['lon'])
        counter = 0
        
        #Iterate throught locations spots, calculating the distance between the spot coordinates and all locations.
        for item_2,row_2 in df_locations.iterrows():
            df_locations_coord = (row_2['lat'],row_2['lon'])
            dist= distance(df_spot_coord,df_locations_coord).km

            #Adding up a count if the distance is less than 30 km
            if dist < 30:
                counter += 1

        # Assing the total count to the spot row      
        df_spots.loc[item, 'count_locations_nearby']=counter
            
    return df_spots



def assign_candidates(df,dict_):

    # Create a new column to store the candidate values
    df.sort_values(['count_locations_nearby','rating'],ascending=False,inplace=True)

    #Considering everyone as a candidate
    df['candidate']=1
    
    # Iterate over each row in the spots df
    for i, row_i in df.iterrows():

        #Defining the coordinate for the row.
        coordinate_1 = (row_i['lat'],row_i['lon'])

        #Checking if it was assigned as not canidate in previous iterations.
        if df.loc[i,'candidate']==0:
            continue
        
        #Iterate again through the df to calculate distances between all other coordinates
        for j, row_j in df.iterrows():

            # Don't compare a location to itself
            if i == j:
                continue
                
            
                
            

            else:
                coordinate_2 = (row_j['lat'],row_j['lon'])
                # Calculate the distance between the two location
                dist = distance(coordinate_1, coordinate_2).km

                if dist < dict_['max_dist']:
                    # If the distance is less than 50km, set to not candidatet
                    df.loc[j,'candidate'] = 0

    #Defined canidates by distance, I remove all that doesn't have any interesting location nearby.               
    for i, row_i in df.iterrows():
        if row_i['count_locations_nearby']==0:
            df.loc[i,'candidate']=0
        
                    
    return df

def nearest_neighbor(coordinates):
    # Create a list to store the order of visited coordinates
    order = []
    
    # Choose the starting coordinate as the first coordinate in the list
    current_coord = coordinates[0]
    order.append(current_coord)
    
    # Create a set to store the remaining unvisited coordinates
    unvisited_coords = set(coordinates[1:])
    
    # While there are unvisited coordinates, choose the nearest neighbor and add it to the order
    while unvisited_coords:

        #Calculate the nearest coordinate between curent coordinate and all the unvisited ones.
        # I remove from unvisited coordinates those that I already chose.
        nearest_coord = min(unvisited_coords, key=lambda x: np.linalg.norm(np.array(x) - np.array(current_coord)))
        order.append(nearest_coord)
        current_coord = nearest_coord
        unvisited_coords.remove(nearest_coord)
    
    return order



def plot_route(dict_, df,key):

    '''Takes a dictionary, a dataframe, and a key
    it returns a folium featured group called 'Route!' with the route
    through all the night spots that suits best the filters chosen by the user'''

    # Initialize the Google Maps client
    gmaps = googlemaps.Client(key)

    
    # Create a list to store the locations in the order they will be visited
    locations = []

    #Define the starting point based on dictionary passed.
    start_point = (dict_['lat'],dict_['lng'])

    #Create a folium feature group for the Route.
    route_map  = folium.FeatureGroup(name='Route!')

    # Add the start point as the first location
    locations.append(start_point)

    # Define the colors that markers will have depending on category
    spots_colors = {
            'Parking lot day/night': 'gray',
            'nan': 'gray',
            'Camping': 'lightblue',
            'Picnic area': 'orange',
            'Free motorhome area': 'purple',
            'Daily parking lot only': 'lightblue',
            'Private car park for campers': 'darkgreen',
            'Paying motorhome area': 'darkpurple',
            'Surrounded by nature': 'green',
            'Rest area': 'blue',
            'Extra services': 'yellow',
            'Off road (4x4)': 'brown',
            'On the farm (farm)': 'green',
            'Service area without parking': 'blue',
            'Homestays accommodation': 'red'}

    # Iterate through the df to add each coordinate point to the map, with the category and rating as a pop up, following the color code.
    for item, row in df.iterrows():
        locations.append((row['lat'],row['lon']))
        marker = folium.Marker(location=(row['lat'],row['lon']),popup=f"ID: {item}   Rating: {row['rating']}", icon=folium.Icon(color=spots_colors[row['night_category']],prefix='fa',icon='car-side'))
        route_map.add_child(marker)
    
    # Call the function nearest_neighbor so all coordinates are in the proper order to visit.
    # Add the sart_point as the last coordinate, so the route starts and ends at the same place
    ordered_locations = nearest_neighbor(locations)
    ordered_locations.append(start_point)
    

    # Iterate through the coordinates and get the directions between each point and the next
    for i in range(len(ordered_locations)-1):
        directions_result = gmaps.directions(ordered_locations[i], ordered_locations[i+1], mode="driving",avoid='highways',region='ES')
        
        #Empty list where all the coordinates of the directions will be stored
        route = []
        
        #Each direction has many steps. Iterate through all of them and get the coordinates of the directions.
        for step in directions_result[0]['legs'][0]['steps']:
            coordinates= googlemaps.convert.decode_polyline(step['polyline']['points'])
            route.extend(coordinates)

        polyline=[]
        #Iterate through all coordinates and create a polyline to plot
        for coordinate in route:
            polyline.append((coordinate['lat'],coordinate['lng']))

        # Add the polyline to the Folium group
        route_map.add_child(folium.PolyLine(polyline, color='red').add_to(route_map))
    
        (print(directions_result))
    return route_map


def locations_group (df):
    '''This function takes a location dataframe 
        it returns a folium group with all the location spots'''

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
    for index, row in df.iterrows():
        locations_group.add_child(folium.Marker(
                location=[row['lat'], row['lon']],
                icon=folium.Icon(color=location_colors[row['category']],icon='circle'),
                popup=row['Name']))
    return locations_group


