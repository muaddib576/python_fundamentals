# you are on section 9.5 (TODO update Take command to use order_args_qty())

from multiprocessing.dummy import current_process
from sys import stderr
from console import fg, bg, fx
import textwrap

WIDTH = 60
MARGIN = ' '*3
DEBUG = True

class InvalidItemError(Exception):
    ...

class InvalidPlaceError(Exception):
    ...

class Command():
    def __init__(self, args):
        self.args = args

    # TODO add validation to ensure the place is good
    
    @property
    def player_place(self):
        """gets the current player location and returns the place object"""
        current_location = PLAYER.place

        player_place = Place.get(current_location)
        
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

    def order_args_qty(self):
        """Takes args list and puts the qty at end of list"""
        
        ordered_args = []
        for x in self.args:
            try:
                ordered_args.append(int(x))
            except ValueError:
                ordered_args = [x] + ordered_args
        
        self.args = ordered_args

class Collectable():
    """Base class for objects with collections"""
    def __init__(self, key, name, description):
        self.key = key
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<{self.__class__.__name__} object={self.name}>"

class Contents():
    """Class for objects with inventories/contents"""
    
    # move this to Contents
    def has_item(self, key, qty=1):
        """Return True if Object inventroy has at least the specified quantity of key, else False"""

        return key in self.inventory and self.inventory[key] >= qty
    
    def add(self, item, qty=1): 
        """Adds X item"""
        if self.has_item(item, qty):
            self.inventory[item] += qty
        else:
            self.inventory.setdefault(item, qty)

    def remove(self, item, qty=1):
        """Remove X item"""
        if self.has_item(item, qty):
            self.inventory[item] -= qty
        
        # remove item from inventory if quantity is 0 or less
        if self.inventory[item] <= 0:
            del self.inventory[item]

class Place(Collectable, Contents):
    def __init__(self, key, name, description, north=None, east=None, south=None, west=None, inventory={}):
        super().__init__(key, name, description)
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.inventory = inventory

    def go(self, direction):
        """Validates the requested direction and updates player location"""
        if direction not in COMPASS:
            error(f"Sorry, there is no '{direction}'")
            return

        destination = self.__dict__.get(direction)

        if not destination:
            error(f"Sorry, there is no '{direction}' from {self.name}.")
            return

        new_place = Place.get(destination)

        if not new_place:
            abort(f"Ruh roh, raggy! The GM seems to have forgotten the details of {destination}.")

        PLAYER.place = new_place.key

        return new_place

    @classmethod
    def get(self, key, default=None):
        """Takes a place key and returns the Place's instance"""
        place = PLACES.get(key, default)

        if place:
            return place
        else:
            raise InvalidPlaceError(f"This is embarrasing, but the information about {key} is missing.")


class Item(Collectable):
    def __init__(self, key, name, description, can_take=False, price=None):
        super().__init__(key, name, description)
        self.can_take = can_take
        self.price = price

    @classmethod
    def get(self, key, default=None):
        """Takes an item key and returns the Item's instance"""
        item = ITEMS.get(key, default)

        if item:
            return item
        else:
            raise InvalidItemError(f"This is embarrasing, but the information about {key} is missing.")

    def is_for_sale(self):
        """Returns True if item has a price"""
        return self.price != None

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
                   'book':12,
                   'bed':1,
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

def abort(message):
    """Prints fatal error message and exits the program"""
    error(message)
    exit(1)

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
                write(f"To the {direction} is {Place.get(nearby_name).name}.")

class Shop(Command):

    def do(self):
        """Does the shop, duh"""
        header("Whater you buyin'?\n")

        for item in ITEMS.values():
            if item.is_for_sale():
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

        if not (current_place.has_item(name) or
                PLAYER.has_item(name)):
            error(f"There is no {name} in {current_place.name.lower()}.")
            return

        item = Item.get(name)

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

        if not current_place.has_item(target):
            error(f"Sorry, there is no {target} here.")
            return

        target_item = Item.get(target)

        if not target_item.can_take:
            wrap(f"You try to pick up {target_item.name}, but it doesn't budge.")
            return

        PLAYER.add(target_item.key)
        current_place.remove(target_item.key)

        wrap(f"You pick up {target_item.name} and put it in your bag.")

class Inventory(Command):
    def do(self):
        """Displayes the current contents of the player inventory"""

        debug("Trying to show player inventory.")

        if not PLAYER.inventory:
            write("Inventory empty.")

        for name, qty in PLAYER.inventory.items():
            item = Item.get(name)
            write(f"(x{qty:>2}) {item.name}")

class Drop(Command):
    def do(self):
        """Removed the specified item from the player's inventory and adds it to the location"""
        if not self.args:
            error("You cannot drop nothing.")
            return

        self.order_args_qty()

        debug(f"Trying to drop: {self.args}")

        name = self.args[0].lower()
        
        qty = 1
        if isinstance(self.args[-1], int):
            qty = self.args[-1]

        current_place = self.player_place

        if PLAYER.has_item(name,qty):
            PLAYER.remove(name,qty)
            current_place.add(name)
            wrap(f"You dropped {qty} {name} on the ground.")
            return

        error(f"You dont have a {name} to drop.")

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
    "inventory": Inventory,
    "i": Inventory,
    "drop": Drop,
    "d": Drop,
}

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
            try:
                cmd.do()
            except (InvalidItemError) as e:
                abort(str(e))


        else:
            error("No such command.")
            continue

if __name__ == "__main__":
    main()