import csv
import numpy as np
import pandas as pd
from lci_to_sp import *

imported_data = pd.read_csv('dummy-lci-table-format.csv', header = 0, sep = ",", encoding='utf-8-sig') # using csv file avoids encoding problem
imported_data.head()

bw_to_spcsv(imported_data, 'dummy-lci-spcsv-format.csv')
