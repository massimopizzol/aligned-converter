import brightway2 as bw
import pandas as pd
import numpy as np
from lci_to_bw2 import * # import all the functions of this module

# set project
bw.projects.set_current('bio3-ei3.9csq') # any project with biosphere3 and ecoinvent 3.9 conseq already imported
bw.databases


# import data from csv
mydata = pd.read_csv('dummy-lci-table-format.csv', header = 0, sep = ",")
mydata.head()

# This below to select only some columns, the minimum required ones are those:
# mydb = mydata[['Activity database','Activity code','Activity name','Activity unit','Activity type',
#               'Exchange database','Exchange input','Exchange amount','Exchange unit','Exchange type']].copy()

# This to drop specific columns
# mydb = mydata.drop('Simapro unit', 1).copy()

# This to include all columns
mydb = mydata.copy()
mydb.head()


#create dictionary in bw format
bw2_db = lci_to_bw2(mydb) # a function from the lci_to_bw2 module
bw2_db


# write database
t_db = bw.Database('dummy-lci') # it works because the database name in the excel file is the same
t_db.write(bw2_db) # shut down all other notebooks using the same project when doing this


# do checks
[print(act) for act in t_db]  # check foreground activities and new bioshpere exchanges
[[print(act['name'], exc['amount']) for exc in list(act.exchanges())]for act in t_db]  # check structure 

myact = t_db.random()
print(myact)
print(list(myact.exchanges())[0]._data) # here you can see Simapro info maintained


# calculation
mymethod = ('IPCC 2013', 'climate change', 'global warming potential (GWP100)')

#activity_name = 'Process A' # I want to find the code for this.
#for activity in bw.Database('dummy-lci').search(activity_name, limit = 10):  
#    print(activity)
#    print(activity['code'])

myact = bw.Database('dummy-lci').get('89537cc9-2e7e-4304-ac2b-1ba8e89f2aa6') # Process A
#myact = bw.Database('dummy-lci').get('eef84f20-c0ef-4e85-94ed-a7b39791ebb7') # Process B
#myact = bw.Database('dummy-lci').get('e76425d6-ad7f-4d46-9ad3-3fcad95304fa') # Process C
#myact = bw.Database('ecoinvent 3.9 conseq').get('db6855ad6838970a9d3b02f257d2f225') # bike
#myact = bw.Database('ecoinvent 3.9 conseq').get('f2846d746b70a0b5e4a7c91b0a8463e7') # barley grain

functional_unit = {myact: 1}
lca = bw.LCA(functional_unit, mymethod)
lca.lci()
lca.lcia()
print(lca.score)