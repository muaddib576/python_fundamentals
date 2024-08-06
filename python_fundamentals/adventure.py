"""."""

# You are in the process of reviewing all the #TODOs and then GRADUATION.
# You updated Command class to use property decorator and a setter to parse the player args, and updated all the command classes to be compliant.
    # NOTE: maybe should there be a contingency if more than 1 qty is passed? ""Sorry im confused, how many did you say??""
        # start with some GIVEN WHEN THENS to identify what is expected player behavior and then decide what to do

#TODO All the player commands use the item keys, but the text displayed to the player is the item names. You should do something to fix that. Maybe just normalize the names?

# NOTE: You got the compass and egress situation fixed.
    # TODO:
    # letter in house to give primary quest? Asks player to bring forgotten item to father in misty woods? Or maybe meet for a picnic? (that way there is no item check needed)?
    # VICTORY MESSAGE and behavior (quit?)
    # Add some delay to the various messages?
    # there is an issue where can_take cannot be True for items in market... meaning that purchased items cannot be dropped
        # You are creating a new shop_inventory attribute
        # The following commands need to be updated
        #   Examine - DONE
        #   Shop - DONE
        #   Buy - IN PROGRESS
        #   Take? -
        #   Look? - DONE? But it might display duplicates if both inventories have item
        #       Somewhat related, Alissa suggested maybe replacing the "shop" command with a menu in the shop that the player can "read"
        #           would need to have the writing dynamically generated. Think about it and discuss with Alissa
        #   has_item will need a new version for shop inventory - DONE
        #   remove -
        #   add? -
        #   should I add a sell command? Is there a gameplay reason for this?


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
    compass = ['north','east','south','west']
    def __init__(self, args):
        self.args = args
        # self.compass = compass
    
    @property
    def player_place(self):
        """gets the current player location and returns the place object"""
        current_location = PLAYER.place

        player_place = Place.get(current_location)
        
        return player_place
    
    @property
    def args(self):
        if "_args" not in self.__dict__:
            self._args = None
        return self._args
    
    @args.setter
    def args(self, value):
        """Sets arg_string and arg_qty values upon instantiation"""

        self._args = value
        
        string_list = []
        qty_list = []

        for x in self._args:
            temp_x = self.word_to_int(x)
            if temp_x:
                qty_list.append(int(temp_x))
            else:
                string_list = string_list + [x]

        final_string = " ".join(string_list)

        # assume 1 if player does not specify qty
        if not qty_list:
            qty_list = [1]

        self.arg_string = final_string.lower()        
        self.arg_qty = qty_list

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

    def word_to_int(self, word):
        #TODO add more words to this list OR switch to more programmatic approach  
        """Converts a string that uses a word to represent a numeral into an numeral"""
        number_words = ["zero", "one", "two", "three", "four", "five", "six",
                        "seven", "eight", "nine", "ten", "eleven", "twelve",
                        "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
                        "eighteen", "nineteen"]
        
        if isinstance(word, int) or word.isnumeric():
            return word

        if word in number_words:
            return number_words.index(word)

        return None

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
    
    # move this to Contents <- wat?
    def has_item(self, key, qty=1):
        """Return True if Object inventory has at least the specified quantity of key, else False"""

        return key in self.inventory and self.inventory[key] >= qty
    
    def has_shop_item(self, key, qty=1):
        """Return True if Object shop_inventory has at least the specified quantity of key, else False"""

        return key in self.shop_inventory and self.shop_inventory[key] >= qty
    
    def add(self, item, qty=1, inventory_type="inventory"): 
        """Adds X item from specified inventory"""

        inventory = getattr(self, inventory_type)

        inventory.setdefault(item, 0)
        inventory[item] += qty

    def remove(self, item, qty=1, inventory_type="inventory"):
        """Remove X item from specified inventory"""
        
        # if self.has_item(item, qty):
        #     self.inventory[item] -= qty
        
        # # remove item from inventory if quantity is 0 or less
        # if self.inventory[item] <= 0:
        #     del self.inventory[item]

        inventory = getattr(self, inventory_type)

        if self.has_item(item, qty): #TODO I think this is causing an issue. Does self not mean what you think after the refactor??
            inventory[item] -= qty

        # remove item from inventory if quantity is 0 or less
        if inventory[item] <= 0:
            del inventory[item]

