"""

This file:

1. Grabs all the drug_names from or drugs info table.
3. Filter both the drug names from drugs info and drug descriptions from the adverse event.
4. takes in an adverse event descreption (drug_reason parameter) and compares it to the every drug name,
   checks if the drug name exists in the drug reason.
5. if a drug name exists in the drug reason, it takes a comparison and adds it to a result list.
6. if there are results, the top 5 highest most similar drug names are used to fetch drug_ids
7. A select statment is made to fetch all the drug ids for each of the 5 most smilar drug names.

"""


import difflib
import mysql.connector



"""
Returns a list of drug ids based on adverse event description given
"""
def check(drug_reason, cursor):

    resulted_drugs = {} #store the drugs that a comparison is made for

    #get all drug names from database
    names = cursor.execute('SELECT drug_name FROM drugsdb.drugs_info;') #select statment to grab all drug names from SQL database
    rows = cursor.fetchall()

    #This counts how many total results are in the 'resulted_drug' list
    counter = 0


    for row in rows:

        table_drug = (str(row[0])).lower()
        adverse_drug_description = drug_reason

        desc_filtered1 = table_drug.replace(',', '')
        desc_filtered2 = desc_filtered1.replace('and', '')
        desc_filtered3 = desc_filtered2.replace('/', ' ')
        desc_filtered4 = desc_filtered3.replace('products', '')
        desc_filtered5 = desc_filtered4.replace('  ', '')

        #filter out all stuff for the adverse event description
        adverse_drug_filtered = filter(adverse_drug_description)

        table_drug_test = desc_filtered5.split()
        adverse_drug_test = adverse_drug_filtered.split()

        test = False


        for x in range(len(adverse_drug_test)):
            for i in range(len(table_drug_test)):
                if adverse_drug_test[x] in table_drug_test[i]:
                    test = True

        # if a string from the adverse event exists in the drug name from table, add it to the resulted list
        if (test):
            counter+=1

            #compare the adverse event desc with the name
            compare = difflib.SequenceMatcher(lambda x: x in ' ', table_drug, adverse_drug_filtered).ratio()

            resulted_drugs[compare] = table_drug
        else:
            pass

    #if there are no resulted drugs, there were no drugs found for this event, return "None" for drug_ids
    if resulted_drugs != {}:
        drug_ids = get_drug_ids(resulted_drugs, counter, cursor)

    else:
        drug_ids = ['None']

    return drug_ids







"""
Helper function that creates the drug_ids list if the 'resulted_drugs' contains comparisons
"""
def get_drug_ids(resulted_drugs, counter, cursor):

    drug_ids = []
    highest_results = []

    #add actual drug names to 'highest_results' list to search for drug id, (only top 5 of results)
    if counter > 5:
        sorted_drugs = sorted(resulted_drugs)
        top_drugs = sorted_drugs[-5:]

        for i in top_drugs:
            highest_results.append(resulted_drugs[i])  #resulted[i] = drug name
    else:
        top_drugs = sorted(resulted_drugs)

        for i in top_drugs:
            highest_results.append(resulted_drugs[i]) #resulted[i] = drug name


    for drug in highest_results:
        try:
            drug_id_results = cursor.execute("SELECT drug_id FROM drugsdb.drugs_info WHERE drug_name = '%s'" % (drug))
            rows2 = cursor.fetchall()

            for row2 in rows2:
                drug_ids.append(str(row2[0]))
        except:
            pass

    return drug_ids






"""
Simple function that filters out keywords from the adverse event descriptions, helps match with 
drugs info table drug names
"""
def filter(adverse_drug):

    desc_filtered1 = adverse_drug.replace(',', '')
    desc_filtered2 = desc_filtered1.replace('and', '')
    desc_filtered3 = desc_filtered2.replace('injectable', '')
    desc_filtered4 = desc_filtered3.replace('products', '')
    desc_filtered5 = desc_filtered4.replace('hydrochloride', '')
    desc_filtered6 = desc_filtered5.replace('sulfate', '')
    desc_filtered7 = desc_filtered6.replace('injection', '')
    desc_filtered8 = desc_filtered7.replace('liquid', '')
    desc_filtered9 = desc_filtered8.replace('liquids', '')
    desc_filtered10 = desc_filtered9.replace('drug', '')
    desc_filtered11 = desc_filtered10.replace('sodium', '')
    desc_filtered12 = desc_filtered11.replace('tablets', '')
    desc_filtered13 = desc_filtered12.replace('hydrochlorothiazide', '')
    desc_filtered14 = desc_filtered13.replace('methylsulfate', '')
    desc_filtered15 = desc_filtered14.replace('/', ' ')
    desc_filtered16 = desc_filtered15.replace('  ', ' ')
    desc_filtered17 = desc_filtered16.replace('   ', ' ')

    return desc_filtered17
















