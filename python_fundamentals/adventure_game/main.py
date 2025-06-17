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
    # NOTE: maybe should there be a contingency if more than 1 qty is passed by the player? ""Sorry im confused, how many did you say??""
        # Alissa: start with some GIVEN WHEN THENS to identify what is expected player behavior and then decide what to do
    # Alissa's feedback: dragons are easy to deal with once you know which is which
        # Brian's thought: maybe make the health penalty more severe?
                         # Or maybe reshuffle the moods after the player leaves the location? "the red head is moody today"?
                         # Or each head cycles through the options? 

from console import fg, bg, fx

from python_fundamentals.adventure_game.params_and_functions import (
    debug,
    error,
    abort,
    start_message,
    defeat,
)

from python_fundamentals.adventure_game.classes import InvalidItemError

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

def main():

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