################################################################################
# Autotriage ########################################### Created By: Ian Moyer #
################################################################################
# Required Operating System: Linux (Debian/Ubuntu recommended) amd64 (NO x32!) #
# !! THIS SCRIPT IS PLATFORM DEPENDENT AND WILL NOT RUN ON WINDOWS OR MACOS !! #
# Required Python Version =< 3.9.2                                             #
# !! THIS SCRIPT WILL NOT RUN ON OLDER PYTHON VERSIONS! IT HAS DEPENDENCIES... #
# ...THAT DO NOT HAVE ANY COMPATIBLE PACKAGES ON OLDER PYTHON VERSIONS!     !! #
# Dependencies:                                                                #
#    * tkinter: apt-get install python3-tk                                     #
#    * tksnack: apt-get install python3-tksnack                                #
#    * selenium: pip install selenium                                          #
#    * Faker: pip install Faker                                                #
################################################################################
# Imports ######################################################################
################################################################################
import os
import time
import random
import base64
import warnings
import tkinter as tk
import tkSnack
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from faker import Faker
################################################################################
# Configurable Variables #######################################################
################################################################################
# You must change these variables to the proper values for your store! #########
# DO NOT INCLUDE ANY CREDENTIALS WHEN UPLOADING TO GITHUB!!!!!!!!!!!!!!!!!!!!! #
# TODO: Add a config package that reads credentials from an INI file that is.. #
# .. encrypted using a master password that would be set using a setup script. #
################################################################################
fixtUsername = "cHV0IHlvdXIgYmFzZTY0IHRleHQgaGVyZQ==" # base64 only, no plaintext!
fixtMagicWord = "cHV0IHlvdXIgYmFzZTY0IHRleHQgaGVyZQ==" # base64 only, no plaintext!
rqUsername = "cHV0IHlvdXIgYmFzZTY0IHRleHQgaGVyZQ==" # base64 only, no plaintext!
rqMagicWord = "cHV0IHlvdXIgYmFzZTY0IHRleHQgaGVyZQ==" # base64 only, no plaintext!
assignedTech = "cHV0IHlvdXIgYmFzZTY0IHRleHQgaGVyZQ==" # base64 only, no plaintext!
#
# TODO: Make the Selenium Select() class work with RepairQ login elements so  ..
# we can look for the text of the address and not count arrow down presses.
#
rqAddrDownArrowCount = (Keys.ARROW_DOWN * 465) # You must count the number of ..
# down arrow presses it takes to get the your store address at the RepairQ    ..
# login screen for this value!
################################################################################
# Variables ####################################################################
################################################################################
ticketQueue = []
#
# TODO: Build out a customer email generator.
#
email = "decline@customer.com"
doTickets = True
mode = None
tName = None
tIMEI = None
tPhoneNumber = None
tTicketType = None
clearInput = Keys.BACK_SPACE * 50
warnings.filterwarnings("ignore", category=DeprecationWarning) # Fix for deprecation warning in the temrinal output when Selenium's driver starts.
genny = Faker()
driverLocation = os.getcwd() + r"/chromedriver"
################################################################################
# Utility Functions ############################################################
################################################################################
def genImei(): # Random IMEI function starting with 35 (for US carriers)
    return str(random.randint(350000000000000,359999999999999))

def genName(): # Random name wrapper function for Faker package.
    return genny.first_name() + " " + genny.last_name()

def genPhoneNumber(): # Random phone number function weighted by area code.
    weight = random.randint(1,7) # 7 Weights for a 5/1 weighted randomness ratio.
    if weight == 1: # (1-5 Weight)
        area = "813"

    elif weight == 2: # (1-5 Weight)
        area = "352"

    else: # (5-1 Weight)
        area = "727"

    return area + str(random.randint(1000000,9999999)) # BUGFIX: Start at 1000000 and not 0000000 due to python striping off the preceding zeroes.

