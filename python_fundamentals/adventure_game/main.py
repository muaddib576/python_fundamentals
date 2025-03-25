"""."""

# Polish:
    # Add some delay to the various messages?
    # add flavor text to all descriptions
        # how will player know to pet?    
    # Cleanup/add command aliases
    # make n/e/s/w aliases for north/east/etc
    # Should I split the game out into multiple files? eg one for the PLACES/ITEMS, one for the command classes, etc

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

# Conversion to multiple files
    # split Player class and PLAYER into a separate file
    # might even want to split classes into even smaller files (eg base classes in one file)
        # Alissa says that she would actually have each class be its own file, but this might be too much for me now
    # UPDATE: your tests are failing likely due to the changes made to the Item/Place classmethods and how the test deepcopy works?? Unsure

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

from python_fundamentals.adventure_game.items_and_locations import PLAYER #TODO this is circular?

#TODO generate this dynamically with a dunder method called "subclasses" or somesuch?
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
    "inspect": Examine,
    "t": Take,
    "take": Take,
    "grab": Take,
    "pickup": Take,
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
    "eat": Eat,
    "drink": Drink,
}

def main():

    start_message()

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

        if PLAYER.current_health == 0:
            defeat()

if __name__ == "__main__":
    main()