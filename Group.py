class group:
    def __init__(self, company, company_id, group_id, size, lat, lng, state, country, locations):
        self.group_id = group_id
        self.size = size
        self.lat = lat
        self.lng = lng
        self.state = state
        self.country = country
        self.company = company
        self.company_id = company_id
        self.locations = locations
        
        
    def get_company(self):
        return self.company
    
    def get_company_id(self):
        return self.company_id
        
    def get_group_id(self):
        return self.group_id
    
    def get_size(self):
        return self.size
    
    def get_lat(self):
        return self.lat
    
    def get_lng(self):
        return self.lng
    
    def get_country(self):
        return self.country
    
    def get_state(self):
        return self.state
    
    def get_locations(self):
        return self.locations
    
    def __len__(self):
        return self.size
    
    def __lt__ (self, other):
        #a group is less than another if there are less components in that group
        if len(self) == len(other):
            return len(self) < len(other)
        return len(self) < len(other)

    def __gt__ (self, other):
        return other.__lt__(self)

    def __eq__ (self, other):
        #two groups are the same if their ids are the same
        return self.group_id == other.group_id

    def __ne__ (self, other):
        #two groups are not the same if their ids are not the same
        return not self.__eq__(other)