#  you finished the pretify part and converting to classes
# you are on section 4
# Think about maybe: command class that handles argument parsing
# maybe: player class where inventory is stored, with add/remove methods
# Alissa made Game class and Command class. But each command inherets from that class. "Do" method
# Game class, do_ as methods. Player and Place class

from sys import stderr
from console import fg, bg, fx
import textwrap

WIDTH = 60
MARGIN = ' '*3
DEBUG = True

# class Object():
#     """Base class"""
#     ...

class Command():
    def __init__(self, args):
        self.args = args

    # TODO add validation to ensure the place is good
    
    def get_place(self):
        """gets the current player location and returns the place object"""
        current_location = PLAYER['place']

        if current_location not in PLACES.keys():
            error(f"It seems the player exists outside the known universe...")
            return
        
        player_place = PLACES[current_location]
        return player_place
    
class Collectable():
    """Base class for objects with collections"""
    def __init__(self, key, name, description):
        self.key = key
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<{self.__class__.__name__} object={self.name}>"

class Place(Collectable):
    def __init__(self, key, name, description, north=None, east=None, south=None, west=None):
        super().__init__(key, name, description)
        self.north = north
        self.east = east
        self.south = south
        self.west = west

    # get = __dict__.get <this can replace the method below>
    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def go(self, direction):
        """Validates the requested direction and updates player location"""
        if direction not in COMPASS:
            error(f"Sorry, there is no '{direction}'")
            return

        destination = self.__dict__.get(direction)

        if not destination:
            error(f"Sorry, there is no '{direction}' from {self.name}.")
            return

        new_place = PLACES.get(destination)

        if not new_place:
            error(f"Ruh roh, raggy! The GM seems to have forgotten the details of {destination}.")
            return

        PLAYER['place'] = new_place.key

        return new_place

class Item(Collectable):
    def __init__(self, key, name, description, price):
        super().__init__(key, name, description)
        self.price = price

# TODO update player to be an object?
PLAYER = {
    "place": "home"
}

PLACES = {
    "home": Place(
        key="home",
        name="Your Cottage",
        description="A cozy stone cottage with a desk and a neatly made bed.",
        east="town square",
    ),
    "town square": Place(
        key="town square",
        name="Town Square",
        description="The square part of town.",
        west="home",
    ),
}

ITEMS = {
    "potion": Item(
        key="potion",
        name="healing potion",
        description="A magical liquid that improves your life's outlook.",
        price=-10,
    ),
    "lockpicks": Item(
        key="lockpicks",
        name="lockpicking tools",
        description="A standard theiving kit.",
        price=-8,
    ),
    "dagger": Item(
        key="dagger",
        name="stabbing dagger",
        description="A length of metal honed to a fine point.",
        price=-20,
    ),
}

COMPASS = ['north','east','south','west']

def debug(message):
    """De debug"""
    if DEBUG:
        print(fg.lightblack(f"!!! {message}"))
    
def error(message):
    """Prints da error"""
    print(f"{fg.red('Error:')} {message}")

def wrap(text):
    # print(MARGIN,text)
    paragraph = textwrap.fill(
        text,
        WIDTH,
        initial_indent=MARGIN,
        subsequent_indent=MARGIN
    )
    
    print(paragraph)

def write(text):
    print(MARGIN, text, sep="")

def header(title):
    print()
    title = fx.bold(title)
    title = fx.underline(title)
    title = fg.cyan(title)
    write(title)
    print()

class Quit(Command):

    def do(self):
        """Ends the game"""
        write("Goodbye.")
        quit()

class Look(Command):

    def do(self):
        """Examines suroundings"""
        print("You see a vast nothingness.")

class Shop(Command):

    def do(self):
        """Does the shop, duh"""
        header("Whater you buyin'?\n")

        for item in ITEMS.values():
            #format this better {num:>80}
            write(f"${abs(item.price):>2d}. {item.key.title()}: {item.description}")
        print()

class Go(Command):
    def do(self):
        """Moves to the specified location"""    
        if not self.args:
            error("You must specify a location.")
            return

        debug(f"Trying to go: {self.args}")

        direction = self.args[0].lower()
        
        current_place = self.get_place()

        if current_place:
            new_place = current_place.go(direction)

            if new_place:
                header(new_place.name)    
                wrap(new_place.description)

class Examine(Command):
    def do(self):
        """Prints a description of the spcified item"""
        if not self.args:
            error("You cannot examine nothing.")
            return
        
        debug(f"Trying to examine: {self.args}")



action_dict = {
    "q": Quit,
    "quit": Quit,
    "l": Look,
    "look": Look,
    "s": Shop,
    "shop": Shop,
    "g": Go,
    "go": Go,
    "e": Examine,
    "examine": Examine,
}

# class Game():
#     def __init__(self):

def main():

    print("Welcome!")

    print(repr(ITEMS['potion']))

    while True:
        print()

        debug(f"You are at: {PLAYER['place']}")

        reply = input(fg.green("> ")).lower().strip()

        args = reply.split()

        if not args:
            continue

        debug(args)

        command = args.pop(0)

        if command in action_dict.keys():
            print()

            klass = action_dict[command]
            cmd = klass(args)
            cmd.do()


        else:
            error("No such command.")
            continue

if __name__ == "__main__":
    main()