def genTicketType():
    weight = random.randint(1,7) # 7 Weights for a 5/1 weighted randomness ratio.
    output = None
    if weight == 1: # (1-5 Weight)
        output = "Charge Port Cleaning"

    elif weight == 2: # (1-5 Weight)
        output = "App Troubleshooting"

    else: # (5-1 Weight)
        output = "Data Transfer"

    return output

def showMessage(msg, title=None):
   if title is None:
       title = "Action required!"

   root = tk.Tk()
   tkSnack.initializeSnack(root)
   snd = tkSnack.Sound()
   snd.read(os.getcwd() + '/alertbox.wav')
   snd.play(blocking=1)
   root.overrideredirect(1)
   root.withdraw()
   root.attributes("-topmost", True)
   result = messagebox.showinfo(title, msg)
   root.destroy()
   return result

################################################################################
# // Entry Point // Entry Point // Entry Point // Entry Point // Entry Point / #
# // Entry Point // Entry Point // Entry Point // Entry Point // Entry Point / #
# // Entry Point // Entry Point // Entry Point // Entry Point // Entry Point / #
################################################################################
# Setup Menu ###################################################################
################################################################################
os.system('clear')
print("Autotriage Setup\n\n")
#
# TODO: Modify the bulk mode to allow setup for manual bulk tickets by input entry of info or by reading from a CSV file.
#
while mode != "single" or mode != "bulk":
    mode = input("Do you want to enter info for a single ticket or setup generation of bulk tickets?\n\n- Type \'single\' or \'s\' to set up single tickets.\n    ^ This mode allows for manual entry of IMEI, name, phone number, and ticket type.\n\n- Type \'bulk\' or \'b\' to set up bulk ticket creation with generated info.\n    ^ This mode generates the info automatically for each ticket made and does not allow manual entry.\n\nMode of operation: ")
    if (mode.upper() == "SINGLE") or (mode.upper() == "S"):
        print("Single mode of operation was selected.")
        mode = "single"
        break

    elif (mode.upper() == "BULK") or (mode.upper() == "B"):
        print("Bulk mode of operation was selected.")
        mode = "bulk"
        break

    else: # Default State
        print("\nYou did not select a mode of operation. Please select single or bulk.")
        mode = None

if (mode == "single"):
    #
    # TODO: Add input validation.
    #
    tIMEI = input("\nEnter the IMEI: ")
    tName = input("\nEnter the customer's name: ")
    #
    # TODO: Add input validation.
    #
    tPhoneNumber = input("\nEnter the customer's phone number: ")
    #
    # TODO: Add input validation.
    #
    tTicketType = input("\nWhat is the type for this ticket?\n\nAvailable options are:\n    -Data Transfer (type \'d\' or \'data\')  <  DEFAULT OPTION\n    -App Troubleshooting (type \'a\' or \'app\')\n    -Charge Port Cleaning (type \'c\' or \'charge\')\n\nNote: No input or input that is invalid will default to Data Transfer ticket type.\n\nEnter the ticket type: ")
    if (tTicketType.upper() == "a") or (tTicketType.upper() == "app"):
        tTicketType = "App Toubleshooting"

    if (tTicketType.upper() == "c") or (tTicketType.upper() == "charge"):
        tTicketType = "Charge Port Cleaning"

    else:
        tTicketType = "Data Transfer"

    print("Ticket Type: " + tTicketType)
    #
    # TODO: Modify this along with the rest of the prompt to allow going back and chaning a ticket.
    #
    input("\nPlease double check the above ticket info.\n\nPress [Enter] to continue or press [Control]+C to exit in the case an error was made.")
    ticket = []
    ticket.append(tIMEI)
    ticket.append(tName)
    ticket.append(tPhoneNumber)
    ticket.append(tTicketType)
    ticketQueue.append(ticket)
    tName = None
    tIMEI = None
    tPhoneNumber = None
    tTicketType = None

