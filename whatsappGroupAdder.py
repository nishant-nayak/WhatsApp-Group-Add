import csv
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#### CONFIG START ####
# File name that contains the data of Names/Numbers
DATA_FILE_NAME = "data/output.csv"

# WhatsApp Group Name (ensure that the group is pinned!)
WA_GROUP_NAME = "Testing WA Bot"
#### CONFIG END ####

class WhatsAppGroupBot:
    # Initialize the driver
    def __init__(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.listNames = []

    # Read the names of the members from the CSV file
    def readNames(self, filename):
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.listNames.append(row["Name"])

    # Open the WhatsApp Web Interface
    def openWhatsappWeb(self):
        self.driver.get('https://web.whatsapp.com/')
        try:
            # Check if QR Code is present on the screen
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div/div[2]/div[1]/div/div[2]/div/canvas'))
            )
            print("Not Logged In!")

            # Program halts for input to continue
            input("Press Enter to continue...")
        except:
            # Check if the sidebar is present (should be present only when logged in)
            try:
                self.driver.find_element(By.XPATH, '//*[@id="side"]')
            except:
                print("Some Error Occurred!")
                self.driver.quit()
                exit(1)

    # Open the specified group
    def openGroup(self, groupName):
        try:
            self.driver.find_element(By.XPATH, f'//*[@title="{groupName}"]').click()
        except:
            print("WhatsApp group doesn't exist or is not Pinned!")
            input("Press Enter to continue...")
            self.openGroup(groupName)

    # Add members to the group
    def addMembers(self):
        # Click the Group name
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]/header/div[2]/div[1]/div/span'))).click()

        # Click the Add Members button
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[6]/div[2]/div[1]/div[2]/div/div'))).click()

        # Type each name and click their respective name tile
        for name in self.listNames:
            searchbar = self.driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div/div[1]/div/label/div/div[2]')
            searchbar.send_keys(name)
            nameTile = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div/*//*[@title="{name}"]')))
            nameTile.click()

        # Click the Tick Button
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@data-icon="checkmark-medium"]'))).click()

        # Click the Confirm Button
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, ' //*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div[2]/div[2]/div'))).click()

    # Exit the bot gracefully
    def exitBot(self):
        print("Job Done!")
        self.driver.quit()

waBot = WhatsAppGroupBot()

waBot.readNames(DATA_FILE_NAME)
waBot.openWhatsappWeb()
waBot.openGroup(WA_GROUP_NAME)
waBot.addMembers()
waBot.exitBot()
