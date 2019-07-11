import formulas
import csv
import requests
import Inventor
import Group
from fastnumbers import fast_real
from unidecode import unidecode

def get_focal_point(location_list, r1):
    #list of location set around every point in tuple form (location, set)
    local_list_list =[]
    # iterate through location_list to create sets for each location
    for location in location_list:

        lat1 = location.get_lat()
        lon1 = location.get_lng()
        local_list = []
        for other_location in location_list:
            lat2 = other_location.get_lat()
            lon2 = other_location.get_lng()
            try:  
                dist = formulas.haversine(lat1, lon1, lat2, lon2)
                if dist <= float(r1):
                    local_list.append(other_location)
            except:
                pass
            
        local_list_list.append((location, local_list))
    
    #local set around focal point of locations in (address, lat, long)
    local_list = []
    # focal point
    focal_point = None
    #iterate through dictionary to get largest set and focal point
    for loc, self_list in local_list_list:
        if (len(self_list) > len(local_list)):
            local_list = self_list
            focal_point = loc
    
    return (focal_point, local_list)

def create_remote_list(focal_point, location_list, r2):
    #remote list around focal point of locations in (address, lat, long)
    remote_list =[]
    lat1 = focal_point.get_lat()
    lon1 = focal_point.get_lng()
    for loc in location_list:
        lat2 = loc.get_lat()
        lon2 = loc.get_lng()
        try:
            dist = formulas.haversine(lat1, lon1, lat2, lon2)
            if dist > float(r2):
                remote_list.append(loc)
        except:
            pass
    return remote_list

def generate_geo_relationship(country, other_center):
   
    #get the country data
    country2 = other_center.get_country()
    state = other_center.get_state()   
    if country2 != 'US':
        other_center.set_state("N/A")
    elif country2 == 'US':
        if state == '':
            coord2 = str(other_center.get_lat()) +","+ str(other_center.get_lng())
            response2 = requests.get("http://dev.virtualearth.net/REST/v1/Locations/" + coord2,
                        params={"key":formulas.get_api_key(),
                                })
            data2 = response2.json()
            try:
                state = str(data2['resourceSets'][0]['resources'][0]['address']['adminDistrict'])
                other_center.set_state(state)
            except:
                other_center.set_state("N/A")
    else:
        coord2 = str(other_center.get_lat()) +","+ str(other_center.get_lng())
        response2 = requests.get("http://dev.virtualearth.net/REST/v1/Locations/" + coord2,
                    params={"key":formulas.get_api_key(),
                            })
        data2 = response2.json()
        if state == '':
            try:
                country2 = str(data2['resourceSets'][0]['resources'][0]['address']['countryRegion'])
                if country2 == 'US':
                    state = str(data2['resourceSets'][0]['resources'][0]['address']['adminDistrict'])
                    other_center.set_state(state)
                else:
                    other_center.set_state("N/A")
            except:
                country2 = "N/A"
                other_center.set_state("N/A")
        else:
            try:
                country2 = str(data2['resourceSets'][0]['resources'][0]['address']['countryRegion'])
            except:
                country2 = "N/A"
      
    if country == country2:
        if country == "N/A":
            return (country, country2, "N/A")
        else: 
            return (country, country2, "domestic")
    else:
        return (country, country2, "cross border")

    
