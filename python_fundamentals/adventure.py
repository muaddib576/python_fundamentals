"""."""

# You are on part 15 - You started writing tests, but just did an outline
# all the player commands use the item keys,\
# but the text displayed to the player is the item names
# you should do something to fix that
# TODO generate this dynamically with a dunder method called "subclasses" or somesuch: line 511 (do eventually)

from multiprocessing.dummy import current_process
from sys import stderr
from console import fg, bg, fx
from console.progress import ProgressBar
import textwrap
from random import choice, randint
from time import sleep

WIDTH = 60
MARGIN = ' '*3
DELAY = 1
DEBUG = True
MAX_HEALTH = 100
BAR = ProgressBar(
    total=(MAX_HEALTH + .1),
    width=(WIDTH - len("Health") - len("100%")),
    clear_left=False,
)

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
        """Takes a list and returns a oxford comma formatted string"""

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

    def health_bar(self):
        """Displays the current health bar"""
        print()
        write(f"Health {BAR(PLAYER.current_health)}")

    def text_delay(self, sentences):
        """Prints the elements from the variable with a DELAY between each"""
        for text in sentences:
            print()
            write(text)
            sleep(DELAY)

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
        """Return True if Object inventory has at least the specified quantity of key, else False"""

        return key in self.inventory and self.inventory[key] >= qty
    
    def add(self, item, qty=1): 
        """Adds X item"""
        self.inventory.setdefault(item, 0)
        self.inventory[item] += qty

    def remove(self, item, qty=1):
        """Remove X item"""
        if self.has_item(item, qty):
            self.inventory[item] -= qty
        
        # remove item from inventory if quantity is 0 or less
        if self.inventory[item] <= 0:
            del self.inventory[item]

class Place(Collectable, Contents):
    def __init__(self, key, name, description, north=None, east=None, south=None, west=None, can=None, inventory=None):
        super().__init__(key, name, description)
        self.north = north
        self.east = east
        self.south = south
        self.west = west

        if not can:
            can = []
            
        if not inventory:
            inventory = {}

        self.can = can
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

    def place_can(self, command):
        """Returns TRUE if the command is valid given the place"""

        return command in self.can


class Item(Collectable):
    def __init__(self, key, name, description, writing=None, can_take=False, price=None):
        super().__init__(key, name, description)
        self.writing = writing
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
    def __init__(self, place=None, current_health=None, inventory={}):
        self.place = place
        self.current_health = current_health
        self.inventory = inventory

    def change_health(self, amount):
        """Adjusts the players health by the given amount. Does not drop below 0 or above max."""
        self.current_health += amount

        if self.current_health > MAX_HEALTH:
            self.current_health = MAX_HEALTH
        elif self.current_health < 0:
            self.current_health = 0

class Dragon_head(Item, Contents):
    MOODS = [
        {
            "mood": "cheerful",
            "treasure": [3, 15],
            "damage": [],
            "message": ("thinks you're adorable! He gives you {treasure} gems!"),
        },
        {
            "mood": "grumpy",
            "treasure": [],
            "damage": [3, 15],
            "message": ("wants to be left alone. The heat from his mighty sigh "
                        "singes your hair, costing you {damage} in health."
            ),
        },
        {
            "mood": "lonely",
            "treasure": [8, 25],
            "damage": [8, 25],
            "message": ("is just SO happy to see you! He gives you a whopping "
                        "{treasure} gems! Then he hugs you, squeezes you, and calls "
                        "you George... costing you {damage} in health."),
        },
    ]

    def __init__(self, key, name, description, mood=None, treasure=None, damage=None, message=None):
        super().__init__(key, name, description)
        self.mood = mood
        self.treasure = treasure
        self.damage = damage
        self.message = message
        self._init_mood()
        
    def _init_mood(self):
        if not self.__class__.MOODS:
            return

        mood = choice(self.__class__.MOODS)

        self.mood = self.mood or mood["mood"]
        self.treasure = self.treasure or mood["treasure"]
        self.damage = self.damage or mood["damage"]
        self.message = self.message or mood["message"]
        self.__class__.MOODS.remove(mood)

    def calc_treasure(self):
        """Returns an int value from within the Dragon's treasure range"""
        treasure_range = self.treasure or [0,0]
        treasure_amount = randint(*treasure_range)

        return treasure_amount

    def calc_damage(self):
        """Returns an int value from within the Dragon's damage range"""

        damage_range = self.damage or [0,0]
        damage_amount = randint(*damage_range)

        return damage_amount

    def mood_text(self, treasure_amount, damage_amount):
        """Given a treasure and damage amount, returns the formatted text specific to the dragon's mood"""

        message_text = self.message
        message_text = message_text.format(treasure=treasure_amount, damage=damage_amount)

        mood_text = f"The dragon's {self.mood} {self.key} head {message_text}"

        return mood_text

