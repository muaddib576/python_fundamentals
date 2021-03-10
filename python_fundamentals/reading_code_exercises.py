"""Just Ice Cream Things"""

from pprint import pprint

flavors = ['Banana', 'Chocolate', 'Lemon', 'Pistachio', 'Raspberry', 'Strawberry', 'Vanilla']

def ice_cream_menu():
    """Prints an ice cream menu"""
    i = 0
    while i < len(flavors):
        print(f"{i+1}. {flavors[i]}")
        i += 1
        

# ice_cream_menu()

def sorbet_list():
    """Generates a list of Sorbet pairings based on all the ice cream flavors"""

    #create list of pairings
    pairings = []    
    #iterate over flavor list, and adds to pairings list    
    i = 0
    while i < len(flavors):
        
        x = (i + 1)
        while x < len(flavors):
            pairings.append(f"{flavors[i]} & {flavors[x]}")
            x += 1
        
        i += 1
    
    return pairings


def sorbet_list_for_loop():
    """Uses For Loops to generates a list of Sorbet pairings based on all the ice cream flavors"""
    pairings = []

    # second = flavors[i+1:-1]
    # import string
    # letters = list(string.ascii_lowercase)

    for i in flavors[0:-1]:
        print("blah")
        for x in flavors[i:-1]:
            pairings.append(f"{flavors[i]} & {flavors[(x)]}")


    # for i, flavor in enumerate(flavors):

    #     for x, flavor in enumerate(flavors, 1):
    #         if x < len(flavors) and x > i:
    #             pairings.append(f"{flavors[i]} & {flavors[(x)]}")

    return pairings


def sorbet_menu():
    """Prints a sorbet pairing menu"""
    # sorbet_pairings = sorbet_list()
    sorbet_pairings = sorbet_list_for_loop()

    i = 0
    while i < len(sorbet_pairings):
        print(f"{i+1}. {sorbet_pairings[i]}")
        i += 1

sorbet_menu()
# print(flavors[0:-1])


