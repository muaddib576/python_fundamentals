from pathlib import Path
from datetime import datetime
import random
import shutil



terminal_size = shutil.get_terminal_size()
width = terminal_size[0]

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

def scorekeeper(path, correct, total):
    """logs the results in score_log.csv"""
    
    incorrect = total - correct
    dt = datetime.today()
    ts = dt.timestamp()
    ts = int(ts)

    if not path.exists():
        print(f"ERROR: {path} does not exist")
        return 

    with open(path, 'a') as ch:
         ch.write(f"{ts},{correct},{incorrect}\n")

    print("This outcome has been recorded for posterity.")



def play(play_cards):
    """Takes the formatted cards and challenges the player"""

    score = 0
    denom = len(play_cards)
    i = 0

    while play_cards:
        
        card = random.choice(play_cards)
        play_cards.remove(card)
        i += 1

        print()
        print("=" * width)
        print("|", end = "")
        print(f"Flashcard {i} of {denom}".center(width-2), end = "")
        print("|")
        print("|", end = "")
        print("Hey there Dummy, here's an easy one:".center(width-2), end = "")
        print("|")
        print("|", end = "")
        print(f"How do you {card['front']}?".center(width-2), end = "")
        print("|")
        print("=" * width)

        answer = input("\nAnswer: ")

        if answer == card["back"]:
            print("Not as dumb as you look... CORRECT")
            score += 1
            continue
        
        print(f"Whoops. Sorry I was looking for: {card['back']}")
        print()

    print("Game Over".center(width))

    print(".-=========-.".center(width))
    print("('-=======-')".center(width))
    print("_|   .=.   |_".center(width))
    print(f"((|  {score} of {denom} |))".center(width))
    print("\|   /|\   |/".center(width))
    print("\__ '`' __/".center(width))
    print("_`) (`_".center(width))
    print("_/_______\_".center(width))
    print("(___________)".center(width))

    return score, denom

def main():
    """does the main thing"""

    card_path = Path.cwd() / "data/flashcards/paths.csv"
    log_path = Path.cwd() / "data/flashcards/score_log.csv"

    cards = load_csv(card_path)

    if cards == False:
        print("Error: someth went wrong.")
        return
    
    results = play(cards)

    scorekeeper(log_path, results[0], results[1])

main()