'''import random

def check_level(character_level):
    print(f"You are a %s level {character_level} %s adventurer." %(check_rank(character_level)))

# def check_rank(level_check):
#     if level_check <= 3:
#         return "pathetic", "novice"
#     elif level_check <= 7:
#         return "passable", "intermediate"
#     elif level_check > 7:
#         return "formidable", "bomb-ass"

def check_rank(level_check):
    if level_check <= 3:
        character_rank = "pathetic", "novice"
    elif level_check <= 7:
        character_rank = "passable", "intermediate"
    elif level_check > 7:
        character_rank = "formidable", "bomb-ass"
    return character_rank

level = random.randint(1,10)

check_level(level)'''


'''def return_two_values():
    a = 40
    b = 2
    c = 5
    return a,b,c

print("First value = %d,  Second value = %d, 3rd value = %d" %(return_two_values()))'''

# inter = int(input())

# for inter in range(300):
#     print('Hello! i is set to', inter)
'''
player = 'Moop'
guess_count = 3
max_guesses = 6
guess_count = str(guess_count)
max_guesses = str(max_guesses)

mylist = ["Good job, " + player + " you actually guessed the correct number in " + guess_count + " guesses.",
                    "Wow, " + player + " it seems you don't totally suck. You got a " + guess_count + " out of " + max_guesses + ".",
                    "Neat, it only took you " + guess_count + " guesses! If only you were as good at life as you are at guessing."]

x = len(mylist)
print(mylist[0])'''
'''
player = input("Hello! What is your name? ")

pclass = input("what do you want to do with your life? ")

print()'''

import random

number = random.randint(1, 20)
max_guesses = 6

player = input("Hello! What is your name? ")
print("Hello " + player + ".")
print("I am thinking of a number between 1 and 20.")
print()

for guess_count in range(1, (max_guesses+1)):
    print("Guess", guess_count, "of", max_guesses)

    guess = input("Your guess: ")
    guess = int(guess)

    if guess < number:
        print('Your guess is too low.')

    elif guess > number:
        print('Your guess is too high.')

    else:
        break

    print()


if guess == number:
    guess_count = str(guess_count)
    print("Good job, " + player + "! You guessed my number in " + guess_count + " guesses!")

else:
    number = str(number)
    print("Nope. The number I was thinking of was " + number + ".")