class Place(Collectable, Contents):
    def __init__(self, key, name, description, north=None, east=None, south=None, west=None, can=None, inventory=None, shop_inventory=None, egress_location=None, current_path=None):
        super().__init__(key, name, description)
        self.north = north
        self.east = east
        self.south = south
        self.west = west

        if not can:
            can = []
            
        if not inventory:
            inventory = {}

        if not shop_inventory:
            shop_inventory = {}

        self.can = can
        self.inventory = inventory
        self.shop_inventory = shop_inventory
        self.egress_location = egress_location
        self.current_path = current_path

    def go(self, direction):
        """Validates the direction exists from current location and updates player location"""

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
            raise InvalidPlaceError(f"This is embarrassing, but the information about {key} is missing.")

    def place_can(self, command):
        """Returns TRUE if the command is valid given the place"""

        return command in self.can
    
    def buy(self, item, item_cost, qty=1):
        """Takes the item key and cost and calls add/remove w/ appropriate params"""

        PLAYER.add(item, qty)
        
        # because the player might be able to buy an item for no cost, and might not have gems
        # We check that the cost is >0 before removing gems from player's inventory
        if item_cost > 0: 
            PLAYER.remove('gems',item_cost)

        self.remove(item, qty, "shop_inventory")
        self.add('gems', item_cost, "shop_inventory")

