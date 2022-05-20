import csv
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
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
        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[6]/div[2]/div[1]/div[2]/div/div'))).click()
        # If the user is not the Group Admin, the button will not be present
        except:
            print("\nYou are not the Group Admin!")
            self.driver.quit()
            exit(1)

        print("\nList of Missing Names")
        print("---------------------")
        # Type each name and click their respective name tile
        for name in self.listNames:
            searchbar = self.driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div/div[1]/div/label/div/div[2]')
            searchbar.send_keys(name)
            try:
                nameTile = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div/*//*[@title="{name}"]')))
                nameTile.click()
            except:
                print(name)
            searchbar.send_keys(Keys.CONTROL + "a")
            searchbar.send_keys(Keys.DELETE)

        print()
        # Click the Tick Button
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@data-icon="checkmark-medium"]'))).click()

        # Click the Confirm Button
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/div[2]/div'))).click()

        try:
            # For people who need to be sent invite links, click the Invite Link button
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div[2]/div[2]/div/div'))).click()

            # Click the Invite Button
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div/div/span/div/span'))).click()
        except:
            # If the element is never clickable, then there are no users to be manually invited
            pass

    # Exit the bot gracefully
    def exitBot(self):
        self.driver.quit()

waBot = WhatsAppGroupBot()

waBot.readNames(DATA_FILE_NAME)
print("Names read!")

waBot.openWhatsappWeb()
print("Web Interface Opened!")

waBot.openGroup(WA_GROUP_NAME)
print("Group Opened!")

waBot.addMembers()
print("Members Added!")

waBot.exitBot()
print("Bot Exited!")
