import csv
import ast
import random
import math
import statistics

#this method compares methods 1 and 2 of clustering by pairing the clusters and
#calculating the average distance between the centers of the clusters for each
#of a number of randomly chosen companies

num_of_companies = 100

#if is assumed that the two files have the same companies
filename_1 = 'outputs/groupings.tsv'
filename_2 = 'outputs/grouped_groups.tsv'

#this method returns the number of rows in a csv or tsv
def get_number_of_rows(filename):
    with open(filename, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        
        cnt = 0
        
        for row in reader:
            cnt += 1
            
        return cnt
    
#this method returns a set of clusters of a particular file - returns none if 
#an error is thrown
# these sets are in the form of a dictionary from the company to the set
#companies is a set of companies names to get the clusters of
def get_cluster_set(filename, companies):
    company_to_clusterset = {}
    #read in the data from the previous module
    with open(filename, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        
        for row in reader:
            curr_company = row['id']
            if curr_company in companies:
                # list of clusters in tuple form with local cluster at index 0
                cluster_list = [] 
                #get the hq cluster
                local_cluster_str = row['HQ']
                local_cluster_dict = ast.literal_eval(local_cluster_str)
                local_cluster_lat = local_cluster_dict['center_lat']
                local_cluster_lng = local_cluster_dict['center_lng']
                cluster_list.append((local_cluster_lat, local_cluster_lng))
                #get the remote clusters
                remote_cluster_list_str = row['remote_groups']
                remote_cluster_dict_list = ast.literal_eval(remote_cluster_list_str)
                for remote_dict in remote_cluster_dict_list:
                    remote_lat = remote_dict['center_lat']
                    remote_lng = remote_dict['center_lng']
                    cluster_list.append((remote_lat, remote_lng))
                company_to_clusterset[curr_company] = cluster_list
            
            
    return company_to_clusterset
        
        
#this method will pair the clusters - a given cluster may be paired with more than one cluster
#returns a list of tuples, where each element in the tuple is a coordinate pair
def pair_clusters(list_one, list_two): 
    bigger_list = list_one
    smaller_list = list_two
    if (len(list_two) > len(list_one)):
        bigger_list = list_two
        smaller_list = list_one
    
    # keep track of matched coords in smaller list
    smaller_list_matched = set()
    # returned list of tuples in the format of [((lat, lng), (lat, lng), dist)]
    ret = []
    for (lat1, lng1) in bigger_list:
        closest_pair = None
        closest_dist = math.inf
        for (lat2, lng2) in smaller_list:
            dist = formulas.haversine(lat1, lng1, lat2, lng2)
            if (dist < closest_dist):
                closest_pair = (lat2, lng2)
                closest_dist = dist
        smaller_list_matched.add(closes_pair)
        ret.append((lat1, lng1), (lat2, lng2), closest_dist)
        
    if (len(smaller_list_matched) != len(smaller_list)):
        print("problem with matching")
    else:
        return ret
   
    
if __name__ == '__main__':
    #write header
    with open('outputs/method_comparison.tsv', 'w', newline="\n", encoding='utf-8-sig') as out_file: 
        csv_writer = csv.writer(out_file, delimiter='\t')
        header = ["company", "id", "M1_num_clusters", "M2_num_clusters", "M1_num_remote_clusters", "M2_num_remote_clusters", 
                  "M1_HQ", "M2_HQ", "HQ1-HQ2_distance", "average_cluster_distance", "median_cluster_distance", "sd", "pairs"]
        csv_writer.writerow(header)
        
    print('Randomly choosing ' + str(num_of_companies) + ' companies')
    
    #set of company ids
    companies = set()
    company_id_to_name = {}
    
    #dictionarie
    method_one_hq = {}
    
    
    with open(filename_1, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        
        for row in reader:
            companies.add((row['id']))
            company_id_to_name[row['id']] = row['company']
            
    sample = random.sample(companies, num_of_companies)
    
    print(len(sample))
    for co in sample:
        print(co)
    
    #get cluster information about the companies
    method_one_clusters = get_cluster_set(filename_1, companies)
    method_two_clusters = get_cluster_set(filename_2, companies)
    
    #get headquarters information about the companies
    method_one_hq = get_headquarters_info(filename_1, companies)
    method_two_hq = get_headquarters_info(filename_2, companies)
    
    #turn these two dictionaries into one dictionary with two sets per company key
    company_cluster_lists = {}
    for company_id in companies:
        list_one = method_one_clusters[company_id]
        list_two = method_two_clusters[company_id]
        company_cluster_lists[company] = (list_one, list_two)
        
    #for each company, pair the corresponding clusters and store them as a set of tuples of coordinates
    company_paired_clusters = {}
    for company, (list_one, list_two) in company_cluster_sets.items():
        company_paired_clusters[company] = pair_clusters(list_one, list_two)
        
    #write the body of the data
    with open('outputs/method_comparison.tsv', 'n', newline="\n", encoding='utf-8-sig') as out_file: 
        csv_writer = csv.writer(out_file, delimiter='\t')
        
        for company_id, cluster_pair_set in company_paired_cluster.items():
            
            row = [str(company_id_to_name[company_id]), str(company_id), len(method_one_clusters[company_id]),
                   len(method_two_clusters[company_id]), len(method_one_clusters[company_id]) - 1,
                   len(method_two_clusters[company_id])]
            
            # get the head quarters information from m1 and m2
            m1_hq_state = method_one_hq[company_id]['state']
            m1_hq_country = method_one_hq[company_id]['country']
            m1_hq_coordinates = "(" + str(method_one_hq[company_id]['center_lat']) + ", " + str(method_one_hq[company_id]['center_lng'] + ")")
            m1_hq_fulllocation = ''
            if m1_hq_state == 'N/A' and mq_h1_country == 'N/A':
                m1_hq_fulllocation == m1_hq_coordinates
            elif m1_hq_state == 'N/A' and not mq_h1_country == 'N/A':
                m1_hq_fulllocation == m1_hq_country + "; " + m1_hq_coordinates
            elif not m1_hq_state == 'N/A' and mq_h1_country == 'N/A':
                m1_hq_fulllocation == m1_hq_state + "; " + m1_hq_coordinates
            else:
                m1_hq_fulllocation == m1_hq_state + "; " + m1_hq_country + "; " + m1_hq_coordinates
                
            row.append(m1_hq_fulllocation)
            
            m2_hq_state = method_two_hq[company_id]['state']
            m2_hq_country = method_two_hq[company_id]['country']
            m2_hq_coordinates = "(" + str(method_two_hq[company_id]['center_lat']) + ", " + str(method_two_hq[company_id]['center_lng'] + ")")
            m2_hq_fulllocation = ''
            if m2_hq_state == 'N/A' and mq_h2_country == 'N/A':
                m2_hq_fulllocation == m2_hq_coordinates
            elif m2_hq_state == 'N/A' and not mq_h2_country == 'N/A':
                m2_hq_fulllocation == m2_hq_country + "; " + m2_hq_coordinates
            elif not m2_hq_state == 'N/A' and mq_h2_country == 'N/A':
                m2_hq_fulllocation == m2_hq_state + "; " + m2_hq_coordinates
            else:
                m2_hq_fulllocation == m2_hq_state + "; " + m2_hq_country + "; " + m2_hq_coordinates
                
            row.append(m2_hq_fulllocation)
            
            # get the distance between the two headquarter estimates
            hq_distance = formulas.haversine(method_one_hq[company_id]['center_lat'], method_one_hq[company_id]['center_lng'],
                                             method_two_hq[company_id]['center_lat'], method_two_hq[company_id]['center_lng'])
            
            row.append(hq_distance)
            
            pairs = company_paired_clusters[company_id]
            distances = [float(pair[2]) for pair in pairs]
            pair_strings = ['(' + str(pair[0]) + '-' + str(pair[1]) + ')' for pair in pairs]
            
            distance_mean = statistics.mean(distances)
            distance_median = statistics.median(distances)
            distance_sd = statistics.stdev(distances, xbar)
            
            row.append(distance_mean)
            row.append(distance_median)
            row.append(distance_sd)
            row.append('; '.join(pair_strings))
            
            csv_writer.writerow(row)
            
    
    
    
            
    