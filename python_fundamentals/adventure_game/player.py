

MAX_HEALTH = 100

class Contents():
    """Class for objects with inventories/contents"""
    
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
    def __init__(self, place=None, current_health=None, inventory={}):
        self.place = place
        self.current_health = current_health
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

PLAYER = Player(
    place="home",
    current_health = 100,
    inventory={
                # 'gems':2,
                # 'map':1,
                # "potion":1
               },
)