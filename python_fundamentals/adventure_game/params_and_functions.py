
from console.progress import ProgressBar
from console import fg, bg, fx
import textwrap
from random import randint
import math
from rich.text import Text
from rich.style import Style
from rich.console import Console
from rich.padding import Padding

import python_fundamentals.adventure_game.player as player

r_console = Console()

WIDTH = 60
MARGIN = ' '*3
DELAY = 1
DEBUG = True

BAR = ProgressBar(
    total=(player.MAX_HEALTH + .1),
    width=(WIDTH - len("Health") - len("100%")),
    clear_left=False,
)

def debug(message):
    """De debug"""
    if DEBUG:
        r_console.print(f"!!! {message}", style = 'bright_black')
    
def error(message):
    """Prints da error"""
    text = Text.assemble(("Error:", "red"), f" {message}")
    r_console.print(text)

def abort(message):
    """Prints fatal error message and exits the program"""
    error(message)
    exit(1)

def text_style_guide(text):
    """Returns the current global style guide for player visible text"""
    
    # TODO: update all write() to be wrap()?
    # TODO: make this conditional on the player status
    # TODO: address the fact that input text already has some fb color information (there should be a library that can handle that)
        # You kinda accidentally solved this with r_text = Text.from_ansi(text) because the Text object is not being fully utilized/printed
    # TODO: this breaks a loooot of tests, but maybe that doesn't matter given it will only be active periodically
    # TODO: maybe change the eat mushroom text to go rianbow in the middle? (eg swiiiirlllllly)
    # TODO: make sure the effect is actually wearing off. The text seems to stay colorful, but only for some messages?
    # TODO: Finish refactoring to use rich.console (you left off on updating wrap())

    if not isinstance(text, Text):
        text = Text.from_ansi(text)

    if "enlightened" in player.PLAYER.status_effects.keys():

        # create set of indexes with prior styles for exception from rainbowification
        excluded_indexes = set()
        
        for span in text.spans:
            span_style = span.style

            if span_style and span_style.color is not None:
                excluded_indexes.update(range(span.start, span.end))
        
        for i, char in enumerate(text):
            if i in excluded_indexes:
                continue

            r = int(127 * (math.sin(.3 * i + 0) + 1))
            g = int(127 * (math.sin(.3 * i + 2) + 1))
            b = int(127 * (math.sin(.3 * i + 4) + 1))

            rainbow_style = Style(color=f"#{r:02x}{g:02x}{b:02x}")

            text.stylize(rainbow_style, i, i+1)
    
    return text

def wrap(text, width=None, initial_indent=None, subsequent_indent=None, is_image=None):
    width = width or WIDTH
    initial_indent = initial_indent or MARGIN
    subsequent_indent = subsequent_indent or MARGIN

    if isinstance(text, str):
        text = (text,)

    if isinstance(text, Text):
        text = (text,)

    blocks = []

    for i, stanza in enumerate(text):
        # paragraph = textwrap.fill(
        #     stanza,
        #     width,
        #     initial_indent=initial_indent,
        #     subsequent_indent=subsequent_indent
        # )

        # if not isinstance(stanza, Text):
        #     stanza = Text.from_ansi(stanza)

        paragraph = text_style_guide(stanza)

        paragraph = paragraph.wrap(r_console, width=width)

        blocks.append(paragraph)

    if is_image:
        for block in blocks:
            r_console.print(block)
        r_console.print()

        # print(*blocks, sep="\n")
        # print()
    else:
        for i, block in enumerate(blocks):
            if i > 0:
                r_console.print()
            # TODO: this padding is only working for subsequent_indent, and it might not be working at all (eg is_image) 
            r_console.print(Padding(block, (0, 0, 0, len(subsequent_indent))))
        r_console.print()

        # print(*blocks, sep="\n\n")
        # print()
        

def write(text):
    if isinstance(text, Text):
        r_console.print(Text(MARGIN) + text)
        return
    print(MARGIN, text, sep="")

def header(title):
    title2 = Text(f"{title}", style="bold underline cyan")
    write(title2)
    print()

def start_message():
    print()
    print("Welcome to Picnic Quest!")
    print()

    # TODO: delete this after confirming parity
    # wrap((
    #     "You wake to the soft glow of morning light filtering through the cottage's wooden shutters. Today is the day. "\
    #     f"A promise made weeks ago lingers in your mind; your father's secret picnic spot, hidden somewhere in the {fg.lightcyan('misty woods')}.",
    #     "Your heart races with excitement as you swing your legs out of bed, already imagining the sights and sounds of the adventure ahead. "\
    #     f"The floorboards creak beneath your bare feet as you step toward the kitchen, eager to find him. But the {fg.lightcyan('cabin')} is unnervingly still.",
    #     f"His coat and boots are gone. On the rough-hewn writing desk lies an unexpected object: a {fg.lightcyan('folded note')}, weighed down by a stone, with your name scrawled on the front."
    # ))

    wrap((
        Text.assemble(
            "You wake to the soft glow of morning light filtering through the cottage's wooden shutters. Today is the day. ",
            "A promise made weeks ago lingers in your mind; your father's secret picnic spot, hidden somewhere in the ",
            ("misty woods", "bright_cyan"),
            ".",
        ),
        Text.assemble(
            "Your heart races with excitement as you swing your legs out of bed, already imagining the sights and sounds of the adventure ahead. ",
            "The floorboards creak beneath your bare feet as you step toward the kitchen, eager to find him. But the ",
            ("cabin", "bright_cyan"),
            " is unnervingly still.",
        ),
        Text.assemble(
            "His coat and boots are gone. On the rough-hewn writing desk lies an unexpected object: a ",
            ("folded note", "bright_cyan"),
            " weighed down by a stone, with your name scrawled on the front."
        )
    ))

def victory():
    wrap(f"After navigating the woods for hours, the once thick mist begins to retreat and ahead you notice the trees give way to a clearing...")
    wrap(f"By a tree stump and a large basket brimming with food, your father stands, waving warmly.")
    wrap(f"Congratulations! You have completed your task, and enjoy a relaxing picnic with your father.")
    wrap(f"As the sun begins to set, he leads you back to your cabin for the night.")
    player.PLAYER.place = "home"
    
def defeat():
    write(f"Health {BAR(player.PLAYER.current_health)}\n")
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