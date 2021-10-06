from sys import stderr

DEBUG = True

PLAYER = {
    "place": "home",
}

PLACES = {
    "home": {
        "key": "home",
        "name": "Your Cottage",
        "east": "town-square",
        "description": "A cozy stone cottage with a desk and a neatly made bed.",
    },
    "town square": {
        "key": "town square",
        "name": "Town Square",
        "west": "home",
        "description": "The square part of town.",
    }
}

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

def debug(message):
    if DEBUG:
        print(f"!!! {message}")
    
def error(message):
    print(f"Error: {message}", file=stderr)

def do_quit(args=None):
    """Ends the game"""
    print("Goodbye.")
    quit()

def do_look(args=None):
    """Examines suroundings"""
    print("You see a vast nothingness.")

def do_shop(args=None):
    """Does the shop, duh"""
    print("Whater you buyin'?\n")

    for item in ITEMS.items():
        print(f"{item[0].title()}: {item[1]['description']}")
    print()

def do_go(direction):
    """Moves to the specified location"""
    
    if not direction:
        print("You must specify a location.")
        return

    debug(f"Trying to go: {direction[0]}")


action_dict = {
    "q": do_quit,
    "quit": do_quit,
    "l": do_look,
    "look": do_look,
    "s": do_shop,
    "shop": do_shop,
    "g": do_go,
    "go": do_go
}

def main():

    print("Welcome!")

    while True:
        print()

        debug(f"You are at: {PLAYER['place']}")

        reply = input("> ").lower().strip()

        args = reply.split()

        if not args:
            continue

        debug(args)

        command = args.pop(0)

        if command in action_dict.keys():
            print()
            action_dict[command](args)

        else:
            error("No such command.")
            continue

if __name__ == "__main__":
    main()