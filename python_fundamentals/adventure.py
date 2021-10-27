from sys import stderr

DEBUG = True

PLAYER = {
    "place": "home",
}

PLACES = {
    "home": {
        "key": "home",
        "name": "Your Cottage",
        "east": "town square",
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

COMPASS = ['north','east','south','west']

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

    for item in ITEMS.values():
        #format this better
        print(f"${abs(item['price'])}. {item['key'].title()}: {item['description']}")
    print()

def do_go(args):
    """Moves to the specified location"""
    
    if not args:
        error("You must specify a location.")
        return

    debug(f"Trying to go: {args}")

    direction = args[0].lower()

    if direction not in COMPASS:
        error(f"Sorry, there is no '{direction}'")
        return

    old_name = PLAYER['place']
    old_place = PLACES[old_name]

    new_name = old_place.get(direction)

    if not new_name:
        error(f"Sorry, there is no '{direction}'' from {old_place['name'].lower()}.")
        return

    new_place = PLACES.get(new_name)

    if not new_place:
        error(f"Ruh roh, raggy! The GM seems to have forgotten the details of {new_name}.")
        return

    PLAYER['place'] = new_name

    print(f"You find yourself in {new_place['name'].lower()}: {new_place['description'].lower()}")



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