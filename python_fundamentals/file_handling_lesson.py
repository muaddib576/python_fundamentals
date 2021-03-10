
def print_groceries():
    
    print("Groceries")
    print("=========")

    fh = open("groceries.txt")
    for line in fh.readlines():
        print(line, end="")
    fh.close()
    print()

def print_brownie():

    fh = open("mug-brownie.md")
    contents = fh.read()
    fh.close()

    print(contents)


def print_todo():
    print("To-do List:")
    print("===========")

    fh = open("todo.txt")
    for line in fh.readlines():
        print("* " + line, end="")
    fh.close()
    print()

def create_todos():
    todos = [
        "laundry",
        "dishes",
    ]

    fh = open("todo.txt", "w")
    for item in todos:
        fh.write(f"- {item}\n")
    fh.close() 

def create_groceries():
    groceries = ["tortillas","sour cream","oreos"]

    fh = open("groceries.txt", "w")
    for item in groceries:
        fh.write("-" + item + "\n")
    fh.close

def add_groceries():
    fh = open("groceries.txt", "a")
    fh.write("-shampoopoo\n")
    fh.close()


def print_brownie():

    fh = open("mug-brownie.md")
    contents = fh.read()
    fh.close()

    print(contents)


def with_browie():

    with open("mug-brownie.md") as fp:
        contents = fp.read()
    
    print(contents)



# print_groceries()
# print_brownie()
# print_todo()
# create_todos()
# create_groceries()
# add_groceries()
