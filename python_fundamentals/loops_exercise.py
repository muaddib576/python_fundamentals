import time
import random

def delay(delay_amount):
    time.sleep(delay_amount)

#1------------------------------

def doin_call():
    """Asks user to pick a valid coin face."""
    coin = ["heads", "tails"]

    player_call = ""

    while player_call not in coin:
        player_call = input("Heads or tails? ").lower()

        if player_call not in coin:
            print("Guess again, Batman!")

    print("You picked", player_call)

#2------------------------------

def num_gen_loop():
    """Generates random numbers until a certain min value is reached"""
    number = 0
    loop_count = 0
    threshold = 50

    while number <= threshold:
        number = random.randint(1,100)
        loop_count += 1
        print(number)

    print("It took", loop_count, "tries to get a number greater than", str(threshold) + ".")

#3------------------------------

def ran_num_collector():
    """"Generates numbers until stopped by user or 10 iterations"""
    loop_count = 0

    while loop_count < 10:
        loop_count += 1
        number = random.randint(1,100)
        print("Here's a random number:", number)
        if loop_count < 10:
            reply = input("Continue? ").lower()
        if reply in ["n","no","naw"]:
            print("Ok, I will stop now.")
            break

#4-----------------------------

def roll_collector():
    """Rolls a D6 and adds to list of rolls if user wants"""
    accepted_yesses = ["y","yes","yah"]
    accepted_noes = ["n","no","naw"]

    rolls = []
    loop_count = 0

    while loop_count < 10:
        loop_count += 1
        number = random.randint(1,6)
        print("You rolled:", number)
        reply = input("Do you want to keep this roll? ").lower()

        while reply not in accepted_yesses and reply not in accepted_noes:
            print("It's a 'yes' or 'no' kind of question...")
            print("Your roll is still a", number)
            reply = input("Do you want to keep this roll? ").lower()

        if reply in accepted_noes:
            continue
        rolls.append(number)

    print(rolls)

#5 incrementing------------------

def countdown():
    """Iterates 3 times and prints number each time"""
    i = 3

    while i != 0:
        print("The current number:", i)
        i -= 1
        time.sleep(1)

# Iterating over a list 1---------

def lunch_menu():
    """Print lunch menu options"""
    i = 0
    menu = ['pizza', 'tacos', 'pasta', 'soup']

    while i < len(menu):
        if i == 0:
            print("Lunch options:")
        print(str(i+1) + ".", menu[i])
        i += 1

# Iterating over a list 2---------

def vowel_get():
    """Prints the position of each vowel in a given word"""
    vowels = ['a','e','i','o','u','y']
    word = input("Give me a word, please: ")
    i = 0

    while i < len(word):
        if word[i] in vowels:
            print("Position:", i+1, "Vowel:", word[i])
        i += 1

#99 bottles of beer-------

def bottles_of_beer():
    """Prints the words for 99 bottles of beer"""
    i = 99

    def plur(quantity):
        if quantity == 1:
            return "bottle"
        else:
            return "bottles"

    while i > 0:
        print("---------------------------------")
        print(i, plur(i), "of beer on the wall.")
        time.sleep(1)
        print(i, plur(i), "of beer.")
        time.sleep(1)
        print("Take one down.")
        time.sleep(1)
        print("Pass it around.")
        time.sleep(1)
        print(i-1, plur(i-1), "of beer on the wall.")
        time.sleep(1.5)
        i -= 1

#-----------------------1/11 excersises---------------

#nested loops excercise------

def multi_table():
    """Prints a 10x10 multiplication table"""
    rows, cols = 10, 10
    r = 0

    #Header row creation
    # print("  |", "0","  1","  2","  3","  4","  5","  6","  7","  8","  9")
    # print("-","  -","  -","  -","  -","  -","  -","  -","  -","  -","  -")


    #Header row creation with iteration
    print(" ", end=" |")
    c = 0
    while c < cols:
        print(str(c).rjust(2), end="  ")
        c +=1
    print()
    print("-","  -","  -","  -","  -","  -","  -","  -","  -","  -","  -")

    #main multiplication table generation
    while r < rows:
        print(r, end=" |")
        c = 0
        while c < cols:
            output = str(r*c)
            print(output.rjust(2), end="  ")
            # delay(1)
            c += 1
        print("\n")
        r += 1

