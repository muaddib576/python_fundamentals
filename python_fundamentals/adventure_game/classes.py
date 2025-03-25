from time import sleep
from random import choice, randint

from python_fundamentals.adventure_game.params_and_functions import (
    write,
    error,
    abort,
    BAR,
    # MAX_HEALTH,
    DELAY,
)

from python_fundamentals.adventure_game.player import (
    Contents,
    PLAYER,
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
    place_dict = {}
    item_dict = {}
    def __init__(self, key, name, description):
        self.key = key
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<{self.__class__.__name__} object={self.name}>"

# class Contents():
#     """Class for objects with inventories/contents"""
    
#     def has_item(self, key: str, qty: int=1, inventory: dict=None):
#         """Return True if Object inventory has at least the specified quantity of key, else False"""

#         if inventory is None:
#             inventory = self.inventory

#         return key in inventory and inventory[key] >= qty
    
#     def has_shop_item(self, key, qty=1): #TODO this method seems redundant after the refactor?
#         """Return True if Object shop_inventory has at least the specified quantity of key, else False"""

#         return key in self.shop_inventory and self.shop_inventory[key] >= qty
    
#     def add(self, item, qty=1, inventory: dict=None): 
#         """Adds X item from specified inventory"""
       
#         if inventory is None:
#             inventory = self.inventory

#         inventory.setdefault(item, 0)
#         inventory[item] += qty

#     def remove(self, item: str, qty: int=1, inventory: dict=None):
#         """Remove X item from specified inventory"""

#         if inventory is None:
#             inventory = self.inventory
        
#         if self.has_item(item, qty, inventory):
#             inventory[item] -= qty

#         if inventory[item] <= 0: # remove item from inventory if quantity is 0 or less
#             del inventory[item]

class Place(Collectable, Contents):
    def __init__(self, key, name, description, north=None, east=None, south=None, west=None, can=None, inventory=None, shop_inventory=None, egress_location=None, misty_path=None, current_path=None, misty_descriptions=None):
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
        self.misty_path = misty_path
        self.current_path = current_path
        self.misty_descriptions = misty_descriptions

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
    def get(cls, key, default=None):
        """Takes a place key and returns the Place's instance"""
        place = cls.place_dict.get(key, default)

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

        if item_cost > 0: # the player might be able to 'buy' an item for no cost, so we check first
            PLAYER.remove('gems',item_cost)
        
        self.remove(item, qty, self.shop_inventory)

        self.add('gems', item_cost, self.shop_inventory)

class Item(Collectable):
    def __init__(self, key, name, description, aliases=None, writing=None, can_take=False, price=None, drink_message=None, eat_message=None, health_change=None):
        super().__init__(key, name, description)
        self.aliases = aliases or []
        self.writing = writing
        self.can_take = can_take
        self.price = price
        self.drink_message = drink_message
        self.eat_message = eat_message
        self.health_change = health_change

    @classmethod
    def get(cls, key, default=None):
        """Takes an item key and returns the Item's instance"""
        item = cls.item_dict.get(key, default)

        if item:
            return item
        else:
            raise InvalidItemError(f"This is embarrassing, but the information about {key} is missing.")

    @classmethod
    def find(cls, key):
        """Returns an item's instance if passed an alias or key for the item"""

        target_key = ''

        for instance in cls.item_dict.values():
            # Check if player's key matched with item key, name, or unpacked alias list
            if key in (instance.key, instance.name, *instance.aliases):
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
    
