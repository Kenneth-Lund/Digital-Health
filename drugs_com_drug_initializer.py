"""
This file takes in the 'pillbox' or 'Drug_names' file and uses the 'urls' created to
scrape the descriptions for each drug.
"""




import requests
import time
import datetime
import threading
from bs4 import BeautifulSoup as bs
import pillbox_names
#import Drug_names
import mysql.connector

session = requests.session()

#intialize system time formatting
now = datetime.datetime.now()

drugs_info = pillbox_names.return_info()
list_of_urls = pillbox_names.return_urls()







"""
This function will allow us to scrape both descriptions and black box warnings.  If the initial url contains a blaxkbox
warning link, then it will scrape the blackbox only for that specific drug.

'drug_rx' parameter = drug rxcui
'url' parameter = url with drug name corresponding to the drug RXCUI Number.

"""
def parse(url, drug_rx):
    print("Loading")
    drug_name = drugs_info[drug_rx][0]

    filtered_drug = drug_name.split("(")[0]
    test = filtered_drug.replace(" ", "-")
    test2 = test[:-1]

    con_url = "https://www.drugs.com/cons/%s.html" % (test2)
    # creates TEMPORARY LINK to search for black box warning

    data = session.get(url, allow_redirects=False)

    soup = bs(data.text, 'html.parser')

    desc_search = soup.find('div', {'class': "snippet search-result search-result-with-secondary"})
    # checks to see if the url with the drug given has possibility of containing a description.

    if desc_search != None:

        desc_test = soup.find('p', {'class': "search-result-desc"})
        # grabs description
        if desc_test != None:
            # if there is a description, scrape it then check temporary blackbox warning link
            desc = desc_test.text

            drugs_info[drug_rx].append(desc)

            data2 = session.get(con_url, allow_redirects=False)

            # connect to TEMPORARY LINK after description session is over
            soup2 = bs(data2.text, 'html.parser')

            test_case = soup2.find('div', {'class': "blackboxWarning"})
            # test_case = the black box warning html #821
            if test_case != None:
                drugs_info[drug_rx].append(test_case.text)
            else:
                drugs_info[drug_rx].append("No Black Box Warning")
        else:
            drugs_info[drug_rx].append("No description")
    else:
        drugs_info[drug_rx].append("No Description")
        drugs_info[drug_rx].append("No Black Box Warning")
        # if there is no description, black box warning will be skipped. , NIH_ID, drug_name, drug_dosage, drug_description, blackbox_warning) , key, drugs_info[key][0], drugs_info[key][1], drugs_info[key][2], drugs_info[key][3]





"""

This function sends all the data scraped from the URLS into the drugs info table.  

"""
def send_data():
    print('sending data...')

    time = now.strftime("%Y-%m-%d %H:%M")

    for key in drugs_info:
        cursor.execute(
            "INSERT INTO drugs_info(drug_id, rxcui, drug_name, drug_dosage, drug_description, blackbox_warning, created_date, updated_date) values(%s, %s, %s, %s, %s, %s, %s, %s)",
            ("default", key, drugs_info[key][0], drugs_info[key][1], drugs_info[key][2], drugs_info[key][3], time, time))

        cnx.commit()






"""

This function enables multithreading by creating a new thread for every url in the 'url list'.  It calls and adds 
the "parse" function for every rxcui/url to a pool.


"""
def parse_pool():
    thread_pool = []
    count = 0
    # for every drug, grab the url and add it to an individual thread to execute
    for drug_rx, url in list_of_urls.items():
        url1 = url[0]
        count += 1
        thread = threading.Thread(target=parse, args=(url1, drug_rx,))
        thread_pool.append(thread)
        thread.start()
        # this time/pause prevents from being IP banned
        time.sleep(.35)
        print(count)
        # This pause allows me to scrape thousands of urls from the same site without getting an IP ban

    # after threads have been created and started join them
    for thread in thread_pool:
        thread.join()



"""
Databse intialization
"""
cnx = mysql.connector.connect(user='drugs_db', password='drugsdb_2018',
                              host='drugsdbinstance.c7abkdznprtj.us-east-1.rds.amazonaws.com',
                              database='drugsdb')

cursor = cnx.cursor()

parse_pool()
send_data()
cnx.close()