elif (mode == "bulk"):
    ticketCount = input("\nEnter the number of tickets to generate: ")
    print("\n")
    ticketQueue = []
    for x in range(int(ticketCount)): # For each ticket in the queue
        ticket = []
        ticket.append(genImei())
        ticket.append(genName())
        ticket.append(genPhoneNumber())
        ticket.append(genTicketType())
        ticketQueue.append(ticket)

print("\nThe web browser will now open to begin ticket creation.")
time.sleep(2)
print("\n")
driver = webdriver.Chrome(executable_path=driverLocation)
driver.maximize_window()
wait = WebDriverWait(driver, 15)
actions = ActionChains(driver)
time.sleep(2)
driverBgOptions = Options() # Setup options object for a second driver.
driverBgOptions.headless = True # Set the second driver to headless mode. (No window is displayed)
driverBg = webdriver.Chrome(executable_path=driverLocation, options=driverBgOptions) # Setup the object to access the second driver.
driverBg.maximize_window() # Expand the viewport so we can actually hit search.
waitBg = WebDriverWait(driverBg, 15) # Setup wait for expected condition object for the second driver. Timeout of 10.
################################################################################
# Login ########################################################################
################################################################################
print("\nLogging in to Fixt...")
driver.get("https://hq.fixt.co/claims/create?group=4910cbdf-91c2-f131-0991-311276247f79&msisdn=GRxD7%2FgrAucti9CUTpWENX962FO1hn6ucRA5H27JoVuGdxMC1%2BLB4gnhMruRC2HQyIamblxg9BWuSURi8W4KWCwR%2FED5XPxnIEg9kGgb5lIpRrmo1Nwsxf6R3VUxppSakh4rQ0a6E%2Bn9IAlmSP8yAA3Wj0JL9JTeaef7")
#
# TODO: Replace all of these ExpectedCondition tests with a full on test loop with error handling....
#
wait.until(EC.visibility_of_element_located((By.ID, "1-email"))).send_keys("na@t-mobile.com")
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "auth0-lock-submit"))).click()
wait.until(EC.visibility_of_element_located((By.ID, "okta-signin-username"))).send_keys(base64.b64decode(fixtUsername).decode("ascii"))
wait.until(EC.visibility_of_element_located((By.ID, "okta-signin-submit"))).click()
wait.until(EC.visibility_of_element_located((By.ID, "input75"))).send_keys(base64.b64decode(fixtMagicWord).decode("ascii"))
wait = WebDriverWait(driver, 1)
#
# TODO: Replace this hacked together test loop with a full on test loop function with error handling...
#
try:
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "button button-primary"))).click()

except:
    try:
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "o-form-button-bar"))).click()

    except:
        try:
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "o-form-button-bar focused-input"))).click()

        except:
            wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/main/div[2]/div/div/form/div[2]/input"))).click()
            pass
        pass

    pass