DRAGON_HEADS = {
    "red": Dragon_head(
        key="red",
        name="Red Dragon Head",
        description="It's red.",
        # mood="",
        # damage=(),
        # treasure=(),
    ),
    "black": Dragon_head(
        key="black",
        name="Black Dragon Head",
        description="It's black.",
    ),
    "silver": Dragon_head(
        key="silver",
        name="Silver Dragon Head",
        description="It's silver.",
    ),
}

PLACES = {
    "home": Place(
        key="home",
        name="Your Cottage",
        description="A cozy stone cottage with a desk and a neatly made bed.",
        east="town-square",
        inventory={'desk':1,
                   'book':1,
                   'bed':1,
        },
    ),
    "town-square": Place(
        key="town-square",
        name="Town Square",
        description="The square part of town.",
        north="market",
        east="woods",
        west="home",
    ),
    "market": Place(
        key="market",
        name="Yee ol' Market",
        description="A dusty store with rows of shelves overflowing with what appears to be junk. "\
            "A large wooden sign hangs above the clerk.",
        south="town-square",
        can=['shop'],
        inventory={'potion':5,
                   'dagger':1,
        },
    ),
    "woods": Place(
        key="woods",
        name="The Woods",
        description="Significantly more trees than the Town.",
        east="hill",
        west="town-square",
    ),
    "hill": Place(
        key="hill",
        name="Grassy hill",
        description="The trees have given way to an expansive hill covered in rustling grass.",
        west="woods",
        south="cave",
    ),
    "cave": Place(
        key="cave",
        name="Foreboding Cave",
        description="A big ol' cave entrance.",
        north="hill",
        can=['pet'],
        inventory={'dragon':1,
        },
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
        description="A standard thieving kit.",
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
        writing={'title':"The book is open to a page that reads:",
                 'message': ("The break in your line of fate may indicate "
                             "a change in location or career.",

                             "You have more than one life line, which may "
                             "indicate you are a cat.",
                 )
        },
        can_take = True,
    ),
    "bed": Item(
        key="bed",
        name="your bed",
        description="Some cloth stuffed with hay. Hardly any bugs.",
    ),
    "gems": Item(
        key="gems",
        name="gems",
        description="The realm's primary currency. They also look pretty.",
    ),
    "dragon": Item(
        key="dragon",
        name="dragon",
        description= (f"A large dragon with heads of {', '.join(list(DRAGON_HEADS.keys())[0:-1])}, " \
                      f"and {list(DRAGON_HEADS.keys())[-1]}."
        )
    ),
}

