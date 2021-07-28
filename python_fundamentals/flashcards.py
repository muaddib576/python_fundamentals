from pathlib import Path
from datetime import datetime
import random
import shutil
import textwrap

TERMINAL_SIZE = shutil.get_terminal_size()
WIDTH = TERMINAL_SIZE[0]
CARD_PATH = Path.cwd() / "data/flashcards/paths.csv"
LOG_PATH = Path.cwd() / "data/flashcards/score_log.csv"
TOPICS = []

def load_card_csv(path):
    """Opens,reads, and returns the contents of the flashcards csv"""

    if not path.exists():
        print(f"ERROR: {path} does not exist")
        return

    print(f"loading file: {path}")

    card_list = []
    
    with open(path) as ch: 

        for i, line in enumerate(ch.readlines(), 1):
            
            # ignores any blank card lines
            if line == "\n":
                continue

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

def menu():
    """Populates a menu of the flashcard CSVs and makes the user pick one"""
    card_dir = Path.cwd() / "data/flashcards/"
    menu_options = ["0. All of 'em"]
    selection = []

    if not card_dir.is_dir():
        print(f"ERROR: {card_dir} does not exist")
        return

    for i, file_path in enumerate(card_dir.iterdir(),1):
        TOPICS.append(file_path)
        menu_options.append(f"{i}. {file_path.stem}")
    
    choices = input(f"Which topic do you desire?")

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

def load_scores(path):
    """loads all past scores"""
    #do the score line dicitonary here
    if not path.exists():
        print(f"ERROR: {path} does not exist")
        return 

    score_list = []

    with open(path) as ch:
        for i, line in enumerate(ch.readlines(), 1):
            row = line.strip()
            row = row.split(",")

            score_list.append(row)
    
    return score_list

def print_scores(past_scores):
    """It ain't fancy, but this formats and prints the scores from score_log.csv"""

    score_board = ''
    for line in past_scores:
        if line[0] == 'date':
            continue

        # make datetime object from epoch int
        dt = datetime.fromtimestamp(int(line[0]))
        
        total_cards = int(line[1])+int(line[2])

        score_board += f"| {dt} | {line[1]} out of {total_cards} |\n"

    #adds a header/footer bounding box based on the length of the first line
    length = len(score_board.split('\n',1)[0])

    header = "="*length+"\n"
    header += "|"+"Scoreboard".center(length-2)+"|"+"\n"
    header += "-"*length+"\n"

    score_board = header + score_board
    score_board += "="*length

    print(score_board)

def print_card_line(card_line, width=100):
    """Formats the card lines"""
    print("|", end = "")
    print(card_line.center(WIDTH-2), end="")
    print("|")

def print_final_score(score,denom):
    """Prints endgame trophy"""
    #make this a docstring and set to a var. Then run through split lines and itterate over each line to center
    #less good option is to make it a list of strings
    print()
    print("Game Over".center(WIDTH))
    print(".-=========-.".center(WIDTH))
    print("('-=======-')".center(WIDTH))
    print("_|   .=.   |_".center(WIDTH))
    print(f"((|  {score} of {denom} |))".center(WIDTH))
    print("\|   /|\   |/".center(WIDTH))
    print("\__ '`' __/".center(WIDTH))
    print("_`) (`_".center(WIDTH))
    print("_/_______\_".center(WIDTH))
    print("(___________)".center(WIDTH))
    print()

def play(play_cards):
    """Takes the formatted cards and challenges the player"""

    score = 0
    denom = len(play_cards)
    i = 0

    while play_cards:
        
        card = random.choice(play_cards)
        play_cards.remove(card)
        i += 1

        q_lines = textwrap.wrap(card['front'], WIDTH-20)

        print()
        print("=" * WIDTH)
        print_card_line(f"Flashcard {i} of {denom}")
        print_card_line("")
        print_card_line("Hey there Dummy, here's an easy one:")
        
        #prints the textwraped question lines. You probs wont like this. (fix by just altering the card['front'] == +?)
        for x, line in enumerate(q_lines,1):
            if x == 1:
                if x == len(q_lines):
                    print_card_line(f"How do you {line}?")
                    continue
                print_card_line(f"How do you {line}")
                continue
            if x == len(q_lines):
                print_card_line(f"{line}?")
                continue
            print_card_line(line)
        
        print("=" * WIDTH)

        answer = input("\nAnswer: ")

        if answer == card["back"]:
            print("Not as dumb as you look... CORRECT")
            score += 1
            continue
        
        print(f"Whoops. Sorry I was looking for: {card['back']}")
        
    print_final_score(score,denom)

    return score, denom

def main():
    """Takes the users input and either 'plays' a round of flashcards, or displays past scores"""

    while True:

        valid_play = ['play','p']
        valid_scoreboard = ['view','v']

        print()
        choice = input("Would you like to PLAY or VIEW previous scores? ").lower()
        print()

        #starts the flashcard challenge if selected
        if choice in valid_play:
            cards = load_card_csv(CARD_PATH)

            if cards == False:
                print("Error: someth went wrong.")
                return
            
            results = play(cards)
            scorekeeper(LOG_PATH, results[0], results[1])
        
        #displays past scores
        elif choice in valid_scoreboard:
            scores = load_scores(LOG_PATH)
            print_scores(scores)

# main()
menu()