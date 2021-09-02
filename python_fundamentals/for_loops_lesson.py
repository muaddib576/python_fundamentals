



def movies_ex():
    movies = ['Superbabies: Baby Geniuses 2', 'Manos: the Hands of Fate', 'Sharknado']

    for movie in movies:
        print(movie)

# movies_ex()

def iterators_ex():
    letters = []

    for letter in "Brian":
        letters.append(letter)
    
    letters_iterator = iter(letters)

    while True:
        print(next(letters_iterator))

# iterators_ex()

def game_char_ex():
    roles = ['Cleric','Bard','Barbarian','Thief']
    roles_iter = iter(roles)

    while True:
        try:
            role = next(roles_iter)
        except StopIteration:
            break

        print(f"Role: {role}")

    for role in roles:
        print(f"Role: {role}")

# game_char_ex()

def game_tools_ex():
    tools = {"Cleric": "god", "Bard": "Lute", "Barbarian": "Wrath", "Thief": "Lockpick"}
    tools_iter = iter(tools.items())

    while True:
        try:
            role, tool = next(tools_iter)
        except StopIteration:
            break
        
        print(f"A {role}'s favorite tool is their trusty: {tool}.")

    for role, tool in tools.items():
        print(f"A {role}'s favorite tool is their trusty: {tool}.")

    for i, (role, tool) in enumerate(tools.items(),1):
        print(f"{i}. A {role}'s favorite tool is their trusty: {tool}.")

game_tools_ex()

def number_names_ex():
    numbahs = ['One','Two','Three','Four','Five']

    for i, numbah in enumerate(numbahs,1):
        print(i, numbah)

# number_names_ex()


