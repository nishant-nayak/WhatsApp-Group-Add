import csv
import pandas as pd

##### CONFIG STARTS #####
# File name that contains the data of Names/Numbers
DATA_FILE_NAME = 'data/data.xlsx'

# File name of the output file
OUTPUT_FILE_NAME = 'data/output.csv'

# Is the name defined in a single field, or as First Name and Last Name?
IS_NAME_SINGLE_FIELD = False

# Fill ONLY if IS_NAME_SINGLE_FIELD is True, else leave blank
FULL_NAME_FIELD = "Name"

# Fill ONLY if IS_NAME_SINGLE_FIELD is False, else leave blank
FIRST_NAME_FIELD = "First Name"
LAST_NAME_FIELD = "Last Name"

# Name of the Phone Number field
PHONE_NUMBER_FIELD = "WhatsApp Number"

# Unique identifier for contact names
IDENTIFIER_STR = "XQCL"
##### CONFIG ENDS #####

# Fieldnames required for Google Contacts, DO NOT EDIT
FIELDNAMES = ['Name','Given Name','Additional Name','Family Name','Yomi Name','Given Name Yomi','Additional Name Yomi','Family Name Yomi','Name Prefix','Name Suffix','Initials','Nickname','Short Name','Maiden Name','Birthday','Gender','Location','Billing Information','Directory Server','Mileage','Occupation','Hobby','Sensitivity','Priority','Subject','Notes','Language','Photo','Group Membership','E-mail 1 - Type','E-mail 1 - Value','Phone 1 - Type','Phone 1 - Value','Phone 2 - Type','Phone 2 - Value','Phone 3 - Type','Phone 3 - Value','Phone 4 - Type','Phone 4 - Value','Address 1 - Type','Address 1 - Formatted','Address 1 - Street','Address 1 - City','Address 1 - PO Box','Address 1 - Region','Address 1 - Postal Code','Address 1 - Country','Address 1 - Extended Address']

# Open Data file
df = pd.read_excel(DATA_FILE_NAME)

# Open Output File
with open(OUTPUT_FILE_NAME, 'w', newline='') as writefile:
    writer = csv.DictWriter(writefile, fieldnames=FIELDNAMES)
    writer.writeheader()

    # Iterate through the data
    for _, row in df.iterrows():
        # If the number consists of only digits, pandas considers it as a float
        # Thus, convert to int before writing to the file
        if IS_NAME_SINGLE_FIELD:
            nameList = row[FULL_NAME_FIELD].split()
            first_name = nameList[0]
            if len(nameList) == 1:
                last_name = "NULL"
            else:
                last_name = nameList[1]
        else:
            first_name = row[FIRST_NAME_FIELD].strip()
            last_name = row[LAST_NAME_FIELD].strip()
        if (type(row[PHONE_NUMBER_FIELD])) in [float, int]:
            # If the number is a 10 digit number, it can be directly written to the file
            if row[PHONE_NUMBER_FIELD] < 10**10 - 1:
                writer.writerow({
                    "Name": f'{IDENTIFIER_STR} {first_name} {last_name}',
                    "Given Name": f'{IDENTIFIER_STR} {first_name}',
                    "Family Name": last_name,
                    "Phone 1 - Type": "Mobile",
                    "Phone 1 - Value": f'+91 {int(row[PHONE_NUMBER_FIELD])}',
                })
            # If the number is a float and is greater than 10 digits, it needs to be converted to a string
            else:
                phone = str(int(row[PHONE_NUMBER_FIELD]))
                phone = '+' + phone[:2] + ' ' + phone[2:]
                writer.writerow({
                    "Name": f'{IDENTIFIER_STR} {first_name} {last_name}',
                    "Given Name": f'{IDENTIFIER_STR} {first_name}',
                    "Family Name": last_name,
                    "Phone 1 - Type": "Mobile",
                    "Phone 1 - Value": phone,
                })
        # If the number contains spaces or special characters, pandas considers it as a string
        else:
            phone = row[PHONE_NUMBER_FIELD]

            # If the number contains a '+' sign, it will be considered as an expression in CSV
            if phone[0] == '+' and phone.count(' ') == 0:
                phone = phone[:3] + ' ' + phone[3:]
            writer.writerow({
                "Name": f'{IDENTIFIER_STR} {first_name} {last_name}',
                "Given Name": f'{IDENTIFIER_STR} {first_name}',
                "Family Name": last_name,
                "Phone 1 - Type": "Mobile",
                "Phone 1 - Value": phone,
            })
