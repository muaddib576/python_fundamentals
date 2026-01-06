"""."""

# Polish:
    # Add some delay to the various messages?
    # light refactor to make some loops more pythonic?
    # Add and/or remove unused items/places to streamline gameplay
    # You have a few random TODO:s, review and address/remove them

# Features:
    # Alissa suggested maybe replacing the "shop" command with a menu in the shop that the player can "read"
        # would need to have the writing dynamically generated. Think about it and discuss with Alissa
        # the "read shop menu" suggestion was about making a clear distinction between the shop inventory and the shop location inventory
    # Alissa's feedback: dragons are easy to deal with once you know which is which
        # Shuffle the moods after each pet. But eating the mushrooms found in the forrest gives player a status effect with lets them see the cheerful head's aura
            # need to add/change:
                # add player.current_status to the inventory output?
                    # convert the s to m where relevant??
                # update player status after eating mushrooms
                # for fun: maybe some text color change and/or animation when examining anything while player.status == 'fried'?
                    # lolcat library
                    # Will need to update the wrap() and write() functions to reference player.current_status
                # when using inventory/examine and player.status == 'fried' then player can see mood/aura colors
                    # perhaps update the wrap()/write() functions to reference player.current_status
                # remove the 'fried' status after either:
                    # a set number of player actionsii
                    # a set time period IRL??
                # in-game breadcrumbing about mushroom effects wrt dragon auras
                # renewable mushrooms (shop sells them? Forrest shrooms respawn over time?)
                # check the balance of the reward/punishments from the moods
                # for fun: maybe add a 'sick' status if the player eats too many mushrooms?

from console import fg, bg, fx

from python_fundamentals.adventure_game.params_and_functions import (
    debug,
    error,
    abort,
    start_message,
    defeat,
)

# DO I not need this anymore??
from python_fundamentals.adventure_game.commands import (
    Quit,
    Look,
    Shop,
    Go,
    Examine,
    Take,
    Inventory,
    Drop,
    Buy,
    Read,
    Pet,
    Eat,
    Drink,
)

from python_fundamentals.adventure_game.classes import (
    Command,
    InvalidItemError,
)

# Even though it is not directly used in main.py, you need to import this so the dicts are initialized
from python_fundamentals.adventure_game import items_and_locations

import python_fundamentals.adventure_game.player as player

def gen_action_dict():
    """Generates a dictionary of all alias/command pairs"""
    
    action_dict = {}
    # Loop through Command class to get the aliases attributes
    for sub_command in Command.__subclasses__():
        if hasattr(sub_command, 'aliases'):
            for alias in sub_command.aliases:
                action_dict[alias] = sub_command

        # because Go is as subclass for Goroot, one more loop is needed
        for sub_sub_command in sub_command.__subclasses__():
            if hasattr(sub_sub_command, 'aliases'):
                for alias in sub_sub_command.aliases:
                    action_dict[alias] = sub_sub_command

    return action_dict

def initialize_world():
    """Initializes the game world. For now, just shuffles the dragon moods. Eventually, may refactor everything to do more."""
    
    if len(items_and_locations.DRAGON_HEADS) != len(items_and_locations.Dragon_head.MOODS):
        error("Error initializing game world: number of dragon heads does not equal number of dragon moods.")
        quit()

    # Shuffle the dragon moods at the start of the game
    items_and_locations.Dragon_head.shuffle_moods()

def main():
    initialize_world()
    
    action_dict = gen_action_dict()

    start_message()

    while True:
        print()

        debug(f"You are at: {player.PLAYER.place}")

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

            # If the player passes more than one qty, the cmd should not be do()ed
            if len(cmd.arg_qty) > 1:
                error("Sorry, that is too many numbers. Slow down and try again.")
                continue

            try:
                cmd.do()
            except (InvalidItemError) as e:
                abort(str(e))
        else:
            error("No such command.")
            continue

        if player.PLAYER.current_health == 0:
            defeat()

if __name__ == "__main__":
    main()