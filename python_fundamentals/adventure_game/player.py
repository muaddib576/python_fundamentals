
from time import time

MAX_HEALTH = 100

class Contents():
    """Class for objects with inventories/contents"""

    # NOTE: These two classes are in this file to prevent circular imports
    
    def has_item(self, key: str, qty: int=1, inventory: dict=None):
        """Return True if Object inventory has at least the specified quantity of key, else False"""

        if inventory is None:
            inventory = self.inventory

        return key in inventory and inventory[key] >= qty
    
    def has_shop_item(self, key, qty=1): #TODO this method seems redundant after the refactor?
        """Return True if Object shop_inventory has at least the specified quantity of key, else False"""

        return key in self.shop_inventory and self.shop_inventory[key] >= qty
    
    def add(self, item, qty=1, inventory: dict=None): 
        """Adds X item from specified inventory"""
       
        if inventory is None:
            inventory = self.inventory

        inventory.setdefault(item, 0)
        inventory[item] += qty

    def remove(self, item: str, qty: int=1, inventory: dict=None):
        """Remove X item from specified inventory"""

        if inventory is None:
            inventory = self.inventory
        
        if self.has_item(item, qty, inventory):
            inventory[item] -= qty

        if inventory[item] <= 0: # remove item from inventory if quantity is 0 or less
            del inventory[item]

class Player(Contents):

    # NOTE: These two classes are in this file to prevent circular imports

    def __init__(self, place=None, current_health=None, status_effects=None, inventory={}):
        self.place = place
        self.current_health = current_health
        self.status_effects = status_effects
        self.inventory = inventory

    def change_health(self, amount):
        """Adjusts the players health by the given amount. Does not drop below 0 or above max."""
        start_health = self.current_health
        
        self.current_health += amount

        if self.current_health > MAX_HEALTH:
            self.current_health = MAX_HEALTH
        elif self.current_health < 0:
            self.current_health = 0

        return self.current_health - start_health
    
    def add_status(self, status, duration):
        """Adds a status effect to the player for the given duration (in seconds)"""
        
        expires_at = time() + duration
        self.status_effects[status] = expires_at

    def check_status(self, status):
        """Returns True if player has the given status effect, else False. Also, removes expired statuses"""
        
        expires_at = self.status_effects.get(status)
        # TODO: Does this work if the status is not present? WRITE TESTS REGARDLESS

        if not expires_at:
            return False
        if time() >= expires_at:
            del self.status_effects[status]
            return False
        return True

PLAYER = Player(
    place="home",
    current_health = 100,
    status_effects = {},
    inventory = {},
)