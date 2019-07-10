import Group
import Inventor
import requests
import csv
import formulas
import math
from fastnumbers import fast_real
                
def generate_geo_relationship(country, other_center):
   
    #get the country data
    country2 = other_center.get_country()
    if country2 == '':
        #this is for using the bing reverse geocode api
        coord2 = str(other_center.get_lat()) +","+ str(other_center.get_lng())
        response2 = requests.get("http://dev.virtualearth.net/REST/v1/Locations/" + coord2,
                    params={"key":formulas.get_api_key(),
                            })
        data2 = response2.json()
        #get the country data
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
    
def output_each_patent(ungrouped, company, company_id, base_radius, coverage_percentage):
    print(company)
    print(len(ungrouped))
    #get the clusters centered around the headquarters
    (hq, hq_set) = get_focal_point(ungrouped, base_radius)
    
    #get the remote locations - assume that every cluster not in the headquarters's radius is a remote location
    remote_set = [i for i in ungrouped if not i in hq_set]
            
    #row to write
    row = [company, company_id, len(hq_set), len(remote_set), len(hq_set) + len(remote_set), str(base_radius), str(coverage_percentage)]
    
    # get local country and state
    country = hq.get_country()
    state = hq.get_state()    
    if country == '' or state == '':
        # get local country
        coord1 = str(local_center.get_lat()) +","+ str(local_center.get_lng())
        response1 = requests.get("http://dev.virtualearth.net/REST/v1/Locations/" + coord1,
                    params={"key":formulas.get_api_key(),
                            })
        data1 = response1.json()
        
        if country == '':
            #get the country data
            try:
                country = str(data1['resourceSets'][0]['resources'][0]['address']['countryRegion'])
            except:
                country = "N/A"
        
        if state == '':
            #get the state data
            try:
                state = str(data1['resourceSets'][0]['resources'][0]['address']['adminDistrict'])
            except:
                state = "N/A"
    
    #list of sets of remote groups
    remote_groups = []
    
    while len(remote_set) > 0:
        #print(len(remote_set))
        #get largest remote group, add to remote groups and remove from set of ungrouped remotes
        (remote_center, remote_group) = get_focal_point(remote_set, base_radius)
        print(len(remote_set))
        remote_groups.append((remote_center, remote_group))
        for loc in remote_group:
            remote_set.remove(loc)
            
    with open('outputs/grouped_groups.tsv', 'a', newline="\n", encoding='utf-8-sig') as out_file: 
        csv_writer = csv.writer(out_file, delimiter='\t')
        
        # convert local_set from a set of tuples to a list of strings
        local_set_string = []
        for loc in hq_set:
            coord = loc.get_group_id()
            local_set_string.append(coord)
        # dict for local_cluster
        local_cluster_dict = {'number_of_patent_groups_in_cluster': len(local_set_string),
                              'locations_id': '; '.join(local_set_string),
                              'center_lat': hq.get_lat(),
                              'center_lng': hq.get_lng(),
                              'state': state,
                              'country': country,
                              'geographical_relationship': 'domestic',
                              'haversine_distance_to_local': 'N/A'}
        row.append(local_cluster_dict)
        
        
        
        # sort remote groups by distance away from local focal point
        remote_group_list = []
        for remote_group in remote_groups:
            (loc, group) = remote_group
            size = len(group)
            remote_group_list.append((loc, group, size))
            remote_group_list.sort(key=lambda tup: tup[2])  # sorts in place
            remote_group_list.reverse()
            
        #this is the number of remote groups of clusters
        num_of_remote_groups = len(remote_group_list)
        total_num_of_groups = num_of_remote_groups + 1
        
        #add that information to the row
        row.insert(5, total_num_of_groups)
        row.insert(6, num_of_remote_groups)
        
        write_remote_cluster = []
        for remote_group in remote_group_list:
            (center, group, size) = remote_group
            # convert remote_group from a set of tuples to a list of strings
            remote_group_string = []
            for loc in group:
                coord = loc.get_group_id()
                remote_group_string.append(coord)
            (c1, c2, rel) = generate_geo_relationship(country, center)
            # dict for remote_cluster
            remote_cluster_dict = {'number_of_patent_groups_in_cluster': len(group),
                                  'locations_id': '; '.join(remote_group_string),
                                  'center_lat': center.get_lat(),
                                  'center_lng': center.get_lng(),
                                  'state': center.get_state(),
                                  'country': c2,
                                  'geographical_relationship:': rel,
                                  'haversine_distance_to_local': formulas.haversine(hq.get_lat(), hq.get_lng(), center.get_lat(), center.get_lng())}
            write_remote_cluster.append(remote_cluster_dict)
        if (len(write_remote_cluster) == 0):
            row.append('N/A')
        else:
            row.append(write_remote_cluster)
        
        # percentage coverage
        # first create a list of tuples (distance, coord)
        loc_list_tuples = []
        for group in hq_set:
            #list of tuples
            location_list = group.get_locations()
            for coord in location_list:
                dist = formulas.haversine(hq.get_lat(), hq.get_lng(), coord[0], coord[1])
                loc_list_tuples.append((dist, coord))
        loc_list_tuples.sort(key=lambda tup: tup[0])  # sorts in place
        num_to_include = math.ceil(float(percent_coverage) * len(loc_list_tuples))
        local_inventors = []
        for coord in loc_list_tuples[:num_to_include]:
            local_inventors.append(coord[1])
        radius_for_percent =  loc_list_tuples[num_to_include - 1][0]
        # dict for local inventors
        local_inventor_dict = {'radius': radius_for_percent,
                               'count': num_to_include,
                           'locations': local_inventors
            }
        row.append(local_inventor_dict) 
        csv_writer.writerow(row)
        