class Item(Collectable):
    def __init__(self, key, name, description, alias_plurals=None, writing=None, can_take=False, price=None, drink_message=None, eat_message=None, health_change=None):
        super().__init__(key, name, description)
        self.alias_plurals = alias_plurals or []
        self.writing = writing
        self.can_take = can_take
        self.price = price
        self.drink_message = drink_message
        self.eat_message = eat_message
        self.health_change = health_change

    @classmethod
    def get(self, key, default=None):
        """Takes an item key and returns the Item's instance"""
        item = ITEMS.get(key, default)

        if item:
            return item
        else:
            raise InvalidItemError(f"This is embarrassing, but the information about {key} is missing.")

    @classmethod
    def find(self, key):
        """Returns an item's instance if passed an alias or key for the item"""

        target_key = ''

        for instance in ITEMS.values():
            # Check if player's key matched with item key, name, or unpacked alias list
            if key in (instance.key, instance.name, *instance.alias_plurals):
                target_key = instance.key
                break
            
            # If still no exact match, check for matches without the key's trailing 's'
            if key[-1] == 's':
                s_less_key = key[:-1]
                if s_less_key == instance.key or s_less_key == instance.name:
                        target_key = instance.key
                        break

        if target_key == '':
            # if no valid object is found, the get() method needs to be skipped
            return
        
        target_item = Item.get(target_key)

        return target_item

    def is_for_sale(self):
        """Returns True if item has a price"""
        return self.price != None
    
    def get_consume_message(self, action):
        """Returns message if item instance has an eat/drink message"""
        
        if action == 'drink':
            return self.drink_message
        
        if action == 'eat':
            return self.eat_message
        
    def get_health_change_text(self):
        """Returns text if consuming item will affect health"""

        if self.health_change:
            if self.health_change >= 0:
                return f"Consuming will give you +{self.health_change} health."
            
            if self.health_change < 0:
                return f"Consuming will take {self.health_change} health."
        
        return ""

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
                   'water':1,
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
        shop_inventory={'potion':5,
                   'dagger':1,
                   'map':1,
        },
    ),
    "woods": Place(
        key="woods",
        name="The Woods",
        description="Significantly more trees than the Town.",
        east="hill",
        south="misty-woods",
        west="town-square",
        inventory={'mushroom':1,
        }
    ),
    "misty-woods": Place(
        key="misty-woods",
        name="The Misty Woods",
        description="A thick mist envelops the trees. You already feel lost just looking at it.",
        north='misty-woods',
        south='misty-woods',
        east='misty-woods',
        west='misty-woods',
        egress_location = 'woods',
        current_path=[],
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
        drink_message=(
            "You uncork the bottle.",
            "The swirling green liquid starts to bubble.",
            "You hesitatingly bring the bottle to your lips...",
            "then quickly down the whole thing!",
            "Surprisingly, it tastes like blueberries.",
            "You feel an odd tingling sensation starting at the top of your head... ",
            "...moving down your body...",
            "...down to the tips of your toes.",
        ),
        health_change=20
    ),
    "water": Item(
        key="water",
        name="bottle of water",
        description="A bottle what has water in it.",
        can_take = True,
        drink_message=(
            "You pull the cork from the waxed leather bottle.",
            "You take a deep drink of the cool liquid.",
            "You feel refreshed.",
        ),
        health_change=5
    ),
    "mushroom": Item(
        key="mushroom",
        name="a red mushroom",
        description="A red mushroom with white spots.",
        can_take = True,
        eat_message=(
            "You shove the whole mushroom in your mouth...",
            "Things start to look swirllllly...",
            "Your tummy doesn't feel so good.",
        ),
        health_change=-15
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
    "map": Item(
        key="map",
        name="Map of the Misty Woods",
        description="A tattered parchment depicting an area thick with trees and mist. You can just make out what appears to be a winding path through the madness.",
        writing={'title':"The Misty Woods",
                 'message': (
                             "┌---------------------------------------------┐",
                             "| ♣  ~  ♣  ♣  ♣  ♣  ~ |↓| ♣  ♣  ♣  ♣  ~  ♣  ♣ |",
                             "| ♣  ~  ♣  ♣  ~  ♣  ~ | | ~  ♣  ~  ♣  ♣  ♣  ♣ |",
                             "| ♣  ♣  ~  ♣  ~  ♣  ♣ |↓| ♣  ♣  ♣  ~  ♣  ♣  ~ |",
                             "| ♣  ♣  ~  _ _♣ _♣ _♣_| | ♣  ♣  ♣  ~  ♣  ♣  ~ |",
                             "| ♣  ♣  ♣ |↓  _ _←_ _ _←| ♣  ~  ♣  ~  ♣  ♣  ♣ |",
                             "| ♣  ♣  ♣ | |_♣_ ~  ♣  ♣  ♣  ♣  ~  ♣  ♣  ♣  ♣ |",
                             "| ♣  ♣  ♣ |→_ _  ↓| ~  ♣  ~  ♣  ♣  ♣  ~  ♣  ♣ |",
                             "| ♣  ♣  ♣  ♣  ♣ | | ♣  ~  ♣  ~  ♣  ♣  ♣  ♣  ~ |",
                             "| ♣  ♣  ♣  ~  ♣|   |♣  ♣  ~  ♣  ♣  ~  ♣  ♣  ♣ |",
                             "| ♣  ♣  ♣  ♣  ♣|_x_|♣  ♣  ~  ♣  ♣  ♣  ~  ♣  ~ |",
                             "| ♣  ♣  ♣  ♣  ~  ♣  ♣  ♣  ♣  ♣  ~  ♣  ♣  ♣  ♣ |",
                             "| ♣  ♣  ~  ♣  ♣  ♣  ♣  ♣  ♣  ♣  ♣  ~  ♣  ♣  ♣ |",
                             "| ♣  ♣  ♣  ♣  ♣  ~  ♣  ♣  ♣  ♣  ♣  ♣  ~  ♣  ~ |",
                             "└---------------------------------------------┘",
                 )
        },
        price=-50,
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
    place="home",
    current_health = 100,
    inventory={'gems':50,
               'lockpicks':1, #TODO remove this item from inventory
               },
)

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
        write("Goodbye. Thanks for playing!")
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
            
            if current_place.shop_inventory:
                item_names += [ITEMS[x].name for x in current_place.shop_inventory]
            
            wrap(f"You see {self.comma_list(item_names)}.")

        for direction in self.compass:
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

        for key, qty in current_place.shop_inventory.items():
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

        if not self.arg_string:
            error("You cannot buy nothing.")
            return

        debug(f"Trying to buy: {self.arg_qty} {self.arg_string}")

        target = self.arg_string
        qty = self.arg_qty[0]
        
        target_item = Item.find(target)
        
        current_gems = PLAYER.inventory.get("gems", 0)

        if not target_item:
            error(f"There is no {target} in {current_place.name.lower()}.")
            return

        if not current_place.has_shop_item(target_item.key, qty):
            if qty == 1:
                qty = 'any'
            error(f"Sorry, there are not {qty} {target} here.")
            return

        if not target_item.is_for_sale():
            error("Sorry, that item is not for sale.")
            return

        item_cost = abs(target_item.price) * qty

        if current_gems - item_cost < 0:
            error(f"Sorry, you do not have enough gems.")
            return

        # PLAYER.add(target_item.key, qty)
        
        # # because the player might be able to buy an item for no cost, and might not have gems
        # # We check that the cost is >0 before removing gems from player's inventory
        # if item_cost > 0: 
        #     PLAYER.remove('gems',item_cost)

        # current_place.remove(target_item.key, qty)
        # current_place.add('gems',item_cost)

        current_place.buy(target_item.key, item_cost, qty)

        wrap(f"You bought {qty} {target_item.name} for {item_cost} gems and put it in your bag.")

class Goroot(Command):
    def goroot(self, direction):
        """Moves to the specified location"""  

        if not self.arg_string:
            error("You must specify a location.")
            return

        current_place = self.player_place

        new_place = current_place.go(direction)

        if current_place:
            new_place = current_place.go(direction)

            if new_place:
                wrap(f"You spend some time walking {direction} and come upon:")
                header(new_place.name)    
                wrap(new_place.description)

class Go(Goroot): #rename this?
    compass = ['north','east','south','west','egress_location'] #overrides the default compass for misty-woods use
    def do(self):
        """Performs the misty version of Go command when player is in the relevant location"""
        
        if not self.arg_string:
            error("You must specify a direction.")
            return

        debug(f"Trying to go: {self.arg_string}")

        direction = self.arg_string
        current_place = self.player_place

        if direction not in self.compass:
            error(f"Sorry, there is no '{direction}'")
            return

        if current_place.key == 'misty-woods': #this could be replaced with kwarg bool?
            misty_path = ['s','s','w','w','s','e','s']
            path_length = len(misty_path)
            
            current_place.current_path += direction[:1]

            if current_place.current_path == misty_path:
                wrap(f"After navigating the woods for hours, the once thick mist begins to retreat and ahead you notice the trees give way to a clearing")
                wrap(f"Congratulations! You have completed your task!")
                quit() #TODO this breaks your test.

            if len(current_place.current_path) == path_length:
                new_place = current_place.go('egress_location')
                current_place.current_path = []

                wrap(f"After wondering in circles for hours, you find yourself back:")
                header(new_place.name)
                wrap(new_place.description)
                return
            
        self.goroot(direction)

class Examine(Command):
    def do(self):
        """Prints a description of the specified item, and qty/price if in the shop"""
        if not self.arg_string:
            error("You cannot examine nothing.")
            return
        
        debug(f"Trying to examine: {self.arg_string}")

        target = self.arg_string
        current_place = self.player_place
        
        target_item = Item.find(target)

        if not target_item:
            error(f"There is no {target} in {current_place.name.lower()}.")
            return

        if not current_place.has_item(target_item.key) and not current_place.has_shop_item(target_item.key) and not PLAYER.has_item(target_item.key):
            error(f"There is no {target} in {current_place.name.lower()}.")
            return

        header(target_item.name.title())
        wrap(f"{target_item.description} {target_item.get_health_change_text()}")
        if current_place.place_can('shop') and current_place.has_shop_item(target_item.key) and target_item.is_for_sale():
            print()
            wrap(f"The shop has {current_place.shop_inventory[target_item.key]}, you can buy one for {abs(target_item.price)} gems.")
            return

class Take(Command):
    def do(self):
        """Removes the specified item from the location and adds to inventory"""
        if not self.arg_string:
            error("You cannot take nothing.")
            return

        debug(f"Trying to take: {self.arg_qty} {self.arg_string}")

        target = self.arg_string

        qty = self.arg_qty[0]

        current_place = self.player_place

        target_item = Item.find(target)

        if not target_item:
            error(f"There is no {target} in {current_place.name.lower()}.")
            return

        if not current_place.has_item(target_item.key,qty):
            error(f"Sorry, there are not {qty} {target} here.")
            return

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
            return

        for name, qty in PLAYER.inventory.items():
            item = Item.get(name)
            write(f"(x{qty:>2}) {item.name}")

class Drop(Command):
    def do(self):
        """Removed the specified item from the player's inventory and adds it to the location"""

        if not self.arg_string:
            error("You cannot drop nothing.")
            return

        debug(f"Trying to drop: {self.arg_qty} {self.arg_string}")

        target = self.arg_string
        qty = self.arg_qty[0]

        target_item = Item.find(target)
        current_place = self.player_place

        if not target_item:
            error(f"There is no {target} in {current_place.name.lower()}.")
            return

        if PLAYER.has_item(target_item.key, qty):
            PLAYER.remove(target_item.key, qty)
            current_place.add(target_item.key, qty)
            wrap(f"You dropped {qty} {target_item.key} on the ground.")
            return

        error(f"You dont have {qty} {target_item.key} to drop.")

class Read(Command):
    def do(self):
        """Prints any writing on the specified item"""

        if not self.arg_string:
            error("You cannot read nothing.")
            return
        
        debug(f"Trying to read: {self.arg_string}")

        target = self.arg_string
        current_place = self.player_place
        
        target_item = Item.find(target)

        if not target_item:
            error(f"There is no {target} in {current_place.name.lower()}.")
            return

        if not (current_place.has_item(target_item.key) or PLAYER.has_item(target_item.key)):
            error(f"There is no {target} here.")
            return

        if target_item.writing == None:
            error("There is nothing to read.")
            return

        wrap(target_item.writing["title"])
        print()
        wrap(target_item.writing["message"], initial_indent=MARGIN*2, subsequent_indent=MARGIN*2)       

class Pet(Command):
    def do(self):
        """Performs the Pet action on the specified dragon"""

        if not self.arg_string:
            error("You cannot pet nothing.")
            return

        current_place = self.player_place

        if not current_place.place_can('pet'):
            error(f"You cannot do that here.")
            return
        
        target_set = False
        temp_arg_list = self.arg_string.split()
        for word in ['head','dragon']:
            if word in temp_arg_list:
                temp_arg_list.remove(word)
                target_set = True
        
        if not target_set:
            error("What are you trying to pet?")
            return
        
        if not temp_arg_list:
            error("Which dragon's head do you want to pet?")
            return

        # TODO this whole arg_string parsing to determine color assignment strat is a bit messy
        color = temp_arg_list[0]

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
        print()
        wrap(target_dragon.mood_text(treasure, damage))

class Consume(Command):
    def consume(self, args, action):
        """Performs the Consume action on the specified item"""

        target = self.arg_string
        target_item = Item.find(target)

        if not target_item:
            error(f"Sorry, you do not posses a {target}.")
            return

        if not PLAYER.has_item(target_item.key):
            error(f"Sorry, you do not posses a {target}.")
            return

        consume_message = target_item.get_consume_message(action)

        if not consume_message:
            error(f"Sorry, your {target_item.name} is not {action}able.")
            return

        PLAYER.remove(target_item.key)

        self.text_delay(consume_message)
        
        if target_item.health_change:
            PLAYER.change_health(target_item.health_change)
            wrap(f"You feel your health change by {target_item.health_change}.")

class Eat(Consume):
    def do(self):
        """Performs the Eat action by calling the Consume action"""
        if not self.arg_string:
            error("You cannot eat nothing.")
            return
        
        action = 'eat'
        self.consume(self.arg_string, action)

class Drink(Consume):
    def do(self):
        """Performs the Eat action by calling the Consume action"""
        if not self.arg_string:
            error("You cannot drink nothing.")
            return
        
        action = 'drink'
        self.consume(self.arg_string, action)

#TODO generate this dynamically with a dunder method called "subclasses" or somesuch
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
    "e": Eat,
    "eat": Eat,
    "drink": Drink,
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
            #TODO change things to make args positional
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