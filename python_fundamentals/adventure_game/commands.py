
from console import fg, bg, fx

from python_fundamentals.adventure_game.params_and_functions import (
    write,
    error,
    debug,
    header,
    wrap,
    victory,
    MARGIN,
)

from python_fundamentals.adventure_game.classes import (
    Command,
    Place,
    Item,
    Dragon_head,
)

from python_fundamentals.adventure_game import player

class Quit(Command):
    aliases = ['quit', 'q']

    def do(self):
        """Ends the game"""
        write("Goodbye. Thanks for playing!")
        quit()

class Look(Command):
    aliases = ['look','l']

    def do(self):
        """Lists the items present in the current location, and all nearby locations"""

        debug(f"Trying to look around.")

        current_place = self.player_place

        # Display info about the current location
        header(f"{current_place.name}")
        wrap(f"{current_place.description}")

        # Display list of the items in the current location
        if current_place.inventory:
            item_names = [Item.item_dict[x].name for x in current_place.inventory]
            
            wrap(f"You see {self.comma_list(item_names)} nearby.")

        if current_place.shop_inventory:
            shop_item_names = [Item.item_dict[x].name for x in current_place.shop_inventory]
            
            wrap(f"Behind the counter, the shopkeeper has {self.comma_list(shop_item_names)} prominently displayed.")

        for direction in self.compass:
            nearby_name = getattr(current_place, direction)

            if nearby_name:
                write(f"To the {fg.lightcyan(direction)} is {fg.lightcyan(Place.get(nearby_name).name)}.")

class Shop(Command):
    aliases = ['shop','s']

    def do(self):
        """Does the shop, duh"""

        current_place = self.player_place

        if not current_place.place_can('shop'):
            error(f"Sorry, you can't shop here.")
            return

        header("Whater you buyin'?\n")

        for key, qty in current_place.shop_inventory.items():
            item = Item.item_dict.get(key)
            if item.is_for_sale():

                prefix_text = f"${abs(item.price):>2d}. {item.name.title()} x{qty} : "
                full_text = f"{prefix_text}{item.description}"

                prefix_len = ' ' * len(f"{MARGIN}{prefix_text}")

                wrap(text=full_text,
                     subsequent_indent=prefix_len
                )

        print()

class Buy(Command):
    aliases = ['buy','b','purchase']

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
        
        current_gems = player.PLAYER.inventory.get("gems", 0)

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

        current_place.buy(target_item.key, item_cost, qty)

        wrap(f"You bought {qty} {target_item.name} for {item_cost} gems and put it in your bag.")

class Goroot(Command):
    aliases = ['go','g','walk']

    def goroot(self, direction):
        """Moves to the specified location"""  

        if not self.arg_string:
            error("You must specify a location.")
            return

        current_place = self.player_place

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
        compass_aliases = {'n':'north',
                           'e':'east',
                           's':'south',
                           'w':'west'
        }

        # accounts for player using n/s/e/w instead of full direction
        if direction in compass_aliases.keys():
            direction = compass_aliases[direction]

        if direction not in self.compass:
            error(f"Sorry, there is no '{direction}'")
            return

        if current_place.key == 'misty-woods': #this could be replaced with kwarg bool?
            # misty_path = ['s','w','s','e','s']
            misty_path = current_place.misty_path
            path_length = len(misty_path)
            
            current_place.current_path += direction[:1]
            current_length = len(current_place.current_path)

            if current_place.current_path == misty_path:
                victory()
                return

            if len(current_place.current_path) == path_length:
                new_place = current_place.go('egress_location')
                current_place.current_path = []

                wrap(f"After wondering in circles for hours, you find yourself back where you started:")
                header(new_place.name)
                wrap(new_place.description)
                return

            # Now we move through the misty path and descriptions
            new_place = current_place.go(direction)

            if new_place:
                wrap(f"You spend some time walking {direction} and come upon:")
                header(new_place.name)
                wrap(new_place.misty_descriptions[current_length-1])
                return

        self.goroot(direction)

class Examine(Command):
    aliases = ['examine','e','inspect']

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

        if not current_place.has_item(target_item.key) and not current_place.has_shop_item(target_item.key) and not player.PLAYER.has_item(target_item.key):
            error(f"There is no {target} in {current_place.name.lower()}.")
            return

        header(target_item.name.title())
        wrap(f"{target_item.description} {target_item.get_health_change_text()}")
        if current_place.place_can('shop') and current_place.has_shop_item(target_item.key) and target_item.is_for_sale():
            print()
            wrap(f"The shop has {current_place.shop_inventory[target_item.key]}, you can buy one for {abs(target_item.price)} gems.")
            return

