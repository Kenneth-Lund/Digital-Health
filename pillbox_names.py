"""
This file returns a list of URl's corresponding with the correct drug name and rxcui
which is not found in the NIH RxTerms data file.
"""



import csv
from collections import defaultdict

list_of_urls = defaultdict(list)
drugs_info = defaultdict(list)

list = []

#This is only for reading the csv file
def read_only_lines(myfile, start, finish):
    test = csv.reader(myfile)
    for ii,line in enumerate(test):
        if ii>=start and ii<finish:
            yield line
        elif ii>=finish:
            return

#This is for reading regular file
def read_only_lines2(myfile, start, finish):
    for ii,line in enumerate(myfile):
        if ii>=start and ii<finish:
            yield line
        elif ii>=finish:
            return

server_data = open("RxTerms201806(2).txt", "r")
pillbox_file = open("pillbox_201605.csv", "r")
#encoding "ISO-8859-1" is to prevent a strange error that came up reading the file







"""

This function checks to see if a pillbox RXCUI is contained within the NIH file.
If a pillbox RXCUI is not in the NIH file, it will be added to the drugs info URL list.

"""
def get_drugs():
    print("getting links...")

    #add all the rxcui's from the sql data we have into a list
    for line in read_only_lines2(server_data, 1, 20954):

        words = line.split("|")
        sql_rxcui = words[0]
        list.append(sql_rxcui)

    #go through new csv file to check for RXCUI's that are not found in our sql data
    for row in read_only_lines(pillbox_file, 1, 47116):

        tester = False
        new_rxcui = row[24]
        drug_name = row[29]
        drug_dosage = row[23]

        #if the new rxcui is already in our database, break and check next one
        for sql_rxcui in list:
            if new_rxcui == sql_rxcui:
                tester = True
                break

        #if the new rxcui is not, create new link for it
        if (tester == False and new_rxcui != ''):
            url = 'https://www.drugs.com/search.php?searchterm=%s' % (drug_name.replace(' ', '%20'))

            list_of_urls[new_rxcui].append(url)
            drugs_info[new_rxcui].append(drug_name)
            drugs_info[new_rxcui].append(drug_dosage)


get_drugs()

def return_urls():
    return list_of_urls

def return_info():
    return drugs_info









