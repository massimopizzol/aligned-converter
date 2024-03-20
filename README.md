[![DOI](https://zenodo.org/badge/733667413.svg)](https://zenodo.org/doi/10.5281/zenodo.10845909)

# Readme

## aligned-converter

Life Cycle Inventory data converters and importers for Simapro and Brightway2 LCA software

Python scripts to convert foreground life cycle inventory data in **tabular format** into a format that can be imported in LCA software SimaPro and Brightway2.
Links between foreground and background datasets and all types of exchanges can be specified.

* `lci_to_sp.py` converts from .csv file in tabular format to Simapro CSV. See also [Simapro-CSV-converter](https://github.com/massimopizzol/Simapro-CSV-converter) for a previous version that uses another excel template.
 
* `lci_to_bw2.py` converts from .csv file in tabular format to a dictionary that can be written as a Brightway2 database

For detailed info about the tabular format of the LCI data see the [aligned-datapackage repository](https://github.com/massimopizzol/aligned-datapackage) and this [ALIGNED T1.2 LCI data template zenodo archive](https://doi.org/10.5281/zenodo.10843472).


Requirements:

* pandas library
* numpy library
* csv library
* Tested with python v.3.11, might work with lower python 3 versions too. 

## Column names

Important, **do not change column names** in the template. The LCI table must have these columns with these exact names:

_Activity database;Activity code;Activity name;Activity unit;Activity type;Exchange database;Exchange input;Exchange amount;Exchange unit;Exchange type;Exchange uncertainty type;Exchange loc;Exchange scale;Exchange negative;Simapro name;Simapro unit;Simapro type_

For import into Brightway2, the last seven columns are not mandatory. For import into Simapro, Brighway2 exchange codes are not needed. Additional columns can be added if needed (e.g., a column named "Notes" or "Additional information" or "Other").
  

## Import to SimaPro

Prepare the life cycle inventory in Excel. 
Save it in .csv format in the same folder as the Python script `lci_to_sp.py` 

* In the LCI table, fill in the mandatory columns. Note that for import into Simapro brighway codes (values for the "Exchange input" column) are not needed. 
* Use exact dataset names in the "Simapro name" column to link with any specific foreground or background activity. 
* In the _Simapro type_ column use "Raw", "Air", "Water", "Soil", "Waste", "Social", "Economic" to indicate exchanges
* In the _Simapro type_ column use "Wastetotreatment" to indicate database processes of the waste treatment category
* Uncertainty, sub-compartment of emission (e.g. "high-population"), and comments can not be included (they can be specified directly in the converted .csv file though)


Run the conversion script, for example:

```python

import csv
import numpy as np
import pandas as pd
from lci_to_sp import *

imported_data = pd.read_csv('CsvTableFileName.csv', header = 0, sep = ",", encoding='utf-8-sig')
bw_to_spcsv(imported_data, 'SimaProCsvFileName.csv')

```

Check that the background database(s) from which the dataset names were taken is current selected among the "libraries", otherwise the import will now work.

From SimaPro, use Import>File and the following settings:

* File format: "SimaPro CSV"
* Object link method: "Try to link imported objects to existing objects first"
* CSV format separator: "Tab"
* Other options: "Replace existing processes..."


## Import to Brightway2

Prepare the life cycle inventory in Excel. 
Save it in .csv format in the same folder as the Python script `lci_to_bw2.py`

* For import into Brightway2, the last seven columns are not strictly mandatory. However, it is recommended to include uncertainty and SimaPro codes for reference under column _Simapro name_.
* In the column _Exchange input_	use exact dataset codes to link with other foreground or background activities
* In the column _Exchange type_ use "technosphere", "production", "biosphere", or "substitution". to indicate various types of exchanges. See Brightway2 docs for more info. 

To run the converter one needs to open a Brightway2 project **that includes the needed biosphere database and background databases** ([see tutorial for importing biosphere3 and ecoinvent here](https://github.com/massimopizzol/advanced-lca-notebooks/blob/main/Course-material/3-Ecoinvent.ipynb)).

Within this project, run the conversion script as in the example below:

```python

import brightway2 as bw
import pandas as pd
import numpy as np
from lci_to_bw2 import *

bw.projects.set_current('ProjectName') # any project with the needed biosphere and background database
mydata = pd.read_csv('CsvTableFileName.csv', header = 0, sep = ",")
bw2_db = lci_to_bw2(mydata) 
t_db = bw.Database('DatabaseName') # same name as specified the data file under "Activity database"
t_db.write(bw2_db) 

```

## Worked examples

The files `dummy-lci-table-format.xlsx` and `dummy-lci-table-format.csv` include a fictional LCI using ecoinvent database, version 3.9.1 consequential system model.

**They can be used as template** and to test the import to software. 

In particular running the `lci_to_sp.py`  returns the file `dummy-lci-spcsv-format.csv` to be imported into SimaPro. 

See also the two worked examples `testing-conversion-in-spcsv.py` and `testing-import-in-bw.py`.


## Disclaimer and recommended use

The foreground system has to be correctly structured before the import succeeds. No tests nor automatic checks are included. For example, mispelling of dataset names, exchange types, incomplete systems (exchanges not defined) etc. will result in a failed import. For debugging, the recommended approach is to use the automatic error messages provided by the LCA software during import. Alternatively, use the validation options of the [frictionless](https://specs.frictionlessdata.io/#overview) data standards and related [frictionless framework](https://framework.frictionlessdata.io/) libraries in python, and use the aligned schema to validate the data. Examples of this are included in the [aligned-datapackage repository](https://github.com/massimopizzol/aligned-datapackage) under the folder "code-and-examples".

These converters have been designed for importing foreground data of limited size. They will work for relatively large systems (hundreds to thousands of exchanges) but they are not recommended for database-scale data import (tens of thousands of exchanges or more).  


## Contact & info

[Massimo Pizzol](mailto:massimo@plan.aau.dk)

## Funding

This work was carried out within Work Package 1: Shared modelling framework and learnings, Task 1.2: Framework for foreground life cycle inventory of bio-based sectors, of the ALIGNED project [wwww.alignedproject.eu](wwww.alignedproject.eu), Horizon Europe grant agreement N° 101059430 [^1].

[^1]: _Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or the European Research Executive Agency. Neither the European Union nor the granting authority can be held responsible for them._
