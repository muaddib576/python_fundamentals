
from console.progress import ProgressBar
from console import fg, bg, fx
import textwrap

from python_fundamentals.adventure_game.player import (
    PLAYER,
    MAX_HEALTH,
)

WIDTH = 60
MARGIN = ' '*3
DELAY = 1
DEBUG = False

BAR = ProgressBar(
    total=(MAX_HEALTH + .1),
    width=(WIDTH - len("Health") - len("100%")),
    clear_left=False,
)

def debug(message):
    """De debug"""
    if DEBUG:
        print(fg.lightblack(f"!!! {message}"))
    
def error(message):
    """Prints da error"""
    print(f"{fg.red('Error:')} {message}")

def abort(message):
    """Prints fatal error message and exits the program"""
    error(message)
    exit(1)

def wrap(text, width=None, initial_indent=None, subsequent_indent=None, is_image=None):
    width = width or WIDTH
    initial_indent = initial_indent or MARGIN
    subsequent_indent = subsequent_indent or MARGIN

    if isinstance(text, str):
        text = (text,)

    blocks = []

    for stanza in text:
        paragraph = textwrap.fill(
            stanza,
            width,
            initial_indent=initial_indent,
            subsequent_indent=subsequent_indent
        )
        
        blocks.append(paragraph)
    
    if is_image:
        print(*blocks, sep="\n")
        print()
    else:
        print(*blocks, sep="\n\n")
        print()

def write(text):
    print(MARGIN, text, sep="")

def header(title):
    title = fx.bold(title)
    title = fx.underline(title)
    title = fg.cyan(title)
    write(title)
    print()

def start_message():
    print()
    print("Welcome to Picnic Quest!")
    print()

    wrap((
        "You wake to the soft glow of morning light filtering through the cottage's wooden shutters. Today is the day. "\
        f"A promise made weeks ago lingers in your mind; your father's secret picnic spot, hidden somewhere in the {fg.lightcyan('misty woods')}.",
        "Your heart races with excitement as you swing your legs out of bed, already imagining the sights and sounds of the adventure ahead. "\
        f"The floorboards creak beneath your bare feet as you step toward the kitchen, eager to find him. But the {fg.lightcyan('cabin')} is unnervingly still.",
        f"His coat and boots are gone. On the rough-hewn writing desk lies an unexpected object: a {fg.lightcyan('folded note')}, weighed down by a stone, with your name scrawled on the front."
    ))

def victory():
    wrap(f"After navigating the woods for hours, the once thick mist begins to retreat and ahead you notice the trees give way to a clearing...")
    wrap(f"By a tree stump and a large basket brimming with food, your father stands, waving warmly.")
    wrap(f"Congratulations! You have completed your task, and enjoy a relaxing picnic with your father.")
    wrap(f"As the sun begins to set, he leads you back to your cabin for the night.")
    PLAYER.place = "home"
    
def defeat():
    write(f"Health {BAR(PLAYER.current_health)}\n")
    wrap(("Your vision fades to black as your strength gives out. The world around you falls silent.",
            "You have succumbed to the trials of this journey.",
    ))
    tombstone = (
            "        _______",
            "      /         \\",
            "     /           \\",
            "    |   R.I.P.    |",
            "    |             |",
            "    |   You have  |",
            "    |   fallen.   |",
            "    |             |",
            "    |_____________|",
            "     \\___________/"
    )
    wrap(tombstone, is_image=True)

    quit()