wait = WebDriverWait(driver, 15)
time.sleep(5)
print("\nLogging in to RepairQ...")
driver.get("https://sosi.repairq.io/site/login")
#
# TODO: Replace all of these ExpectedCondition tests with a full on test loop with error handling....
#
wait.until(EC.visibility_of_element_located((By.ID, "UserLoginForm_username"))).send_keys(base64.b64decode(rqUsername).decode("ascii"))
wait.until(EC.visibility_of_element_located((By.ID, "UserLoginForm_password"))).send_keys(base64.b64decode(rqMagicWord).decode("ascii"))
wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/form/fieldset/div[3]/div/span"))).click()
wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/form/fieldset/div[3]/div/span/span[1]/span"))).send_keys(rqAddrDownArrowCount + Keys.ENTER)
wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/form/fieldset/div[4]/div[2]/button"))).click()
time.sleep(2)
driverBg.get("https://sosi.repairq.io/site/login") # Start RQ login process for the second driver.
#
# TODO: Replace all of these ExpectedCondition tests with a full on test loop with error handling....
#
waitBg.until(EC.visibility_of_element_located((By.ID, "UserLoginForm_username"))).send_keys(base64.b64decode(rqUsername).decode("ascii"))
waitBg.until(EC.visibility_of_element_located((By.ID, "UserLoginForm_password"))).send_keys(base64.b64decode(rqMagicWord).decode("ascii"))
waitBg.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/form/fieldset/div[3]/div/span"))).click()
waitBg.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/form/fieldset/div[3]/div/span/span[1]/span"))).send_keys((Keys.ARROW_DOWN * 465) + Keys.ENTER)
waitBg.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/form/fieldset/div[4]/div[2]/button"))).click()
################################################################################
# Fixt Ticket Creation #########################################################
################################################################################
for ticket in ticketQueue: # For each ticket in the queue
    tIMEI = ticket[0]
    tName = ticket[1]
    tPhoneNumber = ticket[2]
    tTicketType = ticket[3]
    time.sleep(5)
    print("\nCreating the ticket in Fixt...")
    driver.get("https://hq.fixt.co/claims/create?group=4910cbdf-91c2-f131-0991-311276247f79&msisdn=GRxD7%2FgrAucti9CUTpWENX962FO1hn6ucRA5H27JoVuGdxMC1%2BLB4gnhMruRC2HQyIamblxg9BWuSURi8W4KWCwR%2FED5XPxnIEg9kGgb5lIpRrmo1Nwsxf6R3VUxppSakh4rQ0a6E%2Bn9IAlmSP8yAA3Wj0JL9JTeaef7")
    time.sleep(10)
    #
    # TODO: Replace all of these ExpectedCondition tests with a full on test loop with error handling....
    #
    driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/div/div/a"))).click()
    time.sleep(2)
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/div/div/form/div/label[2]"))).click()
    time.sleep(2)
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/div/div/form/div/div/a"))).click()
    time.sleep(2)
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/div/div/form/div[1]/div[2]/div/div/div[3]/a"))).click()
    time.sleep(3)
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/div/div/form/span[1]/div/div[1]/div/div"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "react-select-3-input"))).send_keys("T-Mobile" + Keys.ENTER)
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/div/div/form/span[2]/div/div[1]/div/div"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "react-select-4-input"))).send_keys("64GB" + Keys.ENTER)
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/div/div/form/span[3]/div/div[1]/input"))).send_keys(tIMEI)
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/div/div/form/span[4]/div/div[1]/input"))).send_keys(tPhoneNumber)
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[3]/div/div[2]/div/div[1]/a"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/div/div/form/div/div[2]/textarea"))).send_keys("Diagnostic")
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[3]/div/div[2]/div/div[1]/a"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/div/div/form/div[1]/div[1]/div/div/div[1]/input"))).send_keys("33100 US")
    wait.until(EC.visibility_of_element_located((By.ID, "ChIJUZZbr5zywogRHfMHI-9CgmU"))).click()
    time.sleep(0.5) # This really needs to be changed to a test loop eventually for stability.
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[3]/div/div[2]/div/div[1]/a"))).click()
    time.sleep(0.5) # This really needs to be changed to a test loop eventually for stability.
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/div/div/form/div/div[1]/label[1]"))).click()
    time.sleep(0.5) # This really needs to be changed to a test loop eventually for stability.
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[3]/div/div[2]/div/div[1]/a"))).click()
    time.sleep(0.5) # This really needs to be changed to a test loop eventually for stability.
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/div/div[1]/div[2]/div[3]/div[2]/div[1]/label"))).click()
    time.sleep(0.5) # This really needs to be changed to a test loop eventually for stability.
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[3]/div/div[2]/div/div[1]/a"))).click()
    time.sleep(0.5) # This really needs to be changed to a test loop eventually for stability.
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/div/div/form/div/div[1]/div[1]/input"))).send_keys(clearInput + tName)
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/div/div/form/div/div[2]/label/input"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/div/div/form/div/div[3]/div[1]/input"))).send_keys("decline@customer.com")
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/div/div/form/div/div[4]/div[1]/input"))).send_keys(tPhoneNumber)
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[3]/div/div[2]/div/div[1]/a"))).click()
    time.sleep(0.5) # This really needs to be changed to a test loop eventually for stability.
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/div[1]/div/div/form/a"))).click()
    time.sleep(5)
