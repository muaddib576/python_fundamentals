"""."""

# Polish:
    # Add some delay to the various messages?
    # add flavor text to all descriptions
        # how will player know to pet?    
    # Cleanup/add command aliases
        # NOTE: you mostly implemented this, just need to validate and write a test to check for dupe aliases (you started test_action_keys)
    # make n/e/s/w aliases for north/east/etc ******DONE******

# Features:
    # Alissa suggested maybe replacing the "shop" command with a menu in the shop that the player can "read"
        # would need to have the writing dynamically generated. Think about it and discuss with Alissa
        # the "read shop menu" suggestion was about making a clear distinction between the shop inventory and the shop location inventory
    # should I add a sell command? Is there a gameplay reason for this? ...immersion?
    # NOTE: maybe should there be a contingency if more than 1 qty is passed by the player? ""Sorry im confused, how many did you say??""
        # Alissa: start with some GIVEN WHEN THENS to identify what is expected player behavior and then decide what to do

# Bugs:

# Alissa feedback after playing:
    # dragons are easy to deal with once you know which is which
        # Brian's thought: maybe make the health penalty more severe?
                         # Or maybe reshuffle the moods after the player leaves the location? "the red head is moody today"?
                         # Or each head cycles through the options? 

# NILA feedback
    # forgot examine command, maybe should add list of commands?
        # Brian's thought: help command? sign in town the player can read with a list of "accomplishments" from other adventurers? That takes coins to unlock more hints?

from console import fg, bg, fx

from python_fundamentals.adventure_game.params_and_functions import (
    debug,
    error,
    abort,
    start_message,
    defeat,
)

from python_fundamentals.adventure_game.classes import InvalidItemError

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

# Even though it is not directly used in main.py, you need to import this so the dicts are initialized
from python_fundamentals.adventure_game import items_and_locations

import python_fundamentals.adventure_game.player as player

def gen_action_dict():
    """Generates a dictionary of all alias/command pairs"""
    action_dict = {}
    command_list = [Quit,
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
]

    for command in command_list:
        for alias in command.aliases:
            action_dict[alias] = command

    return action_dict

# TODO this is the old action_dict, you just need to validate it is the same as the new one (aside from the additions) then you can delete
# action_dict = {
#     "q": Quit,
#     "quit": Quit,
#     "l": Look,
#     "look": Look,
#     "s": Shop,
#     "shop": Shop,
#     "g": Go,
#     "go": Go,
#     "e": Examine,
#     "examine": Examine,
#     "inspect": Examine,
#     "t": Take,
#     "take": Take,
#     "grab": Take,
#     "pickup": Take,
#     "i": Inventory,    
#     "inventory": Inventory,
#     "bag": Inventory,
#     "d": Drop,    
#     "drop": Drop,
#     "b": Buy,
#     "buy": Buy,
#     "purchase": Buy,
#     "r": Read,
#     "read": Read,
#     "p": Pet,
#     "pet": Pet,
#     "eat": Eat,
#     "drink": Drink,
# }

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