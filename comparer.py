import csv

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
def get_cluster_set(filename):
    #read in the data from the previous module
    with open(filename, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        
        
        
if __name__ == '__main__':
    print('Randomly choosing ' + str(num_of_companies) + ' companies')
    
    #get the companies to randomly choose
    with open(filename, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        
        for row in reader:
            cnt += 1
    