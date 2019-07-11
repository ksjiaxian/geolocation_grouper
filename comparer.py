import csv
import ast
import random

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
            curr_company = row['company']
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
#returns a set of tuples, where each element in the tuple is a coordinate pair
def pair_clusters(set_one, set_two):
    #TODO!!!
    pass
    
    
if __name__ == '__main__':
    #write header
    with open('outputs/method_comparison.tsv', 'w', newline="\n", encoding='utf-8-sig') as out_file: 
        csv_writer = csv.writer(out_file, delimiter='\t')
        header = ["company", "id", "M1_num_clusters", "M2_num_clusters", "M1_num_remote_clusters", "M2_num_remote_clusters", 
                  "M1_HQ", "M2_HQ", "HQ1-HQ2_distance", "average_cluster_distance", "median_cluster_distance", "sd", "pairs"]
        csv_writer.writerow(header)
        
    print('Randomly choosing ' + str(num_of_companies) + ' companies')
    
    #get the companies to randomly choose, save their metadata as 
    companies = {}
    with open(filename_1, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        
        for row in reader:
            companies.add((row['company']), ) ##todo
            
    sample = random.sample(companies, num_of_companies)
    
    print(len(sample))
    for co in sample:
        print(co)
    
    method_one_clusters = get_cluster_set(filename_1, companies)
    method_two_clusters = get_cluster_set(filename_2, companies)
    
    #get the metadata about each of the companies
    
    
    #turn these two dictionaries into one dictionary with two sets per company key
    company_cluster_sets = {}
    for company in companies:
        list_one = method_one_clusters[company]
        list_two = method_two_clusters[company]
        company_cluster_sets[company] = (list_one, list_two)
        
    #for each company, pair the corresponding clusters and store them as a list of tuples of coordinates
    company_paired_clusters = {}
    for company, (list_one, list_two) in company_cluster_sets.items():
        company_paired_clusters[company] = pair_clusters(list_one, list_two)
        
    #write the body of the data
    with open('outputs/method_comparison.tsv', 'n', newline="\n", encoding='utf-8-sig') as out_file: 
        csv_writer = csv.writer(out_file, delimiter='\t')
        
        for company, cluster_pair_set in company_paired_cluster.items():
            
                  row = [str(company), str()]
                  csv_writer.writerow(header)  
        
    #NOT COMPLETE
    
    
            
    