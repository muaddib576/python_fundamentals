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
                # in-game breadcrumbing about mushroom effects wrt dragon auras
                # switch to randomizing dragon moods
                # player status (good for 2 player actions? or just have a IRL time check)
                # renewable mushrooms (shop sells them? Forrest shrooms respawn over time?)
                # check within examine to see aura when player.status == 'fried'
                # check the balance of the reward/punishments from the moods
                # for fun: maybe some text color change and/or animation when examining anything while player.status == 'fried'?
                    # lolcat library

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