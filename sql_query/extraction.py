import requests
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient
from geopy.geocoders import Nominatim


def get_park_spots(start_index):
    '''This functions extracts the html of all pages starting at indicated index.
        It will get the information for a 10000 places'''


    dict_response={}

    for i in range(start_index,start_index+10000):
        response = BeautifulSoup(requests.get(f'https://www.park4night.com/en/lieu/{i}/').content,'html.parser')
        address = response.find_all('span',attrs={'itemprop':'addressCountry'})
        if len(address)>0:
            country = response.find_all('span',attrs={'itemprop':'addressCountry'})[0].getText().strip()
            if country == 'Spain':

                dict_response[i] = response
    return dict_response



def extract_spot_info(dict_response):
    list_of_spots=[]
    for key, soup in dict_response.items():

        dict_park_to_add = {}

        #Extract the title
        try:
            title = soup.title.string.split(',')[0]
        except:
            title = 'Unknown'

        #Extract coordinates
        try:
            latitude = soup.find('span', {'itemprop': 'latitude'}).text.strip()
            longitude = soup.find('span', {'itemprop': 'longitude'}).text.strip()
        except:
            latitude = None
            longitude = None

        #extract the address
        try: 
            streetaddress = soup.find('span', {'itemprop':'streetAddress'}).text.strip()
            localityaddress = soup.find('span', {'itemprop':'addressLocality'}).text.strip()
        except:
            streetaddress = 'Unknown'
            localityaddress =''

        # extract the number of places for that spot
        try:
            num_places = int(soup.find('td', text='Number of places').find_next_sibling('td').text)
        except:
            num_places = None

        #exctract the height limit
        try:    
            limited_height = float(soup.find('td', text='Limited height:').find_next_sibling('td').text.split(' ')[0])
        except:
            limited_height = None
        
        #extract the number of comments

        number_of_ratings = soup.find('div', {'class': 'grid_11', 'style': 'margin-top:10px;margin-bottom:10px;'}).find('div', {'class': 'texte_3'}).text.strip().split()[0]

        #extract the rating

        rating = float(soup.find('div', {'class': 'rating_fg'})['style'].split('width:')[1].split('px')[0])
            
        #exctract the url
        url = f'https://www.park4night.com/en/lieu/{key}/'

        dict_park_to_add['category']=title
        dict_park_to_add['coordinates']=[latitude,longitude]
        dict_park_to_add['address']=streetaddress +', '+ localityaddress
        dict_park_to_add['num_places']=num_places
        dict_park_to_add['limited_height']=limited_height
        dict_park_to_add['rating']= rating/100*5
        dict_park_to_add['number_ratings']=number_of_ratings
        dict_park_to_add['url']=url

        list_of_spots.append(dict_park_to_add)
        df_spots = pd.DataFrame(list_of_spots)
        #df_spots.to_csv('data/park_spots_1.csv')


def get_community_sphere(lat, lon):

    client = MongoClient("localhost:27017")
    db = client['camper']
    geography = db.get_collection('spain_geography')
    location = [round(lon, 4), round(lat, 4)]
    point = {
        "type": "Point",
        "coordinates": location
    }

    result=  geography.find_one(
        {
            "geometry": {
                "$nearSphere": {
                    "$geometry": point,
                    "$maxDistance": 20000
                }
            }
        },
        projection={"properties.name": 1, "_id": 0})
    if result==None:
        return 'Not found'
    else:
        return result['properties']['name']