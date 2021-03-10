# Goals
# -----
# [x] add user input validation on search/add (ensure not blank, phone number is numbers/symbols, etc)
# [x] print a message if the user doesn't enter a valid command
# [ ] write tests
# [ ] store as a faux-CSV:
#     [ ] separate each field with a comma when writing
#     [ ] split on comma on readin
#     [ ] ensure no commas on validating user input
# [ ] add email address to data user can save in contacts

def add_contact(name, number):
    """Appends a new name and number to contacts.txt"""
    with open("contacts.txt", "a") as fp:
        fp.write(f"{name} {number}\n")

def read_contacts():
    """Adds all the lines from contacts.txt to a variable that will be printed in main()"""
    with open("contacts.txt", "r") as fp:
        contents = fp.read()
    return contents

def search_contacts(name):
    with open("contacts.txt", "r") as fp:
        text = ""
        for line in fp.readlines():
            if name in line.lower():
                text += f"{line}"
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

            new_number = input("What is the phone number of the new contact?\n")

            while not number_validation(new_number):
                new_number = input("Please ensure you type only numbers, hyphens, and parenthesis!\n")

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