def output_each_patent(ungrouped, company, id, r1, r2):
    #get the local locations
    (local_center, local_set) = get_focal_point(ungrouped, r1)
    #get the remote locations
    remote_set = create_remote_list(local_center, ungrouped, r2)
    #find the locations that are not local and not remote
    inbetween = []
    for loc in ungrouped:
        if loc not in remote_set and not loc in local_set:
            inbetween.append(loc)
            
    #row to write
    row = []
    row.append(company)
    row.append(id)
    row.append(len(ungrouped))
    row.append(len(local_set))
    row.append(len(remote_set))
    
        
    #get the country data
    country = local_center.get_country()
    state = local_center.get_state()   
    if country != 'US':
        other_center.set_state("N/A")
    elif country == 'US':
        if state == '':
            coord2 = str(other_center.get_lat()) +","+ str(other_center.get_lng())
            response2 = requests.get("http://dev.virtualearth.net/REST/v1/Locations/" + coord2,
                        params={"key":formulas.get_api_key(),
                                })
            data2 = response2.json()
            try:
                state = str(data2['resourceSets'][0]['resources'][0]['address']['adminDistrict'])
                other_center.set_state(state)
            except:
                other_center.set_state("N/A")
    else:
        coord2 = str(other_center.get_lat()) +","+ str(other_center.get_lng())
        response2 = requests.get("http://dev.virtualearth.net/REST/v1/Locations/" + coord2,
                    params={"key":formulas.get_api_key(),
                            })
        data2 = response2.json()
        if state == '':
            try:
                country = str(data2['resourceSets'][0]['resources'][0]['address']['countryRegion'])
                if country == 'US':
                    state = str(data2['resourceSets'][0]['resources'][0]['address']['adminDistrict'])
                    other_center.set_state(state)
                else:
                    other_center.set_state("N/A")
            except:
                country = "N/A"
                other_center.set_state("N/A")
        else:
            try:
                country = str(data2['resourceSets'][0]['resources'][0]['address']['countryRegion'])
            except:
                country = "N/A"
           
    
    
    
    #list of sets of remote groups
    remote_groups = []
    
    while len(remote_set) > 0:
        #get largest remote group, add to remote groups and remove from set of ungrouped remotes
        (remote_center, remote_group) = get_focal_point(remote_set, r1)
        remote_groups.append((remote_center, remote_group))
        for loc in remote_group:
            remote_set.remove(loc)
        
    row.append(1 + len(remote_groups)) # number of clusters
    row.append(r1) # local radius
    row.append(r2) # remote radius
    with open('outputs/groupings.tsv', 'a', newline="\n", encoding='latin-1') as out_file: 
        csv_writer = csv.writer(out_file, delimiter='\t')
        
        # convert local_set from a set of tuples to a list of strings
        local_set_string = []
        for loc in local_set:
            coord = '(' + str(loc.get_lat()) + ' ' + str(loc.get_lng()) +')'
            local_set_string.append(coord)
        # dict for local_cluster
        local_cluster_dict = {'number_of_inventors_in_cluster': len(local_set),
                              'locations': '; '.join(local_set_string),
                              'center_lat': local_center.get_lat(),
                              'center_lng': local_center.get_lng(),
                              'state': state,
                              'country': country,
                              'geographical_relationship': 'domestic',
                              'haversine_distance_to_local': 'N/A'}
        row.append(local_cluster_dict)
        
        # convert inbetween set from a set of tuples to a list of strings
        inbetween_set_string = []
        for loc in inbetween:
            coord = '(' + str(loc.get_lat()) + ' ' + str(loc.get_lng()) +')'
            inbetween_set_string.append(coord)
        
        if len(inbetween_set_string) == 0:
            row.append('N/A')
        else:   
            # dict for nonlocal_cluster
            nonlocal_cluster_dict = {'number_of_inventors_in_cluster': len(inbetween),
                                  'locations': '; '.join(inbetween_set_string),
                                  'center_lat': 'N/A',
                                  'center_lng': 'N/A',
                                  'state': 'N/A',
                                  'country': 'N/A',
                                  'geographical_relationship': 'N/A',
                                  'haversine_distance_to_local': 'N/A'}
            row.append(nonlocal_cluster_dict)
        
        
        # sort remote groups by distance away from local focal point
        remote_group_list = []
        for remote_group in remote_groups:
            (loc, group) = remote_group
            size = len(group)
            remote_group_list.append((loc, group, size))
            remote_group_list.sort(key=lambda tup: tup[2])  # sorts in place
            remote_group_list.reverse()
        
        write_remote_cluster = []
        for remote_group in remote_group_list:
            (center, group, size) = remote_group
            # convert remote_group from a set of tuples to a list of strings
            remote_group_string = []
            for loc in group:
                coord = '(' + str(loc.get_lat()) + ' ' + str(loc.get_lng())+')'
                remote_group_string.append(coord)
            (c1, c2, rel) = generate_geo_relationship(country, center)
            # dict for remote_cluster
            remote_cluster_dict = {'number_of_inventors_in_cluster': len(group),
                                  'locations': '; '.join(remote_group_string),
                                  'center_lat': center.get_lat(),
                                  'center_lng': center.get_lng(),
                                  'state': center.get_state(),
                                  'country': c2,
                                  'geographical_relationship': rel,
                                  'haversine_distance_to_local': formulas.haversine(local_center.get_lat(), local_center.get_lng(), center.get_lat(), center.get_lng())}
            write_remote_cluster.append(remote_cluster_dict)
        if (len(write_remote_cluster) == 0):
            row.append('N/A')
        else:
            row.append(write_remote_cluster)
        
        csv_writer.writerow(row)
        