################################################################################
# Standby for Ticket Creation ##################################################
################################################################################
#
# TODO: Improve the waiting screen with CSS, more memes, and statistics from the ticket queue/current ticket as well as faster performance...
#

    driver.get("file://" + os.getcwd() + r"/standby.html") # Render the standby page.
    time.sleep(5)
    driverBg.get("https://sosi.repairq.io/site/login") # Start RQ login process for the second driver.
    time.sleep(5)
    waitBg = WebDriverWait(driverBg, 15) # Setup wait for expected condition object for the second driver. Timeout of 10.
    waitBg.until(EC.visibility_of_element_located((By.ID, "UserLoginForm_username"))).send_keys(base64.b64decode(rqUsername).decode("ascii"))
    waitBg.until(EC.visibility_of_element_located((By.ID, "UserLoginForm_password"))).send_keys(base64.b64decode(rqMagicWord).decode("ascii"))
    waitBg.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/form/fieldset/div[4]/div[2]/button"))).click()
    driverBg.get("https://sosi.repairq.io/ticket")
    # Loop to detect if there is a ticket result for the ticket we just made in RQ.
    time.sleep(15) # Required 15s wait to avoid a race condition between the url check and the web driver.
    noTicket = True # Set a flag for exiting the loop.
    for i in range(60):
        if noTicket and (driverBg.current_url == "https://sosi.repairq.io/ticket"):
            noTicket = False # Reset the flag for the test.
            try:
                waitBg.until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"mainModelList\"]/tbody/tr"))).click()

            except:
                noTicket = True
                driverBg.get("https://sosi.repairq.io/ticket")

        else: # If there is a ticket
            break # Exit the loop

################################################################################
# RepairQ Login ################################################################
################################################################################
    driver.get("https://sosi.repairq.io/site/login")
    #
    # TODO: Replace all of these ExpectedCondition tests with a full on test loop with error handling....
    #
    wait.until(EC.visibility_of_element_located((By.ID, "UserLoginForm_username"))).send_keys(base64.b64decode(rqUsername).decode("ascii"))
    wait.until(EC.visibility_of_element_located((By.ID, "UserLoginForm_password"))).send_keys(base64.b64decode(rqMagicWord).decode("ascii"))
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/form/fieldset/div[4]/div[2]/button"))).click()
    time.sleep(10)
