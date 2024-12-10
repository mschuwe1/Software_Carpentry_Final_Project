# Software_Carpentry_Final_Project

This Python project provides users with a simple tool to visualize data. Specifically, it 
leverages the Center for Medicare and Medicaid's (CMS) Open Payments Database. 
This database is published every year and details the payments various pharmaceutical and medical device companies 
make to physicians and hospitals. 

# Prerequisites
- A txt file is also available on the repository "requirements.txt" that outlines the libraries and versions below:
- Python 3.0 or higher
- Required Libraries:
    - Numpy
    - tkinter
    - pandas
    - matplotlib
    - seaborn
    - scypy
 
# Usage
Clone the Final_Submission.py file


The script will open a UI asking the user to select from a dropdown menu the CMS database to query. 
For the purposes of this project, the database is limited to the most recent publication regarding Research Payments.
The tool automatically quereies the CMS database's API, and dowloads the data into a pandas dataframe. 

The tool will then perform data cleaning, and allow the user to investigate the columns of the data. 
Additionaly, there are options for the user to generate bar graphs of various investigator qualities, 
including companies paying the investigator, amount of annual payments to investigators, and the drugs/devices related to those payments. 

There is also an option for users to query for investigators by name and export results into a csv file. 




