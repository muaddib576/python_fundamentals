import random

number = random.randint(1, 20)
difficulty_modes = ["easy", "normal", "hard"]
difficulty = ()

player = input("Hello! What is your name? ")

while difficulty not in difficulty_modes:
    difficulty = input("Hello " + player + "! Would you like to play on easy, normal or hard mode? ").lower()
    if difficulty == 'easy':
        max_guesses = 8
    elif difficulty == 'normal':
        max_guesses = 6
    elif difficulty == 'hard':
        max_guesses = 4

if player.lower() == 'brian':
    print("I am thinking of a number between 1 and 20. Hint for Brians: The number is between", (number -1), "and", str((number + 1)) + ".")
else:
    print("I am thinking of a number between 1 and 20.")

for guess_count in range(1, (max_guesses+1)):
    print("Guess ", guess_count, "of", max_guesses)
    guess = input("Your guess: ")
    guess = int(guess)
    current_delta = abs(guess - number)

    if guess_count > 1:
        if guess == number:
            pass
        elif current_delta < previous_delta:
            print("You are getting warmer.")
        elif current_delta > previous_delta:
            print("You are getting colder.")

    previous_delta = abs(guess - number)

    if guess < number:
        print('Your guess is too low.')
    elif guess > number:
        print('Your guess is too high.')
    else:
        break

if guess == number:
    guess_count = str(guess_count)
    max_guesses = str(max_guesses)
    winner_messages = ["Good job, " + player + ". You actually guessed the correct number in " + guess_count + " guesses.",
                       "Wow, " + player + "it seems you don't totally suck. You got a " + guess_count + " out of " + max_guesses + ".",
                       "Neat, it only took you " + guess_count + " guesses! If only you were as good at life as you are at guessing."
    ]
    print(winner_messages[random.randint(0,len(winner_messages)-1)])

else:
    number = str(number)
    loser_messages = ["WRONG. Wrong wrong wrong. You should have picked " + number + ". But you dumb.",
                      "Incorrect. Sorry, but the number I was thinking of was " + number + ".",
                      "Wow, I thought this game was easy, but you sure proved me wrong. The number was " + number + " if you were wondering."
    ]
    print(loser_messages[random.randint(0,len(loser_messages)-1)])






# loops set global variables??