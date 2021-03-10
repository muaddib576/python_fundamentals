'''
Alissa notes:
Note: add a failure response.
Note our previous conversation about using an if statement here instead of using a set to dedupe. (line 16)
great practice of while loops here, but there's a simpler way to do this with simple arithmetic. Think you can figure it out?
'''



guessed = []
word = "potato"

def remaining_letters():
    """calculates the remaining blank spaces"""

    remaining = len(word)

    for x in guessed:
        if x in word:
            remaining -= 1
    
    return remaining

def main():
    """Hangs someone if you fail"""
    i = 0
    while i < 6:
        print("Chances: " + ("x" * i) + ("_" * (6-i)))
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

        player_guess = ""

        while len(player_guess) != 1:
            player_guess = input("Please enter a SINGLE letter: ")
            
            while player_guess in guessed:
                player_guess = input("You already guess that letter, ya doof. Try again: ")

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