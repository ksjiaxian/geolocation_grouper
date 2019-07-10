from math import radians, cos, sin, asin, sqrt



def haversine(lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles
        return c * r

def euclidean(lat, lng, lat0, lng0):
    deglen = 110.25
    x = float(lat) - float(lat0)
    y = (float(lng) - float(lng0))*cos(float(lat0))
    return deglen*sqrt(x*x + y*y)