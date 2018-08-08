"""
This file inserts all the RxTerm image links found from the NIH restful API
"""

from collections import defaultdict
import requests
import json

import mysql.connector

session = requests.session()

myfile = open("RxTerms201806(2).txt", "r")
api_links = defaultdict(list)
img_links = defaultdict(list)


#Reads the Rxterms file
def read_only_lines(myfile, start, finish):
    for ii, line in enumerate(myfile):
        if ii >= start and ii < finish:
            yield line
        elif ii >= finish:
            return




"""
This function reads the rxTerms file and combines the drug name and base url to create an API link.
Then it adds the link the api_links dictionary to scrape the actual image urls.
"""
def get_drugs():
    for line in read_only_lines(myfile, 1, 200):
        words = line.split("|")
        drug_rx = (words[0])



        url = "https://rximage.nlm.nih.gov/api/rximage/1/rxnav?rxcui=" + drug_rx

        api_links[drug_rx].append(url)

    get_img_links(api_links)





"""
This function uses the api links created to call the restful API and insert the image url/rxcui into the img links table
"""
def get_img_links(api_links):
    for key, val in api_links.items():

        response = session.get(val[0])
        print(key)
        #print(response.text)

        drug_id = cursor.execute("SELECT drug_id FROM drugsdb.drugs_info WHERE rxcui = '%s'" % (key))
        rows = cursor.fetchall()

        drug_id = rows[0][0]
        
        try:
            data = json.loads(response.text)

            if data['nlmRxImages'] != []:
                img_length = len(data['nlmRxImages'])
                img = data['nlmRxImages'][img_length - 1]['imageUrl']
                cursor.execute("INSERT INTO img_links(img_id, drug_id, rxcui, img_link) values(%s, %s, %s, %s)",
                               ("default", drug_id, key, img))
                cnx.commit()
            else:
                print("no image" + key)
        except(ValueError):
            print("no data")
            pass



"""

Initialize the SQL connection

"""

cnx = mysql.connector.connect(user='drugs_db', password='drugsdb_2018',
                              host='drugsdbinstance.c7abkdznprtj.us-east-1.rds.amazonaws.com',
                              database='drugsdb')

cursor = cnx.cursor()
get_drugs()
cnx.close()