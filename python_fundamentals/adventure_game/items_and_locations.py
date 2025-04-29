
from console import fg, bg, fx

from python_fundamentals.adventure_game.classes import (
    Place,
    Item,
    Dragon_head,
)

DRAGON_HEADS = Dragon_head.dragon_dict = {
    "red": Dragon_head(
        key="red",
        name="Red Dragon Head",
        description="It's red.",
    ),
    "black": Dragon_head(
        key="black",
        name="Black Dragon Head",
        description="It's black.",
    ),
    "silver": Dragon_head(
        key="silver",
        name="Silver Dragon Head",
        description="It's silver.",
    ),
}

PLACES = Place.place_dict = {
    "home": Place(
        key="home",
        name="Your Cottage",
        description="A cozy stone cottage with a desk and a neatly made bed.",
        east="town-square",
        inventory={'desk':1,
                   'book':1,
                   'bed':1,
                   'water':1,
                   'note':1,
        },
    ),
    "town-square": Place(
        key="town-square",
        name="Town Square",
        description="The square part of town.",
        north="market",
        east="woods",
        west="home",
        inventory={'monument':1,
        },
    ),
    "market": Place(
        key="market",
        name="Yee ol' Market",
        description="A dusty store with rows of shelves overflowing with what appears to be junk. "\
            "A large wooden sign hangs above the old shopkeeper.",
        south="town-square",
        can=['shop'],
        shop_inventory={'potion':5,
                   'dagger':1,
                   'map':1,
        },
    ),
    "woods": Place(
        key="woods",
        name="The Woods",
        description="Significantly more trees than the Town. You hear bird's chirping above and the crunch of foliage under your feet",
        east="hill",
        south="misty-woods",
        west="town-square",
        inventory={'mushroom':3,
        }
    ),
    "misty-woods": Place(
        key="misty-woods",
        name="The Misty Woods",
        description="A thick mist envelops the trees. You already feel lost just looking at it.",
        north='misty-woods',
        south='misty-woods',
        east='misty-woods',
        west='misty-woods',
        egress_location='woods',
        misty_path = ['s','w','s','e','s'],
        current_path=[],
        misty_descriptions=["The trees stretch as far as you can see... is the mist getting thicker?",
                           "The mist is definitely thicker. And was it always this quiet?",
                           "This eerie silence is almost more oppressive than the ever thickening mists...",
                           "...almost. You can barely make out your hand through the swirling grey patterns.",
        ],
    ),
    "hill": Place(
        key="hill",
        name="Grassy hill",
        description="The trees have given way to an expansive hill covered in rustling grass which seems to all be burnt on the southern facing side.",
        west="woods",
        south="cave",
    ),
    "cave": Place(
        key="cave",
        name="Foreboding Cave",
        description="A big ol' cave entrance.",
        north="hill",
        can=['pet'],
        inventory={'dragon':1,
        },
    ),
}

