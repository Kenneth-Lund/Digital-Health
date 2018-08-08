"""
This file simply puts each drug_id corresponding to the image link RXCUI into the imgs table
"""



import mysql.connector

cnx = mysql.connector.connect(user='drugs_db', password='drugsdb_2018',
                              host='drugsdbinstance.c7abkdznprtj.us-east-1.rds.amazonaws.com',
                              database='drugsdb')

cursor = cnx.cursor()
rxcuis = cursor.execute("SELECT rxcui FROM drugsdb.drug_images;")
rows = cursor.fetchall()

for row in rows:
    rxcui = row[0]

    print(rxcui)

    drug_ids = cursor.execute("SELECT drug_id FROM drugsdb.drugs_info WHERE rxcui = '%s'" % (rxcui))
    row = cursor.fetchall()

    drug_id = row[0][0]

    cursor.execute("""
       UPDATE drug_images SET drug_id=%s WHERE rxcui=%s
    """, (drug_id, rxcui))

    cnx.commit()

cnx.close()