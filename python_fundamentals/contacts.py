# Goals
# -----
# [x] add user input validation on search/add (ensure not blank, phone number is numbers/symbols, etc)
# [x] print a message if the user doesn't enter a valid command
# [x] write tests
# [x] store as a faux-CSV:
#     [x] separate each field with a comma when writing
#     [x] split on comma on readin
#     [x] ensure no commas on validating user input
# [x] add email address to data user can save in contacts
#     [x] add email input() in main()
#     [x] add email validation
#     [x] update add_contact()

import re

contacts_file = 'data/contacts.txt'

def add_contact(name, number, email):
    """Appends a new name and number to contacts.txt"""
    with open(contacts_file, "a") as fp:
        fp.write(f"{name}, {number}, {email}\n")

def read_contacts():
    """Adds all the lines from contacts.txt to a variable, removing any commas"""
    with open(contacts_file, "r") as fp:
        contents = fp.read()
    
    text = ""
    for contact in contents.splitlines():
        if contact:
            contact = contact.split(',')
            text += f"{contact[0]} {contact[1]} {contact[2]}\n"
    
    return text

def search_contacts(name):
    """Returns any contact that contains the string entered by user"""
    contents = read_contacts().split("\n")
    text = ""
    for line in contents:
        if name in line.lower():
            text += f"{line}\n"
    if not text:
        text += "You have no contacts with that name. Womp womp.\n"
    else:
        text = "Search results:\n" + text
    return text

def selection_validation(user_pick):
    """Validates the user picked an existing command"""
    if user_pick in ("a", "v", "s", "q", "add", "view", "search", "quit"):
        return True
    return False

def name_validation(name):
    """checks if name is blank"""
    if not name:
        return False
    if "," in name:
        return False
    return True

def number_validation(number):
    """checks if phone number is valid"""

    if not number:
        return False

    #checks for (xxx)xxx-xxxx
    if number[0] == "(":
        if re.search(r"^\({1}[0-9]{3}\){1}[0-9]{3}-{1}[0-9]{4}$", number):
            return True    
    
    #checks for xxx-xxx-xxxx
    if number[3] == "-":
        if re.search(r"^[0-9]{3}-{1}[0-9]{3}-{1}[0-9]{4}$", number):
            return True
    
    #checks for xxxxxxxxxx
    if number.isnumeric() == True:
        if re.search(r"^[0-9]{10}$", number):
            return True
    
    return False

def email_validation(email):
    """Checks if email looks like wildcard@wildcard.wildcard"""
    if re.search(r"^[^@]+@[^@.]+\.[^@.]+$", email):
        return True
    return False

def main():
    """Asks user to selection actions, and executes acordingly"""
    while True:
        selection = input("Would you like to ADD, VIEW, or SEARCH your contacts? QUIT if you are done :)\n").lower()

        if not selection_validation(selection):
            print("\nSorry, that is not one of the options I gave you...")
            continue
        
        if selection in ("q", "quit"):
            print("\nOkay crazy person I love you bye bye.")
            break

        if selection in ("a", "add"):
            new_name = input("\nWhat is the name of the new contact?\n").title()
            
            while not name_validation(new_name):
                new_name = input("\nPlease type the name better:\n").title()

            new_number = input("\nWhat is the phone number of the new contact?\n" \
                            "Please use one of the following formats:\n" \
                            "(xxx)xxx-xxxx\nxxx-xxx-xxxx\nxxxxxxxxxx\n").replace(" ", "")

            while not number_validation(new_number):
                new_number = input("\nPlease ensure you type only numbers, hyphens, parenthesis\n"\
                            "and use one of the following formats:\n"\
                            "(xxx)xxx-xxxx\nxxx-xxx-xxxx\nxxxxxxxxxx\n").replace(" ", "")

            new_email = input("\nWhat is the email adress for the new contact?\n")

            while not email_validation(new_email):
                new_email = input("\nPlease be sure the email is entered correctly:\n")

            add_contact(new_name, new_number, new_email)
        
        if selection in ("v", "view"):
            text = read_contacts()
            print(f"\n{text}")

        if selection in ("s", "search"):
            query_name = input("\nWhich contact would you like to search for?\n").lower()

            while not name_validation(query_name):
                query_name = input("\nPlease type the name better:\n").lower()

            results = search_contacts(query_name)
            print(f"\n{results}")
        
if __name__ == "__main__":
    main()