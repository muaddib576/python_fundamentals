# Goals
# -----
# [x] add user input validation on search/add (ensure not blank, phone number is numbers/symbols, etc)
# [x] print a message if the user doesn't enter a valid command
# [x] write tests
# [x] store as a faux-CSV:
#     [x] separate each field with a comma when writing
#     [x] split on comma on readin
#     [x] ensure no commas on validating user input
# [ ] add email address to data user can save in contacts
#     [ ] add email input() in main()
#     [ ] add email validation
#     [ ] update add_contact()

contacts_file = 'data/contacts.txt'

def add_contact(name, number):
    """Appends a new name and number to contacts.txt"""
    with open(contacts_file, "a") as fp:
        fp.write(f"{name}, {number}\n")

def read_contacts():
    """Adds all the lines from contacts.txt to a variable, removing any commas"""
    with open(contacts_file, "r") as fp:
        contents = fp.read()
    
    contents = contents.split('\n')
    text = ""
    for contact in contents:
        if contact:
            contact = contact.split(',')
            text += f"{contact[0]} {contact[1]}\n"
    
    return text

def search_contacts(name):
    """Returns any contact that contains the string entered by user"""
    contents = read_contacts().split("\n")
    text = "Search results:\n"
    for line in contents:
        if name in line.lower():
            text += f"{line}\n"
    if not text:
        text += "You have no contacts with that name. Womp womp."
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
    # it seems to me like this could be a project in itself, so im just going to do it lazy and *shudder* trust the user a bit
    nums = ""
    for x in number:
        if x in ("(", ")", "-"):
            continue
        nums += x
    
    try:
        int(nums)
    except ValueError:
        return False

    return True

def main():
    """Asks user to selection actions, and executes acordingly"""
    while True:
        selection = input("Would you like to ADD, VIEW, or SEARCH your contacts? QUIT if you are done :)\n").lower()

        if not selection_validation(selection):
            print("Sorry, that is not one of the options I gave you...")
            continue
        
        if selection in ("q", "quit"):
            print("Okay crazy person I love you bye bye.")
            break

        if selection in ("a", "add"):
            new_name = input("What is the name of the new contact?\n").title()
            
            while not name_validation(new_name):
                new_name = input("Please type the name better:\n").title()

            new_number = str(input("What is the phone number of the new contact?\n"))

            while not number_validation(new_number):
                new_number = str(input("Please ensure you type only numbers, hyphens, and parenthesis!\n"))

            add_contact(new_name, new_number)
        
        if selection in ("v", "view"):
            text = read_contacts()
            print(text)

        if selection in ("s", "search"):
            query_name = input("Which contact would you like to search for?\n").lower()

            while not name_validation(query_name):
                query_name = input("Please type the name better:\n").lower()

            results = search_contacts(query_name)
            print(results)
        
if __name__ == "__main__":
    main()