import random

'''print("#1.", 'F' > 'z')
    #1 false

print("#2.", 0.0 == 0)
    #2 true

list1 = [2, 2, 3, 3]
list2 = [2, 2, 4, 3]
print("#3.", list1 > list2)
    #3 false

print("#4.", 'z' in 'zebra')
    #4 true

list3 = [1, 2, 4]
print("#5.", 5 in list3)
    #5 false


#truthy falsy

print("#2.1", bool(-1))

print("#2.2", bool(" "))

print("#2.3", bool({}))

print("#2.4", bool([0]))'''

'''---------------------------------------------------------------------'''

def toss_coin():
    """Basic coin toss, no user input"""
    coin = random.randint(0,1)
    if not coin:
        print("You lose the coin toss.")
    else:
        print("You win the coin toss.")

# toss_coin()

'''---------------------------------------------------------------------'''
#guessing game

def guessing_game():
    """Prints if a random number was close to specified number"""
    pick = 12
    guess = random.randint(1,100)
    delta = pick - guess

    print("The computer guessed " + str(guess) + ".")

    if guess == pick:
        print("The computer got it right!")
    # elif abs(pick - guess) <= 30:
    # elif guess >= pick-30 and guess <= pick+30:
    elif delta <= 30 and delta >= -30:
        print("The computer was close.")
    else:
        print("The computer got it wrong.")

'''---------------------------------------------------------------------'''

def coin_toss_2():
    """Proper coin toss with user input and everything"""
    coin = ["heads", "tails"]
    player_call = ""

    while player_call not in coin:
        player_call = input("Heads or tails? Choose wisely: ")
        player_call = player_call.lower()
        
        if player_call not in coin:
            print("It's just a normal coin, you must enter 'heads' or 'tails'. This is not hard...")

    coin_flip = coin[random.randint(0,1)]

    if player_call == coin_flip:
        print("The coin landed on " + coin_flip + ". You win!")
    else:
        print("The coin landed on " + coin_flip + ". You lose!")


