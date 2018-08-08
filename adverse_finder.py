from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import mysql.connector
import datetime

def get_hrefs():

    html = browser.page_source

    soup = bs(html, 'html.parser')

    test = soup.find('div', {'class': 'col-md-9 col-lg-9 middle-column'})

    test2 = test.find('article')

    table = test2.find('tbody')

    rows = table.find_all('tr')

    for columns in rows:

        column_data = columns.find_all('td')

        href = column_data[1].find('a').get('href')

        link = 'https://www.fda.gov' + href
        date = column_data[0].text
        desc = column_data[2].text
        reason = column_data[3].text
        recall_int = 1
        time_created = now.strftime("%Y-%m-%d %H:%M")


        cursor.execute(
            "INSERT INTO adverse_stage(test_id, event_link, event_desc) values(%s, %s, %s)",
            ("default", link, desc))

        """cursor.execute(
            "INSERT INTO adverse_events(ae_id, event_date, event_desc, recall, recall_link, event_severity, created_date, updated_date) values(%s, %s, %s, %s, %s, %s, %s, %s)",
            ("default", date, reason, recall_int, link, "Null", time_created, time_created))"""

        cnx.commit()



url = 'https://www.fda.gov/Drugs/DrugSafety/DrugRecalls/default.htm'

options = Options()
options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
options.add_argument('--disable-gpu')
options.add_argument('--headless')

browser = webdriver.Chrome(options= options, executable_path=r'/Users/name/Downloads/chromedriver')
browser.get(url)

cnx = mysql.connector.connect(user='', password='',
                              host='',
                              database='drugsdb')
#initialize cursor
cursor = cnx.cursor()
now = datetime.datetime.now()

get_hrefs()


browser.quit()
cnx.close()