ITEMS = Item.item_dict = {
    "potion": Item(
        key="potion",
        name="healing potion",
        aliases=["health potion",
                 "red potion",
                 "health bottle",
        ],
        description="A magical liquid that improves your life's outlook.",
        can_take = True,
        price=-10,
        drink_message=(
            "You uncork the bottle.",
            "The swirling green liquid starts to bubble.",
            "You hesitatingly bring the bottle to your lips...",
            "then quickly down the whole thing!",
            "Surprisingly, it tastes like blueberries.",
            "You feel an odd tingling sensation starting at the top of your head... ",
            "...moving down your body...",
            "...down to the tips of your toes.",
        ),
        health_change=20
    ),
    "water": Item(
        key="water",
        name="bottle of water",
        aliases=["waterbottle",
                 "water bottle",
                 "bottle",
        ],
        description="A bottle what has water in it.",
        can_take = True,
        drink_message=(
            "You pull the cork from the waxed leather bottle.",
            "You take a deep drink of the cool liquid.",
            "You feel refreshed.",
        ),
        health_change=5
    ),
    "mushroom": Item(
        key="mushroom",
        name="a red mushroom",
        aliases=["shroom",
                 "red mushroom"
        ],
        description="A red mushroom with white spots.",
        can_take = True,
        eat_message=(
            "You shove the whole mushroom in your mouth...",
            "Things start to look swirllllly...",
            "Your tummy doesn't feel so good.",
        ),
        health_change=-15
    ),
    "lockpicks": Item(
        key="lockpicks",
        name="lockpicking tools",
        description="A standard thieving kit.",
        can_take = True,
        price=-8,
    ),
    "dagger": Item(
        key="dagger",
        name="stabbing dagger",
        description="A length of metal honed to a fine point.",
        can_take = True,
        price=-20,
    ),
    "desk": Item(
        key="desk",
        name="a writing desk",
        description="A wooden desk with a large leather-bound book open on its surface.",
    ),
    "note": Item(
        key="note",
        name="note from father",
        aliases=["folded note",
                 "letter",
        ],
        description="A folded note from your father. It's addressed to you.",
        writing={'title':"The tri-folded paper reads:",
                 'message': ("My child,",
                             
                             "I know I promised to take you to the secret spot today. But that was a lie. "
                             "Sometimes, the best adventures are the ones we make for ourselves. I want you to find your own way there.",

                             "The mists are not malicious but they are mischievous, and if you don't already know your way they will surely spin you in circles. "
                             
                             "Even I did not find my way here on my own. The town's old shopkeeper might be willing to help you out... for a price.",

                             "I will be waiting for you with our lunch.",

                             f"P.S. Those who are lost can find inspiration when they {fg.lightyellow('examine')} the great hero's monument."
                 )
        },
        can_take = True,
    ),
    "book": Item(
        key="book",
        name="a book",
        aliases=["leather book",
                 "leather-bound book",
                 "leatherbound book",
        ],
        description="A hefty leather-bound tome open to an interesting passage.",
        writing={'title':"The book is open to a page that reads:",
                 'message': ("In the shadow of the eastern cliffs, the Dragon's Lair holds treasures untold.",
                             
                             "But beware: the guardian of gold is both fierce and fond of affection.",
                             
                             "Approach not with weapons drawn, but with a kind hand, for rumors hold the beast delights in the simplest of pleasures... "
                             "a gentle pet atop its mighty head.",
                 )
        },
        can_take = True,
    ),
    "monument": Item(
        key="monument",
        name="large monument",
        aliases=["statue",
                 "plaque",
        ],
        description=f"A large stone monument with a {fg.lightyellow('read')}-able plaque.",
        writing={'title':"The plaque looks recently polished and reads:",
                 'message': (f"{fg.lightyellow('Look')} upon the legend of The Lopen, whose deeds still light our paths! In his quest, he would {fg.lightyellow('shop')} at the bustling market and {fg.lightyellow('go')} boldly into the unknown.",
                             f"Ever curious, he did {fg.lightyellow('examine')} every hidden secret and bravely {fg.lightyellow('take')} on challenges, keeping a keen {fg.lightyellow('inventory')} of his victories.",
                             f"When peril arose, he would {fg.lightyellow('drop')} all holding him back, then {fg.lightyellow('buy')} the wisdom of ancient masters and {fg.lightyellow('read')} the fabled scrolls of yore.",
                             f"In moments of gentle repose, he would {fg.lightyellow('pet')} his steadfast companion, Sparky, before he would {fg.lightyellow('eat')} the feast of triumph and {fg.lightyellow('drink')} deeply from the wellspring of hope.",
                             f"Let these words be your guide, brave traveler, as you follow in his heroic footsteps.",
                 )
        },
        can_take = False,
    ),
    "map": Item(
        key="map",
        name="Map of the Misty Woods",
        aliases=["misty map",
                 "map of woods"
        ],
        description="A tattered parchment depicting an area thick with trees and mist. You can just make out what appears to be a winding path through the madness.",
        writing={'title':"The Misty Woods",
                 'image': (
                             "┌---------------------   ---------------------┐",
                             "| ♣  ~  ♣  ♣  ♣  ♣  ~ |↓| ♣  ♣  ♣  ♣  ~  ♣  ♣ |",
                             "| ♣  ~  ♣  ♣  ~  ♣  ~ | | ~  ♣  ~  ♣  ♣  ♣  ♣ |",
                             "| ♣  ♣  ~  ♣  ~  ♣  ♣ | | ♣  ♣  ♣  ~  ♣  ♣  ~ |",
                             "| ♣  ♣  ~  _ _♣ _♣ _♣_| | ♣  ♣  ♣  ~  ♣  ♣  ~ |",
                             "| ♣  ♣  ♣ |↓  _ _ _ _ _←| ♣  ~  ♣  ~  ♣  ♣  ♣ |",
                             "| ♣  ♣  ♣ | |_♣_ ~  ♣  ♣  ♣  ♣  ~  ♣  ♣  ♣  ♣ |",
                             "| ♣  ♣  ♣ |→_ _  ↓| ~  ♣  ~  ♣  ♣  ♣  ~  ♣  ♣ |",
                             "| ♣  ♣  ♣  ♣  ♣ | | ♣  ~  ♣  ~  ♣  ♣  ♣  ♣  ~ |",
                             "| ♣  ♣  ♣  ~  ♣|   |♣  ♣  ~  ♣  ♣  ~  ♣  ♣  ♣ |",
                             "| ♣  ♣  ♣  ♣  ♣|_x_|♣  ♣  ~  ♣  ♣  ♣  ~  ♣  ~ |",
                             "| ♣  ♣  ♣  ♣  ~  ♣  ♣  ♣  ♣  ♣  ~  ♣  ♣  N  ♣ |",
                             "| ♣  ♣  ~  ♣  ♣  ♣  ♣  ♣  ♣  ♣  ♣  ~  W  ♣  E |",
                             "| ♣  ♣  ♣  ♣  ♣  ~  ♣  ♣  ♣  ♣  ♣  ♣  ~  S  ~ |",
                             "└---------------------------------------------┘",
                 )
        },
        price=-50,
        can_take = True,
    ),
    "bed": Item(
        key="bed",
        name="your bed",
        description="Some cloth stuffed with hay. Hardly any bugs.",
    ),
    "gems": Item(
        key="gems",
        name="gems",
        description="The realm's primary currency. They also look pretty.",
        can_take = True,
    ),
    "dragon": Item(
        key="dragon",
        name="dragon",
        description= (f"A large dragon with heads of {', '.join(list(Dragon_head.dragon_dict.keys())[0:-1])}, " \
                      f"and {list(Dragon_head.dragon_dict.keys())[-1]}."
        )
    ),
}