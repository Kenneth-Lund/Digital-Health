"""

This file grabs nih drug names the rxTerms file returns a list of the urls corresponding to the name/Rxcui given

"""



from collections import defaultdict

myfile = open("RxTerms201806.txt", "r")

drugs_info = defaultdict(list)
drug_dosages = defaultdict(list)
list_of_urls = defaultdict(list)


# This function allows us to choose a section of the text file to iterate through
def read_only_lines(myfile, start, finish):
    for ii, line in enumerate(myfile):
        if ii >= start and ii < finish:
            yield line
        elif ii >= finish:
            return


def get_drugs():
    for line in read_only_lines(myfile, 1, 20954):
        words = line.split("|")
        # seperates data in text file to grab
        drug_rx = (words[0])
        drug_name = (words[7])
        drug_dosage = (words[10])

        print(drug_name)

        filtered_drug = drug_name.split("(")[0]
        # drug becomes easier to read and more simple after this action
        url = 'https://www.drugs.com/search.php?searchterm=%s' % (filtered_drug)

        list_of_urls[drug_rx].append(url)
        drugs_info[drug_rx].append(drug_name)
        drugs_info[drug_rx].append(drug_dosage)


get_drugs()


def return_urls():
    return list_of_urls


def return_info():
    return drugs_info






