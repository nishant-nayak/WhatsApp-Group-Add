# WhatsApp-Group-Add

WhatsApp-Group-Add is a Python script which helps users to add people to a specific WhatsApp group without directly saving their numbers.
Heavily inspired by [CodeChefVIT's implementation](https://github.com/CodeChefVIT/whatsapp-groupadd).

## Usage

1. Clone the Repo and save the Excel Sheet (in `.xlsx` format) in the data folder. Change the filename in [generateGoogleContacts.py](generateGoogleContacts.py) accordingly.

2. Run the following command:
```bash
pip install -r requirements.txt
python generateGoogleContacts.py
```

3. Import the `output.csv` file into your [Google Contacts](https://contacts.google.com/).

4. Run the following command:

```bash
python whatsappGroupAdder.py
```
