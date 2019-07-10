from fastnumbers import fast_real
import requests
from unidecode import unidecode

class inventor:
    def __init__(self, patent_id, company, inventor_id, lat, lng, city, state, country):
        self.patent_id = patent_id
        self.inventor_id = inventor_id
        self.lat = fast_real(lat)
        self.lng = fast_real(lng)
        self.company = company
        
        if self.lat == '' or self.lng == '':
            try:
                print(unidecode(city))
                print(unidecode(state))
                response = requests.get("http://dev.virtualearth.net/REST/v1/Locations/" + city + ' ' + state + ' ' + country,
                                params={"include":"queryParse",
                                "key":formulas.get_api_key()})
                data = response.json()
                self.lat = data['resourceSets'][0]['resources'][0]['point']['coordinates'][0]
                self.lng = data['resourceSets'][0]['resources'][0]['point']['coordinates'][1]
            
            except:
                self.lat = 404
                self.lng = 404
        self.city = city
        self.state = state
        self.country = country
        
    def get_company(self):
        return self.company
    
    def get_patent_id(self):
        return self.patent_id
    
    def get_inventor_id(self):
        return self.inventor_id
    
    def get_lat(self):
        return self.lat
    
    def get_lng(self):
        return self.lng
    
    def get_city(self):
        return self.city
    
    def get_state(self):
        return self.state
    
    def set_state(self, state):
        self.state = state
    
    def get_country(self):
        return self.country