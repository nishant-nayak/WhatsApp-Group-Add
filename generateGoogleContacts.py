import csv
import pandas as pd

# File name that contains the data of Names/Numbers
dataFileName = 'data/data.xlsx'

# File name of the output file
outputFileName = 'data/output.csv'

# Fieldnames required for Google Contacts
FIELDNAMES = ['Name','Given Name','Additional Name','Family Name','Yomi Name','Given Name Yomi','Additional Name Yomi','Family Name Yomi','Name Prefix','Name Suffix','Initials','Nickname','Short Name','Maiden Name','Birthday','Gender','Location','Billing Information','Directory Server','Mileage','Occupation','Hobby','Sensitivity','Priority','Subject','Notes','Language','Photo','Group Membership','E-mail 1 - Type','E-mail 1 - Value','Phone 1 - Type','Phone 1 - Value','Phone 2 - Type','Phone 2 - Value','Phone 3 - Type','Phone 3 - Value','Phone 4 - Type','Phone 4 - Value','Address 1 - Type','Address 1 - Formatted','Address 1 - Street','Address 1 - City','Address 1 - PO Box','Address 1 - Region','Address 1 - Postal Code','Address 1 - Country','Address 1 - Extended Address']

# Open Data file
df = pd.read_excel(dataFileName)

# Open Output File
with open(outputFileName, 'w', newline='') as writefile:
    writer = csv.DictWriter(writefile, fieldnames=FIELDNAMES)
    writer.writeheader()

    # Iterate through the data
    for _, row in df.iterrows():
        # If the number consists of only digits, pandas considers it as a float
        # Thus, convert to int before writing to the file
        if (type(row["WhatsApp Number"])) is float:
            writer.writerow({
                "Name": f'SBMD {row["First Name"]} {row["Last Name"]}',
                "Given Name": f'SBMD {row["First Name"]}',
                "Family Name": f'{row["Last Name"]}',
                "Phone 1 - Type": "WhatsApp",
                "Phone 1 - Value": f'{int(row["WhatsApp Number"])}',
            })
        # If the number contains spaces or special characters, pandas considers it as a string
        else:
            writer.writerow({
                "Name": f'SBMD {row["First Name"]} {row["Last Name"]}',
                "Given Name": f'SBMD {row["First Name"]}',
                "Family Name": f'{row["Last Name"]}',
                "Phone 1 - Type": "WhatsApp",
                "Phone 1 - Value": f'{row["WhatsApp Number"]}',
            })