class Take(Command):
    aliases = ['take','t','grab','pickup']

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
            wrap(f"Sorry, there are not {qty} {target} available to take here.")

            if current_place.has_shop_item(target_item.key,qty):
                wrap(f"The shop has {qty} {target} but you are no thief.")
            return

        if not target_item.can_take:
            wrap(f"You try to pick up {target_item.name}, but it doesn't budge.")
            return  

        player.PLAYER.add(target_item.key, qty)
        current_place.remove(target_item.key, qty)

        wrap(f"You pick up {qty} {target_item.name} and put it in your bag.")

class Inventory(Command):
    aliases = ['inventory','i','bag']

    def do(self):
        """Displays the current contents of the player inventory"""

        debug("Trying to show player inventory.")

        self.health_bar()

        print()

        if not player.PLAYER.inventory:
            write("Inventory empty.")
            return

        for name, qty in player.PLAYER.inventory.items():
            item = Item.get(name)
            write(f"(x{qty:>2}) {item.name}")

class Drop(Command):
    aliases = ['drop','d']

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

        if player.PLAYER.has_item(target_item.key, qty):
            player.PLAYER.remove(target_item.key, qty)
            current_place.add(target_item.key, qty)
            wrap(f"You dropped {qty} {target_item.key} on the ground.")
            return

        error(f"You dont have {qty} {target_item.key} to drop.")

class Read(Command):
    aliases = ['read','r']

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

        if not (current_place.has_item(target_item.key) or player.PLAYER.has_item(target_item.key)):
            error(f"There is no {target} here.")
            return

        if target_item.writing == None:
            error("There is nothing to read.")
            return

        wrap(target_item.writing["title"])
        if "image" in target_item.writing:
            wrap(target_item.writing["image"], initial_indent=MARGIN*2, subsequent_indent=MARGIN*2, is_image=True)
        if "message" in target_item.writing:
            wrap(target_item.writing["message"], initial_indent=MARGIN*2, subsequent_indent=MARGIN*2)

class Pet(Command):
    aliases = ['pet','p']

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

        if color not in Dragon_head.dragon_dict.keys():
            error("You do not see such a dragon.")
            return
        
        target_dragon = Dragon_head.dragon_dict[color]

        treasure = target_dragon.calc_treasure()
        damage = target_dragon.calc_damage()

        player.PLAYER.add("gems",treasure)
        damage_dealt = player.PLAYER.change_health(-damage)

        sentences = [
            "You slowly creep forward...",
            "...gingerly reach out your hand...",
            f"...and gently pet the dragon's {target_dragon.key} head.",
            "...",
            f"He blinks his eyes and peers at you...",
        ]

        self.text_delay(sentences)
        print()
        wrap(target_dragon.mood_text(treasure, damage_dealt))

class Consume(Command):
    def consume(self, args, action):
        """Performs the Consume action on the specified item"""

        target = self.arg_string
        target_item = Item.find(target)

        if not target_item:
            error(f"Sorry, you do not posses a {target}.")
            return

        if not player.PLAYER.has_item(target_item.key):
            error(f"Sorry, you do not posses a {target}.")
            return

        consume_message = target_item.get_consume_message(action)

        if not consume_message:
            error(f"Sorry, your {target_item.name} is not {action}able.")
            return

        player.PLAYER.remove(target_item.key)

        self.text_delay(consume_message)
        
        if target_item.health_change:
            
            change = player.PLAYER.change_health(target_item.health_change)
            
            wrap(f"You feel your health change by {change}.")

class Eat(Consume):
    aliases = ['eat']

    def do(self):
        """Performs the Eat action by calling the Consume action"""
        if not self.arg_string:
            error("You cannot eat nothing.")
            return
        
        action = 'eat'
        self.consume(self.arg_string, action)

class Drink(Consume):
    aliases = ['drink']

    def do(self):
        """Performs the Eat action by calling the Consume action"""
        if not self.arg_string:
            error("You cannot drink nothing.")
            return
        
        action = 'drink'
        self.consume(self.arg_string, action)