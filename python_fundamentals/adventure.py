

ITEMS = {
    "potion": {
        "key": "potion",
        "name": "healing potion",
        "description": "A magical liquid that improves your life's outlook.",
        "price": -10,
    },
    "lockpicks": {
        "key": "lockpicks",
        "name": "lockpicking tools",
        "description": "A standard theiving kit.",
        "price": -8,
    },
    "dagger": {
        "key": "dagger",
        "name": "stabbing dagger",
        "description": "A length of metal honed to a fine point.",
        "price": -20,
    }
}

def do_quit():
    """Ends the game"""
    print("Goodbye.")
    quit()

def do_look():
    """Examines suroundings"""
    print("You see a vast nothingness.")

def do_shop():
    """Does the shop, duh"""
    print("Whater you buyin'?\n")

    for item in ITEMS.items():
        print(f"{item[0].title()}: {item[1]['description']}")
    print()

action_dict = {
    "q": do_quit,
    "quit": do_quit,
    "l": do_look,
    "look": do_look,
    "s": do_shop,
    "shop": do_shop
}

def main():

    print("Welcome!")

    while True:
        print()
        reply = input("> ").lower()

        if reply in action_dict.keys():
            print()
            action_dict[reply]()

        else:
            print("No such command.")
            continue

if __name__ == "__main__":
    main()