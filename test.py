import os
import time
import random
import base64
import warnings
from faker import Faker

genny = Faker()
mode = None
ticketQueue = []
doTickets = True
mode = None
tName = None
tIMEI = None
tPhoneNumber = None
tTicketType = None

def genImei():
    return str(random.randint(350000000000000,359999999999999))

def genName():
    return genny.first_name() + " " + genny.last_name()

def genPhoneNumber():
    area = random.randint(1,8)
    if area == 1:
        area = "813"

    elif area == 2:
        area = "352"

    else:
        area = "727"

    return area + str(random.randint(1000000,9999999))

def genTicketType():
    weights = random.randint(1,8)
    output = None
    if weights == 1: # (1-5 Weight)
        output = "Charge Port Cleaning"

    elif weights == 2: # (1-5 Weight)
        output = "App Troubleshooting"

    else: # (5-1 Weight)TW95ZXIsIElhbg==
        output = "Data Transfer"

    return output

os.system('clear')
print("Autotriage Setup\n\n")
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
    print("Single mode of operation selected.")
    tIMEI = input("\nEnter the IMEI: ") # TODO: Add input validation.
    tName = input("\nEnter the customer's name: ") # TODO: Add input validation.
    tPhoneNumber = input("\nEnter the customer's phone number: ") # TODO: Add input validation.
    tTicketType = input("\nWhat is the type for this ticket?\n\nAvailable options are:\n    -Data Transfer (type \'d\' or \'data\')  <  DEFAULT OPTION\n    -App Troubleshooting (type \'a\' or \'app\')\n    -Charge Port Cleaning (type \'c\' or \'charge\')\n\nNote: No input or input that is invalid will default to Data Transfer ticket type.\n\nEnter the ticket type: ")
    if (tTicketType.upper() == "a") or (tTicketType.upper() == "app"):
        tTicketType = "App Toubleshooting"

    if (tTicketType.upper() == "c") or (tTicketType.upper() == "charge"):
        tTicketType = "Charge Port Cleaning"

    else:
        tTicketType = "Data Transfer"

    print("Ticket Type: " + tTicketType)
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
    print("Bulk mode of operation selected.")
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
        print("Ticket " + str(x+1) + " of " + ticketCount + ": " + str(ticket))

for ticket in ticketQueue: # For each ticket in the queue
    tIMEI = ticket[0]
    tName = ticket[1]
    tPhoneNumber = ticket[2]
    tTicketType = ticket[3]
