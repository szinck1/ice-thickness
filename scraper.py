from folium.plugins import MarkerCluster
import folium
import requests
import re


import geopy
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup


def getData():


    
    URL = 'https://www.halifax.ca/recreation/programs-activities/skating/ice-thickness'

    try:
        r = requests.get(URL)
    except requests.exceptions.RequestException as e: 
        raise SystemExit(e)
    soup = BeautifulSoup(r.content, 'lxml')

    table = soup.find("table")

    ice_dict = {}
    for tr in table.findAll('tr')[1:]:

        col = tr.findAll('td')

        name = str(col[0].string)
        location = str(col[1].string)
        centimeters = str(col[2].string)
        comments = str(col[3].string)
        date = str(col[4].string)

        ice_dict[name] = {}
        ice_dict[name]['Location'] = location
        ice_dict[name]['Comments'] = comments
        ice_dict[name]['Date'] = date
        ice_dict[name]['Centimeters'] = centimeters

    return ice_dict


def geoCoder(location):

    locator = Nominatim(user_agent="nslakes.netlify.com/steve@zinck.ca")

    geolocation = locator.geocode(location)

    return [geolocation.latitude, geolocation.longitude]


def createMapMarker(ice_dict):

    feature_group = folium.FeatureGroup("Locations")
    my_map = folium.Map(location=[44.651070, -63.582687], zoom_start=10)

    for lake_name in ice_dict:
        try:
            
            lake_comments = ice_dict[lake_name]['Comments']
            lake_centi = ice_dict[lake_name]['Centimeters']
            lake_date = ice_dict[lake_name]['Date']
            lake_name = re.sub(r'\([^)]*\)', '', lake_name).strip()
            lake = geoCoder(lake_name)

            html = f'''<h4>Name:</h4> {lake_name} <br />\
            <h4>Centimeters: </h4> {lake_centi} <br />\
            <h4>Comments: </h4> {lake_comments} <br />\
            <h4>Date: </h4> {lake_date} <br />\
            '''

            feature_group.add_child(folium.Marker(lake, popup=html))

        except Exception as e:
            print(e)
            print("Error with: " + lake_name)
            continue
    my_map.add_child(feature_group)
    my_map.save("docs/index.html")

createMapMarker(getData())