def get_focal_point(location_list, r_base):
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
                if dist <= float(r_base):
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


#main method
if __name__ == '__main__':    
    
    #write header
    with open('outputs/grouped_groups.tsv', 'w', newline="\n", encoding='utf-8-sig') as out_file: 
        csv_writer = csv.writer(out_file, delimiter='\t')
        header = ["company", "id", "num_of_clusters_in_HQ_region", "num_of_clusters_in_remote_regions", "total_number_of_groups (HQ+remote)", "num_of_R&D_centers", "num_of_remote_R&D_centers", "radius_base", 
                  "coverage_percentage", "HQ", "remote_groups", "inventors_in_local"]
        csv_writer.writerow(header)
        
    #create a dictionary that maps company to a list of the company patent groupings
    company_groups = {}
    
    #create a dictionary that maps company_id to company
    id_to_company = {}

    #read in the data from the previous module
    with open('outputs/cluster_list.tsv', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        
        #go through each row in the reader and turn each group row into a group object
        for row in reader:
            group_id = row["cluster_id"]
            size = row['number_of_inventors']
            lat = row['center_lat']
            lng = row['center_lng']
            
            if lat == 'N/A' or lng == 'N/A':
                continue
                
            state = row['state']
            country = row['country']
            company = row['company']
            company_id = row['company_id']
            
            # split locations into list of tuples
            location_list = []
            locations = row['locations']
            loc_list = locations.split("; ")
            for s in loc_list:
                old_coord = s[s.find("(")+1:s.find(")")]
                coord = old_coord.split(" ")
                location_list.append((fast_real(coord[0]), fast_real(coord[1])))
            
            id_to_company[company_id] = company
            
            if company_id in company_groups:
                company_groups[company_id].append(Group.group(company, company_id, group_id, size, lat, lng, state, country, location_list))
            else :
                company_groups[company_id] = []
                company_groups[company_id].append(Group.group(company, company_id, group_id, size, lat, lng, state, country, location_list))
                
            
    print('total number of companies: ' + str(len(company_groups)))
    
    #read in the arguments for percentage and base radius
    r_base = 0
    percent_coverage = 0.0
    
    with open('inputs/arguments_m2.csv', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        
        #create the list of ungrouped addresses
        for row in reader:
            percent_coverage = row['percent_coverage']
            r_base = row['r_base']
            
    
    print('base radius: ' + str(r_base))
    print('percent coverage: ' + str(percent_coverage))
    
    #go through every company and group all the patent groups
    for company_id, group_list in company_groups.items():
        output_each_patent(group_list, id_to_company[company_id], company_id, r_base, percent_coverage)
    