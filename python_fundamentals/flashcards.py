from pathlib import Path
import random

def load_csv(path):
    """does a specific thing"""

    if not path.exists():
        print(f"ERROR: {path} does not exist")
        return

    print(f"loading file: {path}")

    card_list = []
    
    with open(path) as ch: 

        for i, line in enumerate(ch.readlines(), 1):
            card_dict = {'front': "", 'back': ""}
            row = line.split(",")

            if len(row) != 2:
                print("Error: the input file is not proper format.")
                return

            card_dict['front'] = row[0].strip()
            card_dict['back'] = row[1].strip()

            #removes any header Front/Back line
            if card_dict['front'].lower() == "front":
                continue

            card_list.append(card_dict)

    return card_list

def play(play_cards):
    """Takes the formatted cards and challenges the player"""

    score = 0
    denom = len(play_cards)
    i = 1

    while play_cards:
        
        card = random.choice(play_cards)
        play_cards.remove(card)

        print("=" * 20)
        print(f"Flashcard {i} of {denom}")
        i += 1
        print("=" * 20)

        answer = input(f"Hey there Dummy, here's an easy one: \nHow do you {card['front']}?\nAnswer: ")

        if answer == card["back"]:
            print("Not as dumb as you look... CORRECT")
            score += 1
            continue
        
        print(f"Whoops. Sorry I was looking for: {card['back']}")

    print("=" * 20)
    print(f"Final Score: {score} out of {denom}")
    print("=" * 20)

def main():
    """does the main thing"""

    card_path = Path.cwd() / "data/flashcards/paths.csv"

    cards = load_csv(card_path)

    if cards == False:
        print("Error: someth went wrong.")
        return
    
    play(cards)

main()