################################################################################
# RepairQ Ticket Completion ####################################################
################################################################################
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div[1]/div[2]/div/form/div/input"))).send_keys(tIMEI) # tIMEI
    wait.until(EC.visibility_of_element_located((By.ID, "quickSearchBtn"))).click()
    time.sleep(2) # This really needs to be changed to a test loop eventually for stability.
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div[2]/div[3]/div[2]/div[2]/div/div[2]/div[1]/div[4]/a"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div[2]/div[1]/div/form/div/div/div[3]/div[2]/div[5]/div[3]/a[2]"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div[2]/div[1]/div/form/div/div/div[3]/div[2]/div[5]/div[3]/a[2]"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/form/div[2]/div[2]/div[2]/div[1]/div[7]/div/div/label"))).click()
    time.sleep(0.5) # This really needs to be changed to a test loop eventually for stability.
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/form/div[3]/button[3]"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div[2]/div[1]/div/form/div/div/div[3]/div[2]/div[5]/div[3]/a[3]"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div[2]/div[1]/div/form/div/div/div[3]/div[2]/div[5]/div[3]/a[1]"))).click()
    showMessage("Please select the device make/model.\n\nNOTE: YOU MUST ONLY SELECT A SAMSUNG DEVICE!!! Other devices are incompatible with auto triage.")
    #
    # TODO: Replace this hacked together test loop with a full on test loop function with error handling...
    #
    continueTesting = True
    fail = True
    while continueTesting:
        time.sleep(0.5)
        if fail:
            fail = False
            try:
                if "Find a match for" in driver.find_element(By.XPATH, "//*[@id=\"new-device-form\"]/fieldset/div[1]/h3").text:
                    continueTesting = False

            except:
                fail = True
                pass

        else:
            continueTesting = False

    continueTesting = True
    fail = True

    while continueTesting:
        time.sleep(0.5)
        if fail:
            fail = False
            try:
                if tIMEI in driver.find_element(By.XPATH, "//*[@id=\"claim-device-serial\"]").text:
                    continueTesting = False

            except:
                fail = True
                pass

        else:
            continueTesting = False
    time.sleep(2)
    wait.until(EC.visibility_of_element_located((By.ID, "save-description"))).send_keys(tTicketType)
    Select(wait.until(EC.visibility_of_element_located((By.ID, "save-carrier")))).select_by_visible_text("T-Mobile")
    wait.until(EC.visibility_of_element_located((By.ID, "save-password"))).send_keys("N/A")
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div[2]/div[1]/div/form/div/div/div[3]/div[2]/div[5]/div[3]/a[2]"))).click()
    time.sleep(10) # Arbitrary wait to avoid a race condition.
    #
    # TODO: Replace this hacked together test loop with a full on test loop function with error handling...
    #
    continueTesting = True
    fail = True
    tries = 20
    while continueTesting:
        time.sleep(0.5)
        if fail:
            tries = tries - 1
            fail = False
            try:
                # Was a loaner device issued? Modal Box (No Radio Button)
                driver.find_element(By.XPATH, "//*[@id=\"customFieldsEdit\"]/fieldset/div[2]/div/input").click()

            except:
                if tries != 0:
                    fail = True

                pass

        else:
            continueTesting = False
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"customFieldEditModal\"]/div[3]/a[2]"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"claim-loaner-device-sp\"]/fieldset/div/div/label[2]/input"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"claim-walkthrough-modal\"]/div[3]/a[2]"))).click()
    actions.move_to_element(driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[1]/div/form/div/div/div[3]/div[8]/div/div[1]")).perform()
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div[2]/div[1]/div/form/div/div/div[3]/div[7]/div[3]/div[2]/div[6]/div/table/tbody/tr[2]/td[10]/div/a"))).click()
    #
    # TODO: Replace this hacked together test loop with a full on test loop function with error handling...
    #
    continueTesting = True
    fail = True
    while continueTesting:
        time.sleep(0.5)
        if fail:
            fail = False
            try:
                driver.find_element(By.XPATH, "//*[@id=\"inventoryStatusModal\"]/div[3]/a").click()
            except:
                fail = True
                pass

        else:
            continueTesting = False

    if tTicketType == "Charge Port Cleaning":
        wait.until(EC.visibility_of_element_located((By.ID, "search-keyword"))).send_keys("GENERAL")

    elif tTicketType == "App Troubleshooting":
        wait.until(EC.visibility_of_element_located((By.ID, "search-keyword"))).send_keys("GENERAL")

    else:
        wait.until(EC.visibility_of_element_located((By.ID, "search-keyword"))).send_keys("DEVICE")

    actions.move_to_element(driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[1]/div/form/div/div/div[3]/div[8]/div/div[1]")).perform()
    #
    # TODO: Replace this hacked together test loop with a full on test loop function with error handling...
    #
    continueTesting = True
    fail = True
    while continueTesting:
        time.sleep(0.5)
        if fail:
            fail = False
            try:
                driver.find_element(By.XPATH, "/html/body/ul/li").click()
            except:
                fail = True
                pass

        else:
            continueTesting = False

    Select(wait.until(EC.visibility_of_element_located((By.ID, "TicketForm_assignee_id")))).select_by_visible_text(base64.b64decode(assignedTech).decode("ascii"))
    wait.until(EC.visibility_of_element_located((By.ID, "Btnpending_approval"))).click()
    time.sleep(8)
    #
    # TODO: Replace this hacked together test loop with a full on test loop function with error handling...
    #
    continueTesting = True
    fail = True
    while continueTesting:
        time.sleep(0.5)
        if fail:
            fail = False
            try:
                driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[1]/div/form/div/div/div[3]/div[2]/div[5]/div[3]/a[2]").click()
            except:
                fail = True
                pass

        else:
            continueTesting = False

    wait.until(EC.visibility_of_element_located((By.ID, "Btnin_repair"))).click()
    time.sleep(2)
    #
    # TODO: Replace this hacked together test loop with a full on test loop function with error handling...
    #
    continueTesting = True
    fail = True
    while continueTesting:
        time.sleep(0.5)
        if fail:
            fail = False
            try:
                Select(driver.find_element(By.XPATH, "/html/body/div[6]/div[2]/form/fieldset/div[1]/div/select")).select_by_visible_text("English")

            except:
                fail = True
                pass

        else:
            continueTesting = False

    time.sleep(2)
    #
    # TODO: Replace this hacked together test loop with a full on test loop function with error handling...
    #
    continueTesting = True
    fail = True
    while continueTesting:
        time.sleep(0.5)
        if fail:
            fail = False
            try:
                driver.find_element(By.XPATH, "//*[@id=\"customFieldsEdit\"]/fieldset/div[4]/div/input").send_keys(tName)
            except:
                fail = True
                pass

        else:
            continueTesting = False

    #
    # TODO: Replace this hacked together test loop with a full on test loop function with error handling...
    #
    continueTesting = True
    fail = True
    while continueTesting:
        time.sleep(0.5)
        if fail:
            fail = False
            try:
                driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/a[2]").click()
            except:
                fail = True
                pass

        else:
            continueTesting = False

    time.sleep(2)
    #
    # TODO: Replace this hacked together test loop with a full on test loop function with error handling...
    #
    continueTesting = True
    fail = True
    while continueTesting:
        time.sleep(0.5)
        if fail:
            fail = False
            try:
                signature = ActionChains(driver)\
                    .click_and_hold(driver.find_element(By.XPATH, "//*[@id=\"modal-signature\"]/div[2]/div[2]/div/canvas"))\
                    .move_by_offset(-10, -15)\
                    .move_by_offset(20, 32)\
                    .move_by_offset(10, 25)\
                    .release()

                signature.perform()

            except:
                fail = True
                pass

        else:
            continueTesting = False

    #
    # TODO: Replace this hacked together test loop with a full on test loop function with error handling...
    #
    continueTesting = True
    fail = True
    while continueTesting:
        time.sleep(0.5)
        if fail:
            fail = False
            try:
                driver.find_element(By.XPATH, "//*[@id=\"modal-signature\"]/div[2]/div[3]/button[2]").click()
            except:
                fail = True
                pass

        else:
            continueTesting = False

    #
    # TODO: Replace this hacked together test loop with a full on test loop function with error handling...
    #
    continueTesting = True
    fail = True
    while continueTesting:
        time.sleep(0.5)
        if fail:
            fail = False
            try:
                driver.find_element(By.XPATH, "//*[@id=\"form-sign-success\"]/div/div/button").click()
            except:
                fail = True
                pass

        else:
            continueTesting = False

    #
    # TODO: Replace this hacked together test loop with a full on test loop function with error handling...
    #
    continueTesting = True
    fail = True
    while continueTesting:
        time.sleep(0.5)
        if fail:
            fail = False
            try:
                driver.find_element(By.XPATH, "//*[@id=\"customFieldsEdit\"]/fieldset/div[1]/div/label[2]/input").click()
            except:
                fail = True
                pass

        else:
            continueTesting = False

    #
    # TODO: Replace this hacked together test loop with a full on test loop function with error handling...
    #
    continueTesting = True
    fail = True
    while continueTesting:
        time.sleep(0.5)
        if fail:
            fail = False
            try:
                driver.find_element(By.XPATH, "//*[@id=\"customFieldEditModal\"]/div[3]/a[2]").click()
            except:
                fail = True
                pass

        else:
            continueTesting = False

    #
    # TODO: Replace this hacked together test loop with a full on test loop function with error handling...
    #
    continueTesting = True
    fail = True
    while continueTesting:
        time.sleep(0.5)
        if fail:
            fail = False
            try:
                signature = ActionChains(driver)\
                    .click_and_hold(driver.find_element(By.XPATH, "//*[@id=\"modal-signature\"]/div[2]/div[2]/div/canvas"))\
                    .move_by_offset(-10, -15)\
                    .move_by_offset(20, 32)\
                    .move_by_offset(10, 25)\
                    .release()

                signature.perform()

            except:
                fail = True
                pass

        else:
            continueTesting = False

    #
    # TODO: Replace this hacked together test loop with a full on test loop function with error handling...
    #
    continueTesting = True
    fail = True
    while continueTesting:
        time.sleep(0.5)
        if fail:
            fail = False
            try:
                driver.find_element(By.XPATH, "//*[@id=\"modal-signature\"]/div[2]/div[3]/button[2]").click()
            except:
                fail = True
                pass

        else:
            continueTesting = False

    #
    # TODO: Replace this hacked together test loop with a full on test loop function with error handling...
    #
    continueTesting = True
    fail = True
    while continueTesting:
        time.sleep(0.5)
        if fail:
            fail = False
            try:
                driver.find_element(By.XPATH, "//*[@id=\"form-sign-success\"]/div/div/button").click()
            except:
                fail = True
                pass

        else:
            continueTesting = False

    #
    # TODO: Replace this hacked together test loop with a full on test loop function with error handling...
    #
    continueTesting = True
    fail = True
    while continueTesting:
        time.sleep(0.5)
        if fail:
            fail = False
            try:
                driver.find_element(By.XPATH, "//*[@id=\"claim-loaner-device-dr\"]/fieldset/div/div/label[2]/input").click()
            except:
                fail = True
                pass

        else:
            continueTesting = False

    #
    # TODO: Replace this hacked together test loop with a full on test loop function with error handling...
    #
    continueTesting = True
    fail = True
    while continueTesting:
        time.sleep(0.5)
        if fail:
            fail = False
            try:
                driver.find_element(By.XPATH, "//*[@id=\"claim-walkthrough-modal\"]/div[3]/a[2]").click()
            except:
                fail = True
                pass

        else:
            continueTesting = False

    #
    # TODO: Replace this hacked together test loop with a full on test loop function with error handling...
    #
    continueTesting = True
    fail = True
    while continueTesting:
        time.sleep(0.5)
        if fail:
            fail = False
            try:
                driver.find_element(By.ID, "Btnready_for_pickup").click()
            except:
                fail = True
                pass

        else:
            continueTesting = False

    time.sleep(2)
    #
    # TODO: Replace this hacked together test loop with a full on test loop function with error handling...
    #
    continueTesting = True
    fail = True
    while continueTesting:
        time.sleep(0.5)
        if fail:
            fail = False
            try:
                driver.find_element(By.XPATH, "//*[@id=\"claim-walkthrough-modal\"]/div[3]/a[2]").click()
            except:
                fail = True
                pass

        else:
            continueTesting = False

    time.sleep(5)

################################################################################
# Cleanup ######################################################################
################################################################################
driver.close()
driverBg.close()
inputReturn = input("\n\nTicket generation is complete.\n\nPress any key to exit...")