if __name__ == '__main__':
    item_id = 0
    # write header
    with open('outputs/groupings.tsv', 'w', newline="\n", encoding='utf-8-sig') as out_file: 
        csv_writer = csv.writer(out_file, delimiter='\t')
        header = ["company", "id", "number_of_inventors", "number_of_local_inventors", "number_of_remote_inventors", "number_of_clusters (local+remote)", "radius_local", 
                  "radius_remote", "HQ", "nonlocal_cluster", "remote_groups"]
        csv_writer.writerow(header)
    # process radii
    r1 = 0
    r2 = 0
    
    with open('inputs/arguments_m1.csv', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        
        #create the list of ungrouped addresses
        for row in reader:
            r1 = row['r1']
            r2 = row['r2']
    
    total_length = 0     
    # process patent records

    with open('inputs/patent_list_100company.csv', encoding='latin-1') as csvfile:
        reader_count = csv.DictReader(csvfile, delimiter=',')
        total_length =  sum(1 for row in reader_count)
    with open('inputs/patent_list_100company.csv', encoding='latin-1') as csvfile:

        reader = csv.DictReader(csvfile, delimiter=',')
        
        print(total_length)
        id_dict = {}
        
        #have a dictionary map ids to companies
        id_to_company = {}
        
        for row in reader:
            print(reader.line_num)
            id = row['id']
            company = row['acquiree_name']
            
            id_to_company[id] = company
            
            lat = fast_real(row['inventor_add_lat'])
            lng = fast_real(row['inventor_add_lon'])
            inventor_id = row['inventor_id']
            try:
                city = row['inventor_add_city']
                if city == 'NULL':
                    city = ''
            except:
                city = ''
            try:
                state = row['inventor_add_state']
                if state == 'NULL':
                    state = ''
            except:
                state = ''
            try:
                country = row['inventor_add_country']
                if country == 'NULL':
                    country = ''
            except:
                country = ''
                
            #make sure that we do not create an inventor object for rows that have no location information
            if city == '' and state == '' and lat == '' and lng == '' and country == '':
                continue
            
            new_inventor = Inventor.inventor(id, company, inventor_id, lat, lng, city, state, country)
            
            #if the inventor class was not able to find lat and lng for the inventor, then don't add inventor to set of data
            if new_inventor.get_lat() == 404 or new_inventor.get_lng() == 404:
                continue
            
            if id in id_dict:
                inventor_list = id_dict[id]
                inventor_list.append(new_inventor)
                id_dict[id] = inventor_list
            else:
                inventor_list = [new_inventor]
                id_dict[id] = inventor_list
            
        print("begin processing data!")
        print(len(id_dict))
        for id, ungrouped in id_dict.items():
            company = id_to_company[id]
            #using a try catch in case of any company names that use special characters
            try:
                print(id)
                print(company)
                output_each_patent(ungrouped, company, id, r1, r2)
            except:
                company = unidecode(company)
                print(id)
                print(company)
                output_each_patent(ungrouped, company, id, r1, r2)
                