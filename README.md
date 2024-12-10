# Software_Carpentry_Final_Project

This Python project provides users with a simple tool to visualize data. Specifically, it 
leverages the Center for Medicare and Medicaid's Open Payments Database. 
This database is published every year and details the payments various pharmaceutical and medical device companies 
make to physicians and hospitals. 

#Prerequisites
- Python 3.0 or higher
- Required Libraries:
    - Numpy
    - tkinter
    - pandas
    - matplotlib
    - seaborn
    - scypy
 
#Usage
Clone the repository
The script will open a UI asking the user to select from a dropdown menu the CMS database to query. 
For the purposes of this project, the database is limited to the most recent publication regarding Research Payments. 
The tool will then perform data cleaning, and allow the user to investigate the columns of the data. 
Additionaly, there are options for the user to generate bar graphs of various investigator qualities, 
including companies paying the investigator, amount of annual payments to investigators, and the drugs/devices related to those payments. 
There is also an option for users to query for investigators by name and export results into a csv file. 

#Ideas for User Available Visualizations
# 
# - number of investigators per: 
  - state
  - specilty
  - manufacturer
  - Form_of_Payment_or_Transfer_of_Value
    
# - average payment (Total_Amount_of_Payment_USDollars) per:
  -  State - Recipient_State, Principal_Investigator_1_State
  -  Provider Specialty
  -  Manufacturer - Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_ID
  -  Date_of_Payment -
  -  Form_of_Payment_or_Transfer_of_Value
  -  Teaching_Hospital_Name
  -  Covered_Recipient_Type

- Name_of_Drug_or_Biological_or_Device_or_Medical_Supply_1
- Indicate_Drug_or_Biological_or_Device_or_Medical_Supply_1
- Product_Category_or_Therapeutic_Area_1



In some way include the outliers/big payers clinical trial link using the variable ClinicalTrials_Gov_Identifier

Dec 8 To DO:
- remove empties from the total payment amounts/cut out the outliers
- For specialty, use the PI onee "prinicpa_investigator_1_Specialty_1"
- For the specialty, cout ot the first phrase "Osetopathic and ALl etc..."
- For drug compnay: "Submitting_Applicable_Manufacturer_or
_Applicable_GPO_Name"
- increase x axis spacing for all the histograms
- Form_of_Payment_or_Transfer_of_Value
- need to edit histogram function - only allow seelction of total usd payments, and consider filtering by state/specialty/manufactuer essentially the same categorical variables as above
- unit testing -
- verify if the missing values are actually missing or some other non-alpha value
- try to 
  
Dec 9 To Do:

Mark 
- rename the variables on the user side
- truncate physician specilaty variable
- get basic stats to display mean median range
- unit testing  


Mitch
- remove scatter plot
- add tool for looking up investigator by name and by hospital name
-   Covered_Recipient_First_Name
-   Covered_Recipient_Middle_Name
-   Covered_Recipient_Last_Name
-   Covered_Recipient_Name_Suffix
-   Teaching_Hospital_Name
