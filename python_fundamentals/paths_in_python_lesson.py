from pathlib import Path

def e4():
    """Exercise 4: before printing contacts.txt checks to ensure file exists and is a valid file"""
    path = Path("data/contacts.txt")
    
    if not path.exists():
        print("No file named contacts.txt")
        return
    
    if not path.is_file():
        print("Unable to read file: contacts.txt")
        return
    
    with open(path) as fp:
        contents = fp.read()
    
    print(contents)

def e5():
    """Exercise 5: prints the contents of a .py file in the same directory as this file"""
    path = Path(__file__).parent / "contacts.py"

    with open(path) as fh:
        contents = fh.read()

    print(contents)

e5()