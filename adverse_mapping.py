import mysql.connector
import adverse_drug_id

# initialize database connection
cnx = mysql.connector.connect(user='drugs_db', password='drugsdb_2018',
                              host='drugsdbinstance.c7abkdznprtj.us-east-1.rds.amazonaws.com',
                              database='drugsdb')
# initialize cursor
cursor = cnx.cursor()

list_of_adverse_get = cursor.execute('SELECT event_desc, event_link FROM drugsdb.adverse_stage;')
list_of_adverse = cursor.fetchall()

def get_mapping(list_of_adverse):

    for desc1 in list_of_adverse:
        print("executing")
        desc = desc1[0].lower()
        link = desc1[1]

        desc_filtered16 = adverse_drug_id.filter(desc)

        ae_id_get = cursor.execute("SELECT ae_id FROM drugsdb.adverse_events WHERE recall_link = '%s'" % (link))
        ae_id1 = cursor.fetchall()
        ae_id = str(ae_id1[0][0])

        print(desc_filtered16)
        drug_ids = adverse_drug_id.check(desc_filtered16, cursor)


        for drug_id in drug_ids:
            print("ok")
            #cursor.execute("INSERT INTO event_drug_mapping2(id, ae_id, drug_id) values(%s, %s, %s)", ("Default", ae_id, drug_id))

            #cnx.commit()



get_mapping(list_of_adverse)
cnx.close()