PLAYER = Player(
    # place="home",
    place="cave",
    current_health = 100,
    inventory={'gems':50,},
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

def wrap(text, width=None, initial_indent=None, subsequent_indent=None):
    width = width or WIDTH
    initial_indent = initial_indent or MARGIN
    subsequent_indent = subsequent_indent or MARGIN

    if isinstance(text, str):
        text = (text,)

    blocks = []

    for stanza in text:
        paragraph = textwrap.fill(
            stanza,
            width,
            initial_indent=initial_indent,
            subsequent_indent=subsequent_indent
        )
        
        blocks.append(paragraph)
    
    print(*blocks, sep="\n\n")

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

        current_place = self.player_place

        if not current_place.place_can('shop'):
            error(f"Sorry, you can't shop here.")
            return

        header("Whater you buyin'?\n")

        for key, qty in current_place.inventory.items():
            item = ITEMS.get(key)
            if item.is_for_sale():

                prefix_text = f"${abs(item.price):>2d}. {item.name.title()} x{qty} : "
                full_text = f"{prefix_text}{item.description}"

                prefix_len = ' ' * len(f"{MARGIN}{prefix_text}")

                wrap(text=full_text,
                     subsequent_indent=prefix_len
                )

        print()

class Buy(Command):
    def do(self):
        """Exchanges the players gems for items in shops"""

        current_place = self.player_place

        if not current_place.place_can('shop'):
            error(f"Sorry, you can't shop here.")
            return    

        if not self.args:
            error("You cannot buy nothing.")
            return

        self.order_args_qty()

        debug(f"Trying to buy: {self.args}")

        target = self.args[0].lower()
        target_item = Item.get(target)

        qty = 1
        if isinstance(self.args[-1], int):
            qty = self.args[-1]

        if not target_item.is_for_sale():
            error("Sorry, that item is not for sale.")
            return

        if not current_place.has_item(target,qty):
            error(f"Sorry, there are not {qty} {target_item.name} here.")
            return

        item_cost = abs(target_item.price) * qty

        if PLAYER.inventory['gems'] - item_cost < 0:
            error(f"Sorry, you do not have enough gems.")
            return

        PLAYER.add(target_item.key, qty)
        PLAYER.remove('gems',item_cost)

        current_place.remove(target_item.key, qty)
        current_place.add('gems',item_cost)

        wrap(f"You bought {qty} {target_item.name} for {item_cost} gems and put it in your bag.")

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
        # TODO the following line assumes that the item exists in the ITEMS dictionary. You should create a "no item here" message.
        item = Item.get(name)

        if current_place.has_item(name):
            header(item.name.title())
            
            if current_place.place_can('shop') and item.is_for_sale():
                wrap(f"{item.description} The shop has {current_place.inventory[item.key]}, you can buy one for {abs(item.price)} gems.")
                return
            
            wrap(item.description)
            return

        if PLAYER.has_item(name):
            header(item.name.title())
            wrap(item.description)
            return
            
        error(f"There is no {name} in {current_place.name.lower()}.")

class Take(Command):
    def do(self):
        """Removes the specified item from the location and adds to inventory"""
        if not self.args:
            error("You cannot take nothing.")
            return

        self.order_args_qty()

        debug(f"Trying to take: {self.args}")

        target = self.args[0].lower()

        qty = 1
        if isinstance(self.args[-1], int):
            qty = self.args[-1]

        current_place = self.player_place

        if not current_place.has_item(target,qty):
            error(f"Sorry, there are not {qty} {target} here.")
            return

        target_item = Item.get(target)

        if not target_item.can_take:
            wrap(f"You try to pick up {target_item.name}, but it doesn't budge.")
            return

        PLAYER.add(target_item.key, qty)
        current_place.remove(target_item.key, qty)

        wrap(f"You pick up {qty} {target_item.name} and put it in your bag.")

class Inventory(Command):
    def do(self):
        """Displays the current contents of the player inventory"""

        debug("Trying to show player inventory.")

        self.health_bar()

        print()

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

        error(f"You dont have {qty} {name} to drop.")

class Read(Command):
    def do(self):
        """Prints any writing on the specified item"""
        if not self.args:
            error("You cannot read nothing.")
            return
        
        debug(f"Trying to read: {self.args}")

        target = self.args[0].lower()
        current_place = self.player_place

        if not (current_place.has_item(target) or PLAYER.has_item(target)):
            error(f"There is no {target} here.")
            return
        
        target_item = Item.get(target)

        if target_item.writing == None:
            error("There is nothing to read.")
            return

        wrap(target_item.writing["title"])
        print()
        wrap(target_item.writing["message"], initial_indent=MARGIN*2, subsequent_indent=MARGIN*2)       

class Pet(Command):
    def do(self):
        """Performs the Pet action on the specified dragon"""
        if not self.args:
            error("You cannot pet nothing.")
            return

        current_place = self.player_place

        if not current_place.place_can('pet'):
            error(f"You cannot do that here.")
            return
        
        target_set = False
        for word in ['head','dragon']:
            if word in self.args: #TODO you need to lower the args
                self.args.remove(word)
                target_set = True
        
        if not target_set:
            error("What are you trying to pet?")
            return
        
        if not self.args:
            error("Which dragon's head do you want to pet?")
            return

        color = self.args[0].lower()

        if color not in DRAGON_HEADS.keys():
            error("You do not see such a dragon.")
            return
        
        target_dragon = DRAGON_HEADS[color]

        treasure = target_dragon.calc_treasure()
        damage = target_dragon.calc_damage()

        PLAYER.add("gems",treasure)
        PLAYER.change_health(-damage)

        sentences = [
            "You slowly creep forward...",
            "...gingerly reach out your hand...",
            f"...and gently pet the dragon's {target_dragon.key} head.",
            "...",
            f"He blinks his eyes and peers at you...",
        ]

        self.text_delay(sentences)
        wrap(target_dragon.mood_text(treasure, damage))

# TODO generate this dynamically with a dunder method called "subclasses" or somesuch: line 511
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
    "i": Inventory,    
    "inventory": Inventory,
    "d": Drop,    
    "drop": Drop,
    "b": Buy,
    "buy": Buy,
    "r": Read,
    "read": Read,
    "p": Pet,
    "pet": Pet,
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
            # TODO change things to make args positional
            # cmd = klass(*args)
            try:
                cmd.do()
            except (InvalidItemError) as e:
                abort(str(e))


        else:
            error("No such command.")
            continue

if __name__ == "__main__":
    main()