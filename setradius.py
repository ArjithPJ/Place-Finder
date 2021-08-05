import requests
import json
import time
import googlemaps
class GooglePlaces(object):
    def __init__(self, apiKey):
        super(GooglePlaces, self).__init__()
        self.apiKey = apiKey

    def search_places_by_coordinate(self, location, radius, types):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        places = []
        params = {
            'location': location,
            'radius': radius,
            'types': types,
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        results =  json.loads(res.content)
        places.extend(results['results'])
        time.sleep(2)
        while "next_page_token" in results:
            params['pagetoken'] = results['next_page_token'],
            res = requests.get(endpoint_url, params = params)
            results = json.loads(res.content)
            places.extend(results['results'])
            time.sleep(2)
        return places

    def get_place_details(self, place_id, fields):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'placeid': place_id,
            'fields': ",".join(fields),
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        place_details =  json.loads(res.content)
        return place_details
if __name__ == '__main__':
    classLabels=[]
    file_name='labels.txt'
    with open(file_name,'rt') as fpt:
        classLabels=fpt.read().strip('\n').split('\n')
    print(classLabels)
    dict={}
    for i in range(len(classLabels)):
        dict[str(i+1)]=classLabels[i]
    api = GooglePlaces("AIzaSyAQ7AA9K0Rw2yr8T_i7GeQZ3IUGG8EYlnA")
    place=input("Enter the address")
    map_client = googlemaps.Client("AIzaSyAQ7AA9K0Rw2yr8T_i7GeQZ3IUGG8EYlnA")
    geocode=map_client.geocode(address=place)[0]
    print(geocode['geometry']['location'])
    lat=str(geocode['geometry']['location']['lat'])
    lng=str(geocode['geometry']['location']['lng'])
    loc=lat+","+lng
    print(loc)
    print(dict)
    choice=str(input("Enter the choice"))
#"40.819057,-73.914048"
    radius=str(input("Enter the radius"))
    places = api.search_places_by_coordinate(loc, radius, dict[choice])
    fields = ['name', 'formatted_address', 'international_phone_number', 'website', 'rating', 'review']
    for place in places:
        details = api.get_place_details(place['place_id'], fields)
        try:
            website = details['result']['website']
        except KeyError:
            website = ""
 
        try:
            name = details['result']['name']
        except KeyError:
            name = ""
 
        try:
            address = details['result']['formatted_address']
        except KeyError:
            address = ""
 
        try:
            phone_number = details['result']['international_phone_number']
        except KeyError:
            phone_number = ""
 
        try:
            reviews = details['result']['reviews']
        except KeyError:
            reviews = []
        print("===================PLACE===================")
        print("Name:", name)
        print("Website:", website)
        print("Address:", address)
        print("Phone Number", phone_number)
        print("==================REWIEVS==================")
        for review in reviews:
            author_name = review['author_name']
            rating = review['rating']
            text = review['text']
            time = review['relative_time_description']
            profile_photo = review['profile_photo_url']
            print("Author Name:", author_name)
            print("Rating:", rating)
            print("Text:", text)
            print("Time:", time)
            print("Profile photo:", profile_photo)
            print("-----------------------------------------")

