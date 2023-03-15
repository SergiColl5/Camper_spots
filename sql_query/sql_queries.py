
import sqlalchemy as alch
import os 
from dotenv import load_dotenv
import pandas as pd
from geopy.distance import distance

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

#Uploading to sql any csv population dataset
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
    return pd.read_sql_query(f'''select * from {name};''',engine)

def select_location_filters(dict_):
    category = "', '".join(dict_['category'])
    community = "', '".join(dict_['community'])
    rating = dict_['rating']

    night_category = "', '".join(dict_['night_category'])
    
    return pd.read_sql_query(f'''select * 
                                from locations 
                                where community in ('{community}')
                                and category in ('{category}')
                                and Rating > {rating};''',engine)

def select_spot_filter(dict_):
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
    df_spots['count_locations_nearby']=0
    for item, row in df_spots.iterrows():
        df_spot_coord = (row['lat'],row['lon'])
        counter = 0
        
        for item_2,row_2 in df_locations.iterrows():
            df_locations_coord = (row_2['lat'],row_2['lon'])
            dist= distance(df_spot_coord,df_locations_coord)
            if dist < 30:
                counter += 1
        df_spots.loc[item, 'count_locations_nearby']=counter
            
    return df_spots



def assign_candidates(df,dict_):
    # Create a new column to store the candidate values
    df.sort_values(['count_locations_nearby','rating'],ascending=False,inplace=True)

    df['candidate']=1
    
    # Iterate over each row in the DataFrame
    for i, row_i in df.iterrows():
        coordinate_1 = (row_i['lat'],row_i['lon'])
        if df.loc[i,'candidate']==0:
            continue
    
        for j, row_j in df.iterrows():
            if i == j:
                continue
                
            
                # Don't compare a location to itself
            

            else:
                coordinate_2 = (row_j['lat'],row_j['lon'])
                # Calculate the distance between the two location
                dist = distance(coordinate_1, coordinate_2).km

                if dist < dict_['max_dist']:
                    # If the distance is less than 50km, 
                    df.loc[j,'candidate'] = 0
    for i, row_i in df.iterrows():
        if row_i['count_locations_nearby']==0:
            df.loc[i,'candidate']=0
        
                    
    return df