# multi_table()

#1---------------------------

def name_cheer():
    """Prints a chant based on the letters in my name"""
    name = 'Brian'
    i = 0

    while i < len(name):
        print("Gimme a letter!")
        delay(1)
        print(f"{name[i].upper()}!")
        delay(1)
        i += 1
    print("What's that spell?!")
    delay(1)
    print(f"{name}!")

# name_cheer()

#2---------------------------

def jolly_good():
    """Print For He's a Jolly Good Fellow song"""
    i = 3
    while i != 0:
        print("For he’s a jolly good fellow…")
        time.sleep(1)
        i-= 1
    print("Which nobody can deny!")

# jolly_good()

#3---------------------------

def days_of_xmas():
    """Prints the 12 Days of Christmas song"""

    gifts = [["First", "a partridge in a pear tree"],
            ["Second", "two turtle doves"],
            ["Third", "three french hens"],
            ["Fourth", "four calling birds"],
            ["Fifth", "five gold rings"],
            ["Sixth", "six geese a-laying"],
            ["Seventh", "seven swans a-swimming"],
            ["Eighth", "eight maids a-milking"],
            ["Ninth", "nine ladies dancing"],
            ["Tenth", "ten lords a-leaping"],
            ["Eleventh", "eleven pipers piping"],
            ["Twelfth", "twelve drummers drumming"]
            ]

    day = 0

    while day < 12:
        print(f"On the {gifts[day][0]} day of Christmas my true love sent to me:")
        gift_count = day
        while gift_count >= 0:
            #puts an 'and' before the first gift for all days after the first
            if gift_count == 0 and day > 0:
                print("And", end=" ")
                print(gifts[gift_count][1])
            else:
                print(gifts[gift_count][1].capitalize())
            gift_count -= 1
        print()
        day += 1

# days_of_xmas()


#4---------------------------

def hangman():
    """Hangs someone if you fail"""
    guessed = []
    word = "potato"

    def remaining_letters():
        """calculates the remaining blank spaces"""
        remaining = len(word)
        de_dupe_guessed = list(set(guessed))
        r = 0

        while r < len(de_dupe_guessed):
            remaining -= word.count(de_dupe_guessed[r])
            r += 1
        return remaining

    def main():

        i = 0
        while i < 6:
            print("Chances: " + ("x"*i) + ("_" * (6-i)))
            print(f"{remaining_letters()} letters remain: ", end="")
            
            #prints the word with "_" for unguessed letters
            l = 0
            while l < len(word):
                if word[l] in guessed:
                    print(word[l], end="")
                else:
                    print("_", end="")
                l += 1
            print("\n")

            player_guess = input("Please guess a single letter: ")

            while len(player_guess) != 1:
                player_guess = input("I said guess a SINGLE letter: ")

            if player_guess.lower() in word:
                print(f"Good job, '{player_guess}' is in the word!")
                guessed.append(player_guess)
            
            if remaining_letters() == 0:
                print(f"Congrats! You guessed every letter in the word '{word}'. No one dies today!")
                break

            i += 1
        if remaining_letters != 0:
            print(f"Ruh roh. The word was '{word}'. Your horrible spelling skills have once again resulted in death. Live with that.")
    main()

hangman()

# chances: xx____
# 5 letters: _e___


#--------1/18 Excercise------------

def scorecard():
    """Prints a scorecard for a 3 player 3 round game"""
    r = 0

    while r < 3:
        print(f"Round: {r+1}")
        p = 0
        print()
        while p < 3:
            print(f"Player {p+1} score:", end=" ")
            print("______________")
            p += 1
        print()
        r += 1

# scorecard()
