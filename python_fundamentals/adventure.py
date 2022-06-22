# you are on section 6.3
# maybe: player class where inventory is stored, with add/remove methods
# TODO add this to add method
# TODO add get() method

from multiprocessing.dummy import current_process
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
    
    @property
    def player_place(self):
        """gets the current player location and returns the place object"""
        current_location = PLAYER.place

        if current_location not in PLACES.keys():
            error(f"It seems the player exists outside the known universe...")
            return
        
        player_place = PLACES[current_location]
        return player_place
    
    def comma_list(self, item_list):
        """Takes a list and returns a oxford comma formated string"""

        x = len(item_list)

        if x > 2:
            text = ", ".join(item_list)
            # splits on the last ", " and then re-joins with an ", and"
            text = ", and ".join(text.rsplit(", ", 1))
            return text
        elif x > 0:
            text = " and ".join(item_list)
            return text
        else:
            return ""

class Collectable():
    """Base class for objects with collections"""
    def __init__(self, key, name, description):
        self.key = key
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<{self.__class__.__name__} object={self.name}>"

    # TODO add get() method

class Contents():
    """Class for objects with inventories/contents"""
    
    def has_item(self, item):
        if item in self.inventory:
            return True
        else:
            return False
    
    def add(self, item):  
        if self.has_item(item):
            self.inventory[item] += 1
        else:
            self.inventory.setdefault(item, 1)

    def remove(self, item):        
        if self.has_item(item):
            self.inventory[item] -= 1
        
        # remove item from inventory if quantity is 0
        if self.inventory[item] == 0:
            del self.inventory[item]

class Place(Collectable, Contents):
    def __init__(self, key, name, description, north=None, east=None, south=None, west=None, inventory={}):
        super().__init__(key, name, description)
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.inventory = inventory

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

        PLAYER.place = new_place.key

        return new_place

class Item(Collectable):
    def __init__(self, key, name, description, can_take=False, price=None):
        super().__init__(key, name, description)
        self.can_take = can_take
        self.price = price

class Player(Contents):
    def __init__(self, place=None, inventory={}):
        self.place = place
        self.inventory = inventory

PLACES = {
    "home": Place(
        key="home",
        name="Your Cottage",
        description="A cozy stone cottage with a desk and a neatly made bed.",
        east="town square",
        inventory={'desk':1,
                   'book':1,
                   'bed':1
        }
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
    "desk": Item(
        key="desk",
        name="a writing desk",
        description="A wooden desk with a large leather-bound book open on its surface.",
    ),
    "book": Item(
        key="book",
        name="a book",
        description="A hefty leather-bound tome open to an interesting passage.",
        can_take = True,
    ),
    "bed": Item(
        key="bed",
        name="your bed",
        description="Some cloth stuffed with hay. Hardly any bugs.",
    ),
}

# TODO ask alissa how to do properties for player.place
PLAYER = Player(
    place="home",
    # place=PLACES.get("home"),
    inventory={},
)

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
        """Lists the items present in the current location, and all nearby locations"""

        debug(f"Trying to look around.")

        current_place = self.player_place

        # Display info about the current location
        header(f"{current_place.name}")
        wrap(f"{current_place.description}")

        # Display list of the items in the current location
        if current_place.inventory:
            item_names = [ITEMS[x].name for x in current_place.inventory]
            wrap(f"You see {self.comma_list(item_names)}.")

        for direction in ('north','south','east','west'):
            nearby_name = getattr(current_place, direction)

            if nearby_name:
                write(f"To the {direction} is {PLACES[nearby_name].name}.")

        # print("You see a vast nothingness.")

class Shop(Command):

    def do(self):
        """Does the shop, duh"""
        header("Whater you buyin'?\n")

        for item in ITEMS.values():
            if item.price:
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
        
        current_place = self.player_place

        if current_place:
            new_place = current_place.go(direction)

            if new_place:
                header(new_place.name)    
                wrap(new_place.description)

class Examine(Command):
    def do(self):
        """Prints a description of the specified item"""
        if not self.args:
            error("You cannot examine nothing.")
            return
        
        debug(f"Trying to examine: {self.args}")

        name = self.args[0].lower()
        current_place = self.player_place

        if name not in current_place.inventory:
            error(f"There is no {name} in {current_place.name.lower()}.")
            return

        if name not in ITEMS.keys():
            error(f'Hmmm, "{name}" seems to be missing from my files.')
            return

        item = ITEMS[name]

        header(item.name.title())
        wrap(item.description)

class Take(Command):
    def do(self):
        """Removes the specified item from the loaction and adds to inventory"""
        if not self.args:
            error("You cannot take nothing.")
            return

        debug(f"Trying to take: {self.args}")

        target = self.args[0].lower()
        current_place = self.player_place

        if target not in current_place.inventory:
            error(f"Sorry, there is no {target} here.")
            return

        # TODO add this to add method
        if target not in ITEMS:
            raise Exception(f"This is embarrasing, but the information about {target} is missing.")
            # error(f"This is embarrasing, but the information about {target} is missing.")
            # return

        target = ITEMS[target]

        if not target.can_take:
            wrap(f"You try to pick up {target.name}, but it doesn't budge.")
            return

        PLAYER.add(target.key)
        current_place.remove(target.key)

        wrap(f"You pick up {target.name} and put it in your bag.")

            
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
    "t": Take,
    "take": Take,
    "grab": Take,
}

# class Game():
#     def __init__(self):

def main():

    print("Welcome!")

    print(repr(ITEMS['potion']))

    while True:
        print()

        debug(f"You are at: {PLAYER.place}")

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