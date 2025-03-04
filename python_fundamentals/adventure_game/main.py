


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