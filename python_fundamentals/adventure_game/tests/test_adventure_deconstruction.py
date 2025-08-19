import pytest
import importlib

import python_fundamentals.adventure_game.items_and_locations as items_and_locations
import python_fundamentals.adventure_game.params_and_functions as params_and_functions
import python_fundamentals.adventure_game.player as player

import python_fundamentals.adventure_game.classes as classes
# redundant import needed to set DELAY = 0 for the tests

from python_fundamentals.adventure_game.params_and_functions import (
    error,
    abort,
    debug,
    header,
    write,
    wrap,
)

from python_fundamentals.adventure_game.classes import (
    Command,
    Place,
    Item,
    Dragon_head,
    InvalidItemError,
    InvalidPlaceError,   
)

from python_fundamentals.adventure_game.commands import (
    Go,
    Examine,
    Look,
    Take,
    Inventory,
    Drop,
    Shop,
    Buy,
    Read,
    Pet,
    Consume,
    Eat,
    Drink,
    Quit
)

from python_fundamentals.adventure_game.main import (
    gen_action_dict,
)


@pytest.fixture(autouse=True)
def setup():
    breakpoint()
    importlib.reload(items_and_locations)
    breakpoint()
    importlib.reload(params_and_functions)
    importlib.reload(player)
    
    # params_and_functions.DELAY = 0
    classes.DELAY = 0
    # TODO this solves the delay test issue, but I don't like that I am importing python_fundamentals.adventure_game.classes twice
    # Maybe it's best not to care about this, as it only affects the test file...

    yield

def test_action_keys():
    # GIVEN: the full action_dict
    action_dict_test = gen_action_dict()
    actual_commands = set(action_dict_test.values())

    # AND: expected keys
    expected_commands = {Quit,
                         Look,
                         Shop,
                         Go,
                         Examine,
                         Take,
                         Inventory,
                         Drop,
                         Buy,
                         Read,
                         Pet,
                         Eat,
                         Drink,
    }

    # THEN: All the expected commands should be there?
    assert expected_commands.issubset(actual_commands), \
        "The constructed list should contain the player accessible Commands"

def test_collectable_get():
    # GIVEN: An item
    Item.item_dict = {}
    Item.item_dict['cup'] = Item(
        key="cup",
        name="cup",
        description="You can drink from it.",
    )
    
    # WHEN: get class method is called on the key
    item = Item.get('cup')

    # THEN: the item object is returned
    assert item.key == 'cup'

def test_collectable_get_missing():
    # GIVEN: An item dict
    Item.item_dict = {}

    # WHEN: get() class method is called on an key that is not present
    with pytest.raises(Exception) as info:
        Item.get('cup')

    # THEN: An exception is raised for the player
    exception = info.value
    assert "This is embarrassing" in str(exception)

def test_collectable_find_name():
    # GIVEN: an item
    Item.item_dict = {
        "fake": Item(
            key="fake",
            name="fake alias",
            description="It's fake.",
        ),
        "grass": Item(
            key="grass",
            name="unrelated alias",
            description="It's grass.",
        )
    }
    # WHEN: the find method is called using either the name or the key
    item = Item.find('unrelated alias')

    # THEN: the item is returned
    assert item.key == 'grass', \
        "The find method should return the Item object when passed the item.name"

def test_collectable_find_key():
    # GIVEN: an item
    Item.item_dict = {
        "fake": Item(
            key="fake",
            name="fake alias",
            description="It's fake.",
        ),
        "grass": Item(
            key="grass",
            name="unrelated alias",
            description="It's grass.",
        )
    }
    # WHEN: the find method is called using either the name or the key
    item = Item.find('fake')

    # THEN: the item is returned
    assert item.name == 'fake alias', \
        "The find method should return the Item object when passed the item.key"

def test_collectable_find_name_plural_s():
    # GIVEN: an item
    Item.item_dict = {
        "potion": Item(
            key="potion",
            name="a healing potion",
            description="It's fake.",
        ),
        "grass": Item(
            key="grass",
            name="unrelated alias",
            description="It's grass.",
        )
    }
    # WHEN: the find method is called using either the name or the key with a plural 's'
    item = Item.find('potions')

    # THEN: the item is returned
    assert item.key == 'potion', \
        "The find method should return the Item object when passed a key pluralized with a single 's'"

def test_collectable_find_name_s_not_plural():
    # GIVEN: an item
    Item.item_dict = {
        "potion": Item(
            key="potion",
            name="a healing potion",
            description="It's fake.",
        ),
        "grass": Item(
            key="grass",
            name="unrelated alias",
            description="It's grass.",
        )
    }
    # WHEN: the find method is called using either the name or the key with a plural 's'
    item = Item.find('grass')

    # THEN: the item is returned
    assert item.key == 'grass', \
        "The find method should return the Item object when passed a key with an s for non plural"

def test_collectable_find_name_plural_dict():
    # GIVEN: an item
    Item.item_dict = {
        "potion": Item(
            key="potion",
            name="a healing potion",
            description="It's fake.",
        ),
        "octopus": Item(
            key="octopus",
            name="a live octopus",
            description="It's grEIGHT.",
            aliases=['octopuses','octopi']
        )
    }
    # WHEN: the find method is called using either the aliases
    item = Item.find('octopuses')
    item2 = Item.find('octopi')

    # THEN: the item is returned
    assert item.key == 'octopus', \
        "The find method should return the Item object when passed a key equal to any aliases"
    assert item2.key == 'octopus', \
        "The find method should return the Item object when passed a key equal to any aliases"

def test_do_nothing():
    pass

def test_collectable_find_name_examine(capsys: pytest.CaptureFixture[str]):
    # GIVEN: an item
    # breakpoint()
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {'grass':1}
    Place.place_dict = {
        "shire": Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={}
        )
    }
    Item.item_dict = {
        "grass": Item(
            key="grass",
            name="unrelated alias",
            description="It's grass.",
        )
    }

    # WHEN: the find method is called using either the name via the Examine class command
    # item = Item.find('unrelated alias')
    # breakpoint()
    Examine(['unrelated alias']).do()
    output = capsys.readouterr().out

    # THEN: the item is returned
    assert "It's grass." in output, \
        "The find method should return the Item object when passed the item.name"

@pytest.mark.skip(reason="method to be deleted")
def test_towards():
    # GIVEN: Two linked locations

    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            east="mordor"
        )
    Place.place_dict["mordor"] = Place(
            key="mordor",
            name="Mordor",
            description="Buncha orcs.",
            west="shire"
        )


    # WHEN: One is passed a direction
    place = Place.place_dict["mordor"]

    # place.get("xxx")
    # Place.get("mordor")

    destination = place.towards('west')

    # THEN: The linked location is returned
    assert destination == 'shire'

def test_teardown():
    """Test that item key added in previous test does not persist"""
    assert "shire" not in Place.place_dict, \
        """Each test should have a fresh data set"""

def test_error(capsys: pytest.CaptureFixture[str]):
    error("error test")
    output = capsys.readouterr().out
    
    assert output == "Error: error test\n"

def test_abort():
    with pytest.raises(SystemExit):
        abort("abort test")

def test_debug(capsys: pytest.CaptureFixture[str]):
    debug("debug test")
    output = capsys.readouterr().out

    assert output == f"!!! debug test\n"

def test_header(capsys: pytest.CaptureFixture[str]):
    header("header test")
    output = capsys.readouterr().out

    assert output == f"{params_and_functions.MARGIN}header test\n\n"

def test_write(capsys: pytest.CaptureFixture[str]):
    write("write test")
    output = capsys.readouterr().out

    assert output == f"{params_and_functions.MARGIN}write test\n"

def test_wrap(capsys: pytest.CaptureFixture[str]):
    # GIVEN: The default WIDTH and MARGIN
    params_and_functions.WIDTH = 10
    params_and_functions.MARGIN = ' '*3

    # WHEN: the wrap function is called
    test_string = '*' * 14
    wrap(test_string)
    output = capsys.readouterr().out

    # THEN: the default WIDTH and MARGIN are used
    assert output == f"{params_and_functions.MARGIN}*******\n{params_and_functions.MARGIN}*******\n\n"

def test_wrap_custom(capsys: pytest.CaptureFixture[str]):
    # WHEN: the wrap function is passed custom width and margin values
    test_string = '*' * 11
    width = 10
    initial_indent = ' '*4
    subsequent_indent = ' '*5

    wrap(test_string, width, initial_indent, subsequent_indent)
    output = capsys.readouterr().out

    # THEN: the specified indent values are used
    assert output == f"{initial_indent}******\n{subsequent_indent}*****\n\n"

@pytest.mark.parametrize(
        ['start','amount','expected','message'], [
        (10, 1, 11, ""),
        (10, 10, 20, ""),
        (10, 11, 21, ""),
        (10, 15, 25, ""),
])
def test_add(start, amount, expected, message):
    # GIVEN: the player's initial gems
    player.PLAYER.inventory = {'gems':start}

    # WHEN: the add method is called
    player.PLAYER.add('gems', amount)
    
    # THEN: the player's health should be changed by the # passed to health_change
    assert player.PLAYER.inventory['gems'] == expected, message

def test_go(capsys: pytest.CaptureFixture[str]):
    player.PLAYER.place = 'shire'
    Place.place_dict = {
        "shire": Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={},
            east='moria'
        ),
        "moria": Place(
            key="moria",
            name="The Mines of Moria",
            description="Buncha drawf skellies.",
            inventory={},
            west='shire'
        )
    }

    Go(['east']).do()
    output = capsys.readouterr().out

    assert player.PLAYER.place == 'moria', \
        "Player should be moved to the direction they specified"
    assert "Buncha drawf skellies" in output, \
        "Player should be told their new location's description"

def test_go_no_place(capsys: pytest.CaptureFixture[str]):
    player.PLAYER.place = 'shire'
    Place.place_dict = {
        "shire": Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={},
            east='moria'
        ),
    }

    Go(['west']).do()
    output = capsys.readouterr().out

    assert player.PLAYER.place == 'shire', \
        "Player's location should not change when there is nothing in the specified direction"
    assert "Sorry, there is no 'west'" in output, \
        "Player should be told there is nothing in that direction"

def test_go_misty_bad_direction(capsys: pytest.CaptureFixture[str]):
    player.PLAYER.place = 'misty-woods'
    Place.place_dict = {
        "shire": Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={},
            south='misty-woods'
        ),
        "misty-woods": Place(
            key="misty-woods",
            name="The Misty Woods",
            description="Buncha misty hobbits.",
            misty_descriptions=["Buncha misty hobbits 1",
                                "Buncha misty hobbits 2",
                                "Buncha misty hobbits 3",
                                "Buncha misty hobbits 4",
            ],
            inventory={},
            north='misty-woods',
            south='misty-woods',
            east='misty-woods',
            west='misty-woods',
            egress_location='shire',
            misty_path = ['s','w','s','e','s'],
            current_path = ['s','s']
        ),
    }

    Go(['tohell']).do()
    output = capsys.readouterr().out

    assert Place.place_dict["misty-woods"].current_path == ['s','s'], \
        "A invalid direction should not add to the current path"
    assert "Sorry, there is no 'tohell'" in output, \
        "Player should be told the typed direction does not exist."

def test_go_misty_mid_sequence(capsys: pytest.CaptureFixture[str]):
    player.PLAYER.place = 'misty-woods'
    Place.place_dict = {
        "shire": Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={},
            south='misty-woods'
        ),
        "misty-woods": Place(
            key="misty-woods",
            name="The Misty Woods",
            description="Buncha misty hobbits.",
            misty_descriptions=["Buncha misty hobbits 1",
                                "Buncha misty hobbits 2",
                                "Buncha misty hobbits 3",
                                "Buncha misty hobbits 4",
            ],
            inventory={},
            north='misty-woods',
            south='misty-woods',
            east='misty-woods',
            west='misty-woods',
            egress_location='shire',
            misty_path = ['s','w','s','e','s'],
            current_path = ['s','s']
        ),
    }

    Go(['west']).do()
    output = capsys.readouterr().out

    assert player.PLAYER.place == 'misty-woods', \
        "After 3 moves in the mist, the player should still be in the mist."
    assert Place.place_dict["misty-woods"].current_path == ['s','s','w'], \
        "Each move the player makes should be added to the current_path history"
    assert "Buncha misty hobbits 3" in output, \
        "Player should be told the same location's 3rd misty description"

def test_go_misty_timeout(capsys: pytest.CaptureFixture[str]):
    player.PLAYER.place = 'misty-woods'
    Place.place_dict = {
        "shire": Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={},
            south='misty-woods'
        ),
        "misty-woods": Place(
            key="misty-woods",
            name="The Misty Woods",
            description="Buncha misty hobbits.",
            inventory={},
            north='misty-woods',
            south='misty-woods',
            east='misty-woods',
            west='misty-woods',
            egress_location='shire',
            misty_path = ['s','w','s','e','s'],
            current_path = ['s','w','s','e'],
        ),
    }

    Go(['west']).do()
    output = capsys.readouterr().out

    assert player.PLAYER.place == 'shire', \
        "After 5 moves in the mist, without the correct sequence, the player should get kicked out to the egress location"
    assert Place.place_dict["misty-woods"].current_path == [], \
        "AAfter 5 moves in the mist, without the correct sequence, the current_path history should be reset"
    assert "After wondering in circles for hours," in output, \
        "The Player is told they went in a big circle."
    assert "Buncha hobbits." in output, \
        "Player should be told their new location's description"
    
def test_go_misty_clearing(capsys: pytest.CaptureFixture[str]):
    player.PLAYER.place = 'misty-woods'
    Place.place_dict = {
        "misty-woods": Place(
            key="misty-woods",
            name="The Misty Woods",
            description="Buncha misty hobbits.",
            inventory={},
            north='misty-woods',
            south='misty-woods',
            east='misty-woods',
            west='misty-woods',
            egress_location='shire',
            misty_path = ['s','w','s','e','s'],
            current_path = ['s','w','s','e'],
        ),
    }

    Go(['south']).do()
    output = capsys.readouterr().out

    assert "Congratulations! You have completed your task," in output, \
        "The Player is told they won the game."

def test_examine_no_arg(capsys: pytest.CaptureFixture[str]):
    Examine([]).do()
    output = capsys.readouterr().out

    assert "Error: You cannot examine nothing.\n" in output, \
        "Passing no argument should throw an error"

def test_examine_missing_from_place_and_player_inv(capsys: pytest.CaptureFixture[str]):
    # GIVEN: That the item the player wants to examine is not in the current
    #        place, and not in the player's inventory
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {}
    Place.place_dict = {
        "shire": Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={}
        )
    }
    Item.item_dict = {
        "grass": Item(
            key="grass",
            name="grass blades",
            description="It's grass.",
            price=-10,
        )
    }
    
    # WHEN: The player tries to examine it
    Examine(['grass']).do()
    output = capsys.readouterr().out

    # THEN: The player should be told they can't
    assert "Error: There is no grass in the shire." in output, \
        "An Examine target not in the current location or player inventory should throw an error"

def test_examine_missing_from_place(capsys: pytest.CaptureFixture[str]):
    # GIVEN: That the item the player wants to examine is not in the current
    #        place, but is in the player's inventory
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {'grass':1}
    Place.place_dict = {
        "shire": Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={}
        )
    }
    Item.item_dict = {
        "grass": Item(
            key="grass",
            name="grass blades",
            description="It's grass.",
            price=-10,
        )
    }

    # WHEN: The player examines that item
    Examine(['grass']).do()
    output = capsys.readouterr().out

    # THEN: The player should be told the description of the item.
    assert "It's grass." in output, \
        "A valid Examine target should print the item description."

def test_examine_missing_from_player_inv(capsys: pytest.CaptureFixture[str]):
    # GIVEN: That the item the player wants to examine is not in the player's inventorty
    #        but is in the current place
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {}
    Place.place_dict = {
        "shire": Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={'grass':1,'hills':1}
        )
    }
    Item.item_dict = {
        "grass": Item(
            key="grass",
            name="grass blades",
            description="It's grass.",
            price=-10,
            health_change=-7
        )
    }

    # WHEN: The player examines that item
    Examine(['grass']).do()
    output = capsys.readouterr().out

    # THEN: The player should be told the description of the item and the health impact (if any)
    assert "It's grass." in output, \
        "A valid Examine target should print the item description."
    
    assert "-7 health" in output, \
        "The player should be told the health impact for an examined item."

def test_examine_missing_item(capsys: pytest.CaptureFixture[str]):
    player.PLAYER.place = 'shire'
    Place.place_dict = {
        "shire": Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={'grass':1,'hills':1}
        )
    }
    Item.item_dict = {}

    Examine(['hills']).do()
    output = capsys.readouterr().out

    assert 'There is no hills in' in output, \
        "If a key is not preset in ITEMS, the player should be told it is not at the location."

def test_examine_in_shop(capsys: pytest.CaptureFixture[str]):
    # GIVEN: That the item the player wants to examine is not in the player's inventorty
    #        but is in the current place, and the current place is a shop
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {}
    Place.place_dict = {
        "shire": Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            shop_inventory={'grass':3,'hills':1},
            can=['shop']
        )
    }
    Item.item_dict = {
        "grass": Item(
            key="grass",
            name="grass blades",
            description="It's grass.",
            price=-10,
            health_change=7
        )
    }

    # WHEN: The player examines that item
    Examine(['grass']).do()
    output = capsys.readouterr().out

    # THEN: The player should be told the description of the item and its price.
    assert "It's grass." in output, \
        "An Examine target should print the item description."
    
    assert "The shop has 3, you can buy one for 10 gems." in output, \
        "If the location can shop, the quantity/price should be printed."
    
    assert "+7 health" in output, \
        "The player should be told the health impact for an examined item."

def test_get_place_start(capsys: pytest.CaptureFixture[str]):
    assert Command([]).player_place == Place.place_dict[player.PLAYER.place], \
        "Starting location should be 'your cottage'"
    
def test_get_place_missing_place(capsys: pytest.CaptureFixture[str]):
    player.PLAYER.place = 'shire'
    Place.place_dict = {}

    with pytest.raises(InvalidPlaceError) as info:
        Command([]).player_place

def test_comma_list_3():
    # GIVEN: a list of 3 or more elements
    test_list = ['1','2','3']
    # WHEN: the list is passed to the comma_list() method
    test_string = Command([]).comma_list(test_list)
    # THEN: a comma seperated string is returned
    assert test_string == "1, 2, and 3", " A list of three should be comma seperated"

def test_comma_list_2():
    # GIVEN: a list of 2 elements
    test_list = ['1','2']
    # WHEN: the list is passed to the comma_list() method
    test_string = Command([]).comma_list(test_list)
    # THEN: a string with both elements seperated by an 'and' is returned
    assert test_string == "1 and 2", "A list of 2 should be and seperated"

def test_comma_list_1():
    # GIVEN: a list of 1 element
    test_list = ['1']
    # WHEN: the list is passed to the comma_list() method
    test_string = Command([]).comma_list(test_list)
    # THEN: a string with that element is returned
    assert test_string == "1", "A list of one should return itself"

def test_comma_list_0():
    # GIVEN: a list of 0 elements
    test_list = []
    # WHEN: the list is passed to the comma_list() method
    test_string = Command([]).comma_list(test_list)
    # THEN: an error is returned
    assert test_string == "", "A list of nothing should return an empty string"

def test_look_place(capsys: pytest.CaptureFixture[str]):
    
    # GIVEN: The player's current location
    player.PLAYER.place = 'shire'
    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
        )

    # WHEN: The player activates Look
    Look([]).do()
    output = capsys.readouterr().out

    # THEN: The player is told the description of the current location
    assert "Buncha hobbits" in output, "The description of the current location should print"

def test_look_items(capsys: pytest.CaptureFixture[str]):
    
    # GIVEN: The player's current location
    player.PLAYER.place = 'shire'
    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={'grass':1}
        )

    Item.item_dict = {
        "grass": Item(
            key="grass",
            name="grass blades",
            description="It's grass.",
            price=-10,
        )
    }

    # WHEN: The player activates Look
    Look([]).do()
    output = capsys.readouterr().out

    # THEN: The player is told the list of items present in the location
    assert "grass blades" in output, "The names of the items in the current locations should print"

def test_look_items_w_shop(capsys: pytest.CaptureFixture[str]):
    
    # GIVEN: The player's current location
    player.PLAYER.place = 'shire'
    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={'grass':1},
            shop_inventory={'horse':1},
        )

    Item.item_dict = {
        "grass": Item(
            key="grass",
            name="grass blades",
            description="It's grass.",
            price=-10,
        ),
        "horse": Item(
            key="horse",
            name="Poo Brained Horse",
            description="It looks like a normal horse.",
            price=-20,
        ),
    }

    # WHEN: The player activates Look
    Look([]).do()
    output = capsys.readouterr().out

    # THEN: The player is told the list of items present in the location
    assert "grass blades" in output, "The names of the items in the location's inventory should print"
    assert "Poo Brained Horse" in output, "The names of the items in the location's shop_inventory should print"

def test_look_no_items(capsys: pytest.CaptureFixture[str]):
    
    # GIVEN: The player's current location
    player.PLAYER.place = 'shire'
    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
        )

    # WHEN: The player activates Look
    Look([]).do()
    output = capsys.readouterr().out

    # THEN: The player is told the list of items present in the location
    assert "You see" not in output, "If there are no items in the location, you can't see anything"

def test_look_nearby(capsys: pytest.CaptureFixture[str]):
    
    # GIVEN: The player's current location
    player.PLAYER.place = 'shire'
    Place.place_dict = {
        "shire": Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            east="mordor",
            west="sea",
        ),
        "mordor": Place(
            key="mordor",
            name="Mordor",
            description="Buncha orcs.",
            west="shire",
        ),
        "sea": Place(
            key="sea",
            name="The Sea",
            description="Buncha water.",
            east="shire",
        )
    }

    # WHEN: The player activates Look
    Look([]).do()
    output = capsys.readouterr().out

    # THEN: The player is told the list of nearby places
    assert "Mordor" in output, "The names of the nearby locations should print"
    assert "The Sea" in output, "The names of the nearby locations should print"

def test_look_no_nearby(capsys: pytest.CaptureFixture[str]):
    
    # GIVEN: The player's current location
    player.PLAYER.place = 'shire'
    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
        )

    # WHEN: The player activates Look
    Look([]).do()
    output = capsys.readouterr().out

    # THEN: The player is told the list of nearby places
    assert "To the" not in output, "If there is nothing nearby, the names of the nearby locations should not print"

def test_take_valid_item(capsys: pytest.CaptureFixture[str]):
    
    # GIVEN: The player's current location and a valid item
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {}
    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={'grass':1}
        )

    Item.item_dict = {
        "grass": Item(
            key="grass",
            name="grass blades",
            description="It's grass.",
            can_take=True,
            price=-10,
        )
    }

    # WHEN: The player tries to take a valid item
    Take(['grass']).do()
    output = capsys.readouterr().out

    # THEN: The player aquires the item
    assert 'grass' in player.PLAYER.inventory, "The tooken item should be in the player's inventory"

    # AND: the item is removed from the place
    assert 'grass' not in Place.place_dict["shire"].inventory, "the tooken item should no longer be at the place"

    # AND: the player is informed
    assert "You pick up" in output, "The player should be told they have aquired the item"

def test_take_missing_item(capsys: pytest.CaptureFixture[str]):
    # GIVEN: The player's current location and an item that is not present
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {}
    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={}
        )

    # WHEN: The player tries to take the item
    Take(['grass']).do()
    output = capsys.readouterr().out

    # THEN: The player is told the item is not present
    assert "There is no grass in" in output, "The player should be told the desired item is not present"

    # AND: gets nothing
    assert 'grass' not in player.PLAYER.inventory, "The desired item should not be in the player's inventory"

def test_raises_example():
    """Example of using pytest.raises to check for an exception.
    https://docs.pytest.org/en/6.2.x/assert.html
    https://docs.pytest.org/en/6.2.x/reference.html#pytest.raises
    """
    with pytest.raises(TypeError):
        raise TypeError()

    with pytest.raises(TypeError) as info:
        raise TypeError("Something went wrong!")

    exception = info.value
    assert "wrong" in str(exception)

def test_take_untakable_item(capsys: pytest.CaptureFixture[str]):
    # GIVEN: The player's current location and an untakable item
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {}
    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={'grass':1}
        )

    Item.item_dict = {
        "grass": Item(
            key="grass",
            name="grass blades",
            description="It's grass.",
            can_take=False,
            price=-10,
        )
    }

    # WHEN: The player tries to take the item
    Take(['grass']).do()
    output = capsys.readouterr().out

    # THEN: The player is told the item does not move
    assert "but it doesn't budge" in output, "The player should be told the item info is missing"    

    # AND: gets nothing
    assert 'grass' not in player.PLAYER.inventory, "The desired item should not be put in the player's inventory"

    # AND: the item is not removed from the location
    assert 'grass' in Place.place_dict["shire"].inventory, "the desired item should remain at the place"

def test_take_quantity_one(capsys: pytest.CaptureFixture[str]):
    # GIVEN: The current location with items present and player's inventory
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {}
    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={'ring': 1}
    ) 
    Item.item_dict = {
        "ring": Item(
            key="ring",
            name="ring",
            description="A metal circle.",
            can_take=True,
        )
    }

    # WHEN: The player tries to take an item from the place
    Take(['ring', 1]).do()
    output = capsys.readouterr().out
    
    # THEN: The item is removed from the current location's inventory
    assert 'ring' not in Place.place_dict["shire"].inventory, \
        "the tooken item should be removed from the current location inventory"

    # AND: The item is added to the player's inventory
    assert 'ring' in player.PLAYER.inventory, \
        "The tooken item should be added to player's inventory"

    # AND: The player is informed
    assert "You pick up 1 ring and put it in your bag." in output, \
        "The player should be told they picked up the item"

def test_take_qty(capsys: pytest.CaptureFixture[str]):
    # GIVEN: The current location and the items in the player's inventory
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {}
    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={'ring':10}
    )  
    Item.item_dict = {
        "ring": Item(
            key="ring",
            name="ring",
            description="A metal circle.",
            can_take=True,
        )
    }

    # WHEN: The player tries to take an item
    Take(['ring', 3]).do()
    output = capsys.readouterr().out

    # THEN: The item is removed from the current location's inventory
    assert Place.place_dict["shire"].inventory['ring'] == 7, \
        "the tooken item quantity should be decreased by 3 in the location's inventory"

    # AND: The item is added from the players inventory
    assert player.PLAYER.inventory['ring'] == 3, \
        "The tooken item quantity should be increased by 3 in player's inventory"

    # AND: The player is informed
    assert "You pick up 3 ring and put it in your bag." in output, \
        "The player should be told they took the item"

def test_take_invalid_qty(capsys: pytest.CaptureFixture[str]):
    # GIVEN: The current location and the items in the player's inventory
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {}
    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={'ring':3}
    )  
    Item.item_dict = {
        "ring": Item(
            key="ring",
            name="ring",
            description="A metal circle.",
            can_take=True,
        )
    }

    # WHEN: The player tries to take an invalid qty an item
    Take(['ring', 4]).do()
    output = capsys.readouterr().out

    # THEN: The item is not removed from the current location's inventory
    assert Place.place_dict["shire"].inventory['ring'] == 3, \
        "the tooken item quantity should be decreased by 3 in the location's inventory"

    # AND: The item is not added from the players inventory
    assert "ring" not in player.PLAYER.inventory.keys(), \
        "The invalid qty item should not be added to the player's inventory"

    # AND: The player is informed
    assert "Sorry, there are not 4 ring available to take here" in output, \
        "The player should be told there are not enough"

def test_inventory(capsys: pytest.CaptureFixture[str]):
    # GIVEN: Items in the player inventory
    player.PLAYER.inventory = {'lockpicks':1, 'knife':2}
    Item.item_dict = {
        "lockpicks": Item(
            key="lockpicks",
            name="lockpicking tools",
            description="A standard theiving kit.",
        ),
        "knife": Item(
            key="knife",
            name="blunt knife",
            description="An old knife.",
        )
    }

    # WHEN: The inventory is checked
    Inventory([]).do()
    output = capsys.readouterr().out

    # THEN: The inventory contents are displayed
    assert '(x 1) lockpicking tools' in output, "The player should be told the items their inventory"

    # AND: The inventory contents are displayed
    assert '(x 2) blunt knife' in output, "The player should be told the items their inventory"

def test_inventory_empty(capsys: pytest.CaptureFixture[str]):
    # GIVEN: An empty player inventory
    player.PLAYER.inventory = {}

    # WHEN: The inventory is checked
    Inventory([]).do()
    output = capsys.readouterr().out

    # THEN: The player is told their inventory is empty
    assert 'empty' in output, "When the inventory is empty, the player should be told this"

@pytest.mark.parametrize(
    ["args", "expected_string", 'expected_qty'], [
    (['1','thing'], 'thing', [1]),
    (['five','thing'], 'thing', [5]),
    (['thing','1'], 'thing', [1]),
    (['thing','two'], 'thing', [2]),
    (['thing', '1', 'option'], 'thing option', [1]),
    (['thing', 'one', 'option'], 'thing option', [1]),
    (['2', 'thing', '1', 'option'], 'thing option', [2, 1]),
    (['two', 'thing', 'one', 'option'], 'thing option', [2, 1]),
])

def test_args_setter(args, expected_string, expected_qty):
    # GIVEN: args consisting of a string and qty
    # THEN: The args are parsed and stored in the correct class attribute
    cmd = Command(args)

    assert cmd.arg_string == expected_string
    assert cmd.arg_qty == expected_qty

def test_drop_no_arg(capsys: pytest.CaptureFixture[str]):
    # WHEN: The player calls Drop with no argument
    Drop([]).do()
    output = capsys.readouterr().out

    # Then an error is displayed to the player
    assert "Error: You cannot drop nothing.\n" in output, \
        "Passing no argument should throw an error"

def test_drop_no_item(capsys: pytest.CaptureFixture[str]):
    # GIVEN: The items in the player's inventory
    player.PLAYER.inventory = {}
    Item.item_dict = {
        "ring": Item(
            key="ring",
            name="a ring",
            description="A metal circle.",
            can_take=True,
        )
    }

    # WHEN: The player tries to drop an item not in their inventory
    Drop(['ring']).do()
    output = capsys.readouterr().out

    # THEN: The player is told they do not have the item to drop
    assert "You dont have 1 ring to drop" in output, "The player cannot drop an item not in their inventory"

def test_drop_quantity_one(capsys: pytest.CaptureFixture[str]):
    # GIVEN: The current location and the items in the player's inventory
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {'ring':1}
    Item.item_dict = {
        "ring": Item(
            key="ring",
            name="a ring",
            description="A metal circle.",
            can_take=True,
        )
    }
    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={}
    )
    
    # WHEN: The player tries to drop an item in their inventory
    Drop(['ring', 1]).do()
    output = capsys.readouterr().out

    # THEN: The item is removed from the players inventory
    assert 'ring' not in player.PLAYER.inventory, \
        "The dropped item should be removed from player's inventory"
    
    # AND: The item is added to the current location's inventory
    assert 'ring' in Place.place_dict["shire"].inventory, \
        "the dropped item should be added to the current location inventory"

    # AND: The player is informed
    assert "You dropped 1 ring on the ground." in output, \
        "The player should be told they dropped the item"

def test_drop_qty(capsys: pytest.CaptureFixture[str]):
    # GIVEN: The current location and the items in the player's inventory
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {'ring':4}
    Item.item_dict = {
        "ring": Item(
            key="ring",
            name="a ring",
            description="A metal circle.",
            can_take=True,
        )
    }
    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={'ring':1}
    )
    
    # WHEN: The player tries to drop an item in their inventory
    Drop(['ring', 2]).do()
    output = capsys.readouterr().out

    # THEN: The item is removed from the players inventory
    assert player.PLAYER.inventory['ring'] == 2, \
        "The dropped item quantity should be reduced by 1 in player's inventory"
    
    # AND: The item is added to the current location's inventory
    assert Place.place_dict["shire"].inventory['ring'] == 3, \
        "the dropped item quantity should be increased by the qty in the location inventory"

    # AND: The player is informed
    assert "You dropped 2 ring on the ground." in output, \
        "The player should be told they dropped the item"

def test_drop_invalid_qty(capsys: pytest.CaptureFixture[str]):
    # GIVEN: The current location and the items in the player's inventory
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {'ring':2}
    Item.item_dict = {
        "ring": Item(
            key="ring",
            name="a ring",
            description="A metal circle.",
            can_take=True,
        )
    }
    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={'ring':1}
    )
    
    # WHEN: The player tries to drop an item in their inventory
    Drop(['ring', 3]).do()
    output = capsys.readouterr().out

    # THEN: The item is not removed from the players inventory
    assert player.PLAYER.inventory['ring'] == 2, \
        "The invalid qty item should not be removed from the players's inventory"
    
    # AND: The item is not added to the current location's inventory
    assert Place.place_dict["shire"].inventory['ring'] == 1, \
        "The invalid qty item should not be added to the location's inventory"

    # AND: The player is informed
    assert "You dont have 3 ring to drop." in output, \
        "The player should be told they do not have enough of the qty"

# TODO rename these tests, and add some versions of these tests for Item
def test_player_has_true():
    # GIVEN: The player's inventory
    player.PLAYER.inventory = {'ring':2}

    # WHEN: has_item() is called for an item/quantity the player possesses
    assert player.PLAYER.has_item('ring', 1), \
        "Should return True if the player has at least the specified qty"

def test_player_has_false():
    # GIVEN: The player's inventory
    player.PLAYER.inventory = {}

    # WHEN: has_item() is called for an item/quantity the player does not possess
    assert player.PLAYER.has_item('ring', 1) == False, \
        "Should return False if the player does not have the item"

def test_player_has_false_quantity():
    # GIVEN: The player's inventory
    player.PLAYER.inventory = {'ring':2}

    # WHEN: has_tiem() is called for an item/quantity the player does not possess
    assert player.PLAYER.has_item('ring', 3) == False, \
        "Should return False if the player does not have the specified qty"

def test_place_has_true():
    # GIVEN: A place with an inventory
    Place.place_dict["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        inventory={'ring':2} 
    )

    # WHEN: has_item() is called for an item/quantity the place possesses
    assert Place.place_dict["shire"].has_item('ring', 1) == True, \
        "Should return True if the place has at least the specified qty"

def test_place_has_false():
    # GIVEN: A place with an inventory
    Place.place_dict["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        inventory={} 
    )

    # WHEN: has_item() is called for an item/quantity the place possesses
    assert Place.place_dict["shire"].has_item('ring', 1) == False, \
        "Should return False if the place does not have the item"

def test_place_has_false_quantity():
    # GIVEN: A place with an inventory
    Place.place_dict["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        inventory={'ring':1} 
    )

    # WHEN: has_item() is called for an item/quantity the place possesses
    assert Place.place_dict["shire"].has_item('ring', 2) == False, \
        "Should return False if the place does not have the specified qty"

def test_place_has_shop_true():
    # GIVEN: A place with an inventory
    Place.place_dict["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        shop_inventory={'ring':2} 
    )

    # WHEN: has_item() is called for an item/quantity the place possesses
    assert Place.place_dict["shire"].has_shop_item('ring', 1) == True, \
        "Should return True if the place has at least the specified qty"

def test_place_has_shop_false():
    # GIVEN: A place with an inventory
    Place.place_dict["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        shop_inventory={} 
    )

    # WHEN: has_item() is called for an item/quantity the place possesses
    assert Place.place_dict["shire"].has_shop_item('ring', 1) == False, \
        "Should return False if the place does not have the item"

def test_place_has_shop_false_quantity():
    # GIVEN: A place with an inventory
    Place.place_dict["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        shop_inventory={'ring':1} 
    )

    # WHEN: has_item() is called for an item/quantity the place possesses
    assert Place.place_dict["shire"].has_shop_item('ring', 2) == False, \
        "Should return False if the place does not have the specified qty"

def test_is_for_sale():
    # GIVEN: An item with a price
    Item.item_dict = {
        "lockpicks": Item(
            key="lockpicks",
            name="lockpicking tools",
            description="A standard theiving kit.",
            price=-10
        ),
        "knife": Item(
            key="knife",
            name="blunt knife",
            description="An old knife.",
        )
    }

    # THEN: An item with a price returns True
    assert Item.item_dict["lockpicks"].is_for_sale(), \
        "An item with a price should return True"
    
    # AND: An item without a price returns False
    assert not Item.item_dict["knife"].is_for_sale(), \
        "An item without a price should return False"

# TODO add more shop tests, this one only covers part of what determines if an item shows in the shop
def test_shop_can(capsys: pytest.CaptureFixture[str]):
    # GIVEN: A place that can "shop" and has an inventory
    player.PLAYER.place = 'shire'
    Place.place_dict["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        can=['shop'],
        shop_inventory={'ring':1,
                   'stew':1, 
        } 
    )
    Item.item_dict = {
        "ring": Item(
            key="ring",
            name="The Ring",
            description="Not a normal ring.",
        ),
        "stew": Item(
            key="stew",
            name="Rabbit Stew",
            description="A bowl of rabbit stew.",
            price=-10
        ),
    }
    
    # WHEN: The Shop command is called
    Shop([]).do()
    output = capsys.readouterr().out

    # THEN: items that are for sale are printed
    assert "Rabbit Stew" in output, \
        "The player should be told the item with a price is for sale."

    # AND: items that are not for sale are not printed
    assert "The Ring" not in output, \
        "The player should not be told the item without a price is for sale."

def test_shop_no_can(capsys: pytest.CaptureFixture[str]):
    # GIVEN: A place that does not have can = ["shop"]
    player.PLAYER.place = 'shire'
    Place.place_dict["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        shop_inventory={'ring':1,
                   'stew':1, 
        } 
    )
    Item.item_dict = {
        "stew": Item(
            key="stew",
            name="Rabbit Stew",
            description="A bowl of rabbit stew.",
            price=-10
        ),
    }
    
    # WHEN: The Shop command is called
    Shop([]).do()
    output = capsys.readouterr().out

    # THEN: items that are for sale are printed
    assert "Sorry, you can't shop here." in output, \
        "The player should be told they are unable to shop."

def test_buy_no_arg(capsys: pytest.CaptureFixture[str]):
    player.PLAYER.place = 'shire'
    Place.place_dict["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        can=['shop'],
    )

    # WHEN: The player calls buy with no argument
    Buy([]).do()
    output = capsys.readouterr().out

    # Then an error is displayed to the player
    assert "Error: You cannot buy nothing.\n" in output, \
        "Passing no argument should throw an error"

def test_buy_no_can(capsys: pytest.CaptureFixture[str]):
    # GIVEN: A place that does not have can = ["shop"]
    player.PLAYER.place = 'shire'
    Place.place_dict["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
    )
    
    # WHEN: The Buy command is called
    Buy(['stew']).do()
    output = capsys.readouterr().out

    # THEN: the player is told they cannot shop here
    assert "Sorry, you can't shop here." in output, \
        "The player should be told they are unable to shop."

def test_buy_not_for_sale(capsys: pytest.CaptureFixture[str]):
    # GIVEN: A place that can "shop" and has an inventory without a price
    player.PLAYER.place = 'shire'
    Place.place_dict["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        can=['shop'],
        shop_inventory={'ring':1,
        } 
    )
    Item.item_dict = {
        "ring": Item(
            key="ring",
            name="The Ring",
            description="Not a normal ring.",
        ),
    }
    
    # WHEN: The Buy command is called
    Buy(['ring']).do()
    output = capsys.readouterr().out

    # THEN: items that are for sale are printed
    assert "Sorry, that item is not for sale" in output, \
        "The player should be told the item without a price is not for sale."

def test_buy_for_sale(capsys: pytest.CaptureFixture[str]):
    # GIVEN: A place that can "shop" and has an inventory with a price
    player.PLAYER.place = 'shire'
    Place.place_dict["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        can=['shop'],
        shop_inventory={'stew':1, 
        } 
    )
    Item.item_dict = {
        "stew": Item(
            key="stew",
            name="Rabbit Stew",
            description="A bowl of rabbit stew.",
            price=-10
        ),
    }
    
    # WHEN: The Buy command is called
    Buy(['stew']).do()
    output = capsys.readouterr().out

    # THEN: the player is not told the item is not for sale
    assert "Sorry, Rabbit Stew is not for sale" not in output, \
        "The player should not be told the item with a price is not for sale."

def test_buy_low_money(capsys: pytest.CaptureFixture[str]):
    # GIVEN: A place that can "shop" and has an inventory with a price, and a poor player
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {'gems':1}
    Place.place_dict["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        can=['shop'],
        shop_inventory={'stew':1, 
        } 
    )
    Item.item_dict = {
        "stew": Item(
            key="stew",
            name="Rabbit Stew",
            description="A bowl of rabbit stew.",
            price=-10
        ),
    }
    
    # WHEN: The Buy command is called
    Buy(['stew']).do()
    output = capsys.readouterr().out

    # THEN: the player is not told they cannot afford the item
    assert "Sorry, you can't afford Rabbit Stew" not in output, \
        "The player should not be told they are unable to afford the item."

def test_buy_no_money(capsys: pytest.CaptureFixture[str]):
    # GIVEN: A place that can "shop" and has an inventory with a price, and a poor player
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {}
    Place.place_dict["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        can=['shop'],
        shop_inventory={'stew':1, 
        } 
    )
    Item.item_dict = {
        "stew": Item(
            key="stew",
            name="Rabbit Stew",
            description="A bowl of rabbit stew.",
            price=-10
        ),
    }
    
    # WHEN: The Buy command is called
    Buy(['stew']).do()
    output = capsys.readouterr().out

    # THEN: the player is not told they cannot afford the item
    assert "Sorry, you can't afford Rabbit Stew" not in output, \
        "The player should not be told they are unable to afford the item."

def test_buy_no_money_free(capsys: pytest.CaptureFixture[str]):
    # GIVEN: A place that can "shop" and has an inventory with a free price, and a player w/ no gems
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {}
    Place.place_dict["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        can=['shop'],
        shop_inventory={'stew':1, 
        } 
    )
    Item.item_dict = {
        "stew": Item(
            key="stew",
            name="Rabbit Stew",
            description="A bowl of rabbit stew.",
            price=0
        ),
    }
    
    # WHEN: The Buy command is called
    Buy(['stew']).do()
    output = capsys.readouterr().out

    # THEN: the player is not told they cannot afford the item
    assert "You bought 1 Rabbit Stew" in output, "The player should be told they have bought the item"

def test_buy_no_qty(capsys: pytest.CaptureFixture[str]):
    # GIVEN: A place that can "shop" and has a single item with a price, and a moneyed player
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {'gems':50}
    Place.place_dict["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        can=['shop'],
        shop_inventory={'stew':1,
        } 
    )
    Item.item_dict = {
        "stew": Item(
            key="stew",
            name="Rabbit Stew",
            description="A bowl of rabbit stew.",
            price=-10
        ),
    }
    
    # WHEN: The Buy command is called
    Buy(['stew']).do()
    output = capsys.readouterr().out

    # THEN: The player aquires the item
    assert 'stew' in player.PLAYER.inventory, "The bought item should be in the player's inventory"

    # AND: the item is removed from the place
    assert 'stew' not in Place.place_dict["shire"].shop_inventory, "the bought item should no longer be at the place"

    # AND: The player's gems are reduced by the cost of the item
    assert player.PLAYER.inventory['gems'] == 40, "The players gems should be reduced by the cost of the item"

    # AND: The place's gems are increased by the cost of the item
    assert Place.place_dict["shire"].shop_inventory['gems'] == 10, "The place's gems should be increased by the cost of the item"

    # AND: the player is informed
    assert "You bought 1 Rabbit Stew for 10 gems" in output, "The player should be told they have bought the item"

def test_buy_invalid_qty(capsys: pytest.CaptureFixture[str]):
    # GIVEN: A place that can "shop" and has a multiple items with a price, and a moneyed player
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {'gems':50}
    Place.place_dict["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        can=['shop'],
        shop_inventory={'stew':2, 
        } 
    )
    Item.item_dict = {
        "stew": Item(
            key="stew",
            name="Rabbit Stew",
            description="A bowl of rabbit stew.",
            price=-10
        ),
    }
    
    # WHEN: The Buy command is called with a qty greater than the location's inventory
    Buy(['stew', 3]).do()
    output = capsys.readouterr().out

    # THEN: The player should acquire 0 of the item
    assert 'stew' not in player.PLAYER.inventory.keys(), "The invalid qty purchase should not be in the player's inventory"

    # AND: the location's item qty should not change
    assert Place.place_dict["shire"].shop_inventory['stew'] == 2, "The invalid qty purchase attempt should not change the location inv"

    # AND: The player's gems should not change
    assert player.PLAYER.inventory['gems'] == 50, "The invalid qty purchase should not change the player's gems"

    # AND: The place's gems are increased by the cost of the item
    assert 'gems' not in Place.place_dict["shire"].shop_inventory.keys(), "The invalid qty purchase should not change the place's gems"

    # AND: the player is informed
    assert "Sorry, there are not 3 stew here." in output, "The player should be told the location does not have the requested qty"

def test_buy_qty(capsys: pytest.CaptureFixture[str]):
    # GIVEN: A place that can "shop" and has a multiple items with a price, and a moneyed player
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {'gems':50}
    Place.place_dict["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        can=['shop'],
        shop_inventory={'stew':5, 
        } 
    )
    Item.item_dict = {
        "stew": Item(
            key="stew",
            name="Rabbit Stew",
            description="A bowl of rabbit stew.",
            price=-10
        ),
    }
    
    # WHEN: The Buy command is called with a qty >1
    Buy(['stew', 3]).do()
    output = capsys.readouterr().out

    # THEN: The player aquires the qty of the item
    assert player.PLAYER.inventory['stew'] == 3, "The bought item qty should be in the player's inventory"

    # AND: the item is removed from the place
    assert Place.place_dict["shire"].shop_inventory['stew'] == 2, "the bought item qty should be removed from the place"

    # AND: The player's gems are reduced by the cost of the item
    assert player.PLAYER.inventory['gems'] == 20, "The players gems should be reduced by the cost of the items"

    # AND: The place's gems are increased by the cost of the item
    assert Place.place_dict["shire"].shop_inventory['gems'] == 30, "The place's gems should be increased by the cost of the items"

    # AND: the player is informed
    assert "You bought 3 Rabbit Stew" in output, "The player should be told they have bought the item"

def test_read_no_arg(capsys: pytest.CaptureFixture[str]):
    # WHEN: The player calls read with no argument
    Read([]).do()
    output = capsys.readouterr().out

    # Then an error is displayed to the player
    assert "Error: You cannot read nothing.\n" in output, \
        "Passing no argument should throw an error"

def test_read_no_item(capsys: pytest.CaptureFixture[str]):
    # GIVEN: a location and player inventory
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {}
    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={}
        )

    # WHEN: the player tries to read an item that is not present
    Read(['magazine']).do()
    output = capsys.readouterr().out
    
    # THEN: the plater is told the item is not present
    assert "There is no magazine" in output, \
        "The player should be told the desired item is not present"

def test_read_place_no_writing(capsys: pytest.CaptureFixture[str]):
    # GIVEN: a location with an item that has no writing
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {}
    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={"stew":1}
        )
    Item.item_dict = {
        "stew": Item(
            key="stew",
            name="Rabbit Stew",
            description="A bowl of rabbit stew.",
        )
    }

    # WHEN: the player tries to read the item without writing
    Read(['stew']).do()
    output = capsys.readouterr().out
    
    # THEN: the player is told the item has nothing to read
    assert "There is nothing to read." in output, \
        "The player should be told the item has nothing to read"

def test_read_player_no_writing(capsys: pytest.CaptureFixture[str]):
    # GIVEN: a player inventory with an item that has no writing
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {"stew":1}
    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={}
        )
    Item.item_dict = {
        "stew": Item(
            key="stew",
            name="Rabbit Stew",
            description="A bowl of rabbit stew.",
        )
    }

    # WHEN: the player tries to read the item without writing
    Read(['stew']).do()
    output = capsys.readouterr().out
    
    # THEN: the player is told the item has nothing to read
    assert "There is nothing to read." in output, \
        "The player should be told the item has nothing to read"

def test_read_place(capsys: pytest.CaptureFixture[str]):
    # GIVEN: a place inventory with an item that has writing
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {}
    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={"magazine":1}
        )
    Item.item_dict = {
        "magazine": Item(
            key="magazine",
            name="Old Magazine",
            description="A popular magazine.",
            writing={"title":"Hobbiton Times",
                     "message":"blah blah blah blah blah",
            },
        )
    }

    # WHEN: the player tries to read the item with writing
    Read(['magazine']).do()
    output = capsys.readouterr().out
    
    # THEN: the player is told the title and message
    assert "Hobbiton Times" in output, \
        "The player should be told the item's title"
    
    assert "blah blah blah blah blah" in output, \
        "The player should be told the item's message"

def test_read_player(capsys: pytest.CaptureFixture[str]):
    # GIVEN: a player inventory with an item that has writing
    player.PLAYER.place = 'shire'
    player.PLAYER.inventory = {"magazine":1}
    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={}
        )
    Item.item_dict = {
        "magazine": Item(
            key="magazine",
            name="Old Magazine",
            description="A popular magazine.",
            writing={"title":"Hobbiton Times",
                     "message":"blah blah blah blah blah",
            },
        )
    }

    # WHEN: the player tries to read the item with writing
    Read(['magazine']).do()
    output = capsys.readouterr().out
    
    # THEN: the player is told the title and message
    assert "Hobbiton Times" in output, \
        "The player should be told the item's title"
    
    assert "blah blah blah blah blah" in output, \
        "The player should be told the item's message"

@pytest.mark.parametrize(
    ["a", "b", "expected"], [
    (1, 1, 2),
    (2, 2, 4),
])
def test_example(a, b, expected):
    assert a + b == expected

@pytest.mark.parametrize(
        ['start','amount','expected','message'], [
        (50, 10, 60, "A positive number should be added to health"),
        (50, -10, 40, "A negative number should be subtracted from health"),
        (50, -51, 0, "Heath should not drop below 0"),
        (50, 51, player.MAX_HEALTH, "Health should not go above {MAX_HEALTH}"),
])
def test_change_health(start, amount, expected, message):
    # GIVEN: the player's initial health
    player.PLAYER.current_health = start

    # WHEN: the health_change method is called
    player.PLAYER.change_health(amount)
    
    # THEN: the player's health should be changed by the # passed to health_change
    assert player.PLAYER.current_health == expected, message

def test_pet_no_arg(capsys: pytest.CaptureFixture[str]):
    Pet([]).do()
    output = capsys.readouterr().out

    assert "Error: You cannot pet nothing.\n" in output, \
        "Passing no argument should throw an error"

def test_pet_cant(capsys: pytest.CaptureFixture[str]):
    # GIVEN: a place where you can't pet anything
    player.PLAYER.place = 'shire'
    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            can=[],
        )
    
    # WHEN: the player tries to pet anything
    Pet(['kitty']).do()
    output = capsys.readouterr().out
    
    # THEN: the player is told they cannot pet at this location
    assert "You cannot do that here." in output, \
        "The player should be told petting isn't an option at the current location"

def test_pet_no_target(capsys: pytest.CaptureFixture[str]):
    # GIVEN: The player is at a location that accepts petting
    player.PLAYER.place = 'shire'
    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            can=['pet'],
        )
    
    # WHEN: The player tries to pet but does not specify the 'dragon' or 'head'
    Pet(['red']).do()
    output = capsys.readouterr().out

    # THEN: The player is told they must specify
    assert "What are you trying to pet?" in output, \
        "If 'dragon' or 'head' is not specified, the player should be told to specify the target for the pets."

def test_pet_no_color(capsys: pytest.CaptureFixture[str]):
    # GIVEN: The player is at a location that accepts petting
    player.PLAYER.place = 'shire'
    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            can=['pet'],
        )
    
    # WHEN: The player tries to pet but does not specify the color
    Pet(['dragon', 'head']).do()
    output = capsys.readouterr().out

    # THEN: The player is told they must specify
    assert "Which dragon's head do you want to pet?" in output, \
        "The player should be told they must specify which dragon they want to pet."

def test_pet_invalid_color(capsys: pytest.CaptureFixture[str]):
    # GIVEN: The player is at a location that accepts petting and a list of valid colors
    player.PLAYER.place = 'shire'
    Place.place_dict["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            can=['pet'],
        )
    Dragon_head.dragon_dict = {
            "red": Dragon_head(
                key="red",
                name="Red Dragon",
                description="It's red.",
            ),
        }
    
    # WHEN: The player tries to pet but does not specify a valid color
    Pet(['beige', 'head']).do()
    output = capsys.readouterr().out

    # THEN: The player is told the color is invalid
    assert "You do not see such a dragon." in output, \
        "The player should be told the color is not valid."

def test_pet(capsys: pytest.CaptureFixture[str]):
    # GIVEN: A dragon and a mood, and a player at a location that allows petting
    player.PLAYER.place = 'mountain'
    Place.place_dict["mountain"] = Place(
            key="mountain",
            name="The Misty Mountain",
            description="Big ol rock.",
            can=['pet'],
        )
    items_and_locations.Dragon_head.MOODS = [
        {"mood": "moody", "treasure": [], "damage": [], "message": ("")}
    ]
    Dragon_head.dragon_dict = {
            "purple": Dragon_head(
                key="purple",
                name="Purple Dragon",
                description="It's purple.",
            )
    }
    
    # WHEN: the player pets the dragon
    Pet(['purple', 'head']).do()
    output = capsys.readouterr().out

    # THEN: the mood is assigned, the player is told
    assert "dragon's moody purple head" in output, \
        "The player should be told the head color and the mood"

def test_moods_assignment():
    # GIVEN: A dragon and a mood
    items_and_locations.Dragon_head.MOODS = [
        {"mood": "moody", "treasure": [1,1], "damage": [2,2], "message": ("snorts at you.")}
    ]
    Dragon_head.dragon_dict = {
            "purple": Dragon_head(
                key="purple",
                name="Purple Dragon",
                description="It's purple.",
            )
    }
    
    # THEN: the instantiated dragon should have the mood assigned, and the mood should be removed
    assert Dragon_head.dragon_dict["purple"].mood == "moody", "The mood should be assigned"
    assert Dragon_head.dragon_dict["purple"].treasure == [1,1], "The treasure should be assigned"
    assert Dragon_head.dragon_dict["purple"].damage == [2,2], "The damage should be assigned"
    assert Dragon_head.dragon_dict["purple"].message == "snorts at you.", "The message should be assigned"
    assert len(items_and_locations.Dragon_head.MOODS) == 0, \
        "The mood should be removed from the list after assignment"

def test_pet_treasure(capsys: pytest.CaptureFixture[str]):
    # GIVEN: A dragon with treasure
    player.PLAYER.place = 'mountain'
    player.PLAYER.inventory = {'gems':10}
    Place.place_dict["mountain"] = Place(
            key="mountain",
            name="The Misty Mountain",
            description="Big ol rock.",
            can=['pet'],
        )
    items_and_locations.Dragon_head.MOODS = [
            {"mood": "generous",
            "treasure": [5,5],
            "damage": [],
            "message": ("thinks you're adorable! He gives you {treasure} gems!")
            }
    ]
    Dragon_head.dragon_dict = {
            "purple": Dragon_head(
                key="purple",
                name="Purple Dragon",
                description="It's purple.",
            )
    }

    # WHEN: the player pets the dragon
    Pet(['purple', 'head']).do()
    output = capsys.readouterr().out

    # THEN: The player should receive some gems and be told about it.
    assert player.PLAYER.inventory['gems'] == 15, \
        "The gems should be added to the player's inventory"
    assert "5 gems" in output, \
        "The player should be told they received gems"

def test_pet_no_treasure(capsys: pytest.CaptureFixture[str]):
    # GIVEN: A dragon with no treasure
    player.PLAYER.place = 'mountain'
    player.PLAYER.inventory = {'gems':10}
    Place.place_dict["mountain"] = Place(
            key="mountain",
            name="The Misty Mountain",
            description="Big ol rock.",
            can=['pet'],
        )
    items_and_locations.Dragon_head.MOODS = [
            {"mood": "generous",
            "treasure": [],
            "damage": [],
            "message": ("")
            }
    ]
    Dragon_head.dragon_dict = {
            "purple": Dragon_head(
                key="purple",
                name="Purple Dragon",
                description="It's purple.",
            )
    }

    # WHEN: the player pets the dragon
    Pet(['purple', 'head']).do()
    output = capsys.readouterr().out

    # THEN: The player should not receive gems, and not be told about it.
    assert player.PLAYER.inventory['gems'] == 10, \
        "The players gems should be unchanged"
    assert "gems" not in output, \
        "The player should not be told they received gems"

def test_pet_damage(capsys: pytest.CaptureFixture[str]):
    # GIVEN: A dragon with that does damage
    player.PLAYER.place = 'mountain'
    player.PLAYER.current_health = 50
    Place.place_dict["mountain"] = Place(
            key="mountain",
            name="The Misty Mountain",
            description="Big ol rock.",
            can=['pet'],
        )
    items_and_locations.Dragon_head.MOODS = [
            {"mood": "generous",
            "treasure": [],
            "damage": [7,7],
            "message": ("singes your hair, costing you {damage} in health.")
            }
    ]
    Dragon_head.dragon_dict = {
            "purple": Dragon_head(
                key="purple",
                name="Purple Dragon",
                description="It's purple.",
            )
    }

    # WHEN: the player pets the dragon
    Pet(['purple', 'head']).do()
    output = capsys.readouterr().out

    # THEN: The player should receive some damage and be told about it.
    assert player.PLAYER.current_health == 43, \
        "The players health should be reduced by the damage amount"
    assert "costing you -7 in health" in output, \
        "The player should be told they received damage"

def test_pet_no_damage(capsys: pytest.CaptureFixture[str]):
    # GIVEN: A dragon with that does damage
    player.PLAYER.place = 'mountain'
    player.PLAYER.current_health = 50
    Place.place_dict["mountain"] = Place(
            key="mountain",
            name="The Misty Mountain",
            description="Big ol rock.",
            can=['pet'],
        )
    items_and_locations.Dragon_head.MOODS = [
            {"mood": "generous",
            "treasure": [],
            "damage": [],
            "message": ("")
            }
    ]
    Dragon_head.dragon_dict = {
            "purple": Dragon_head(
                key="purple",
                name="Purple Dragon",
                description="It's purple.",
            )
    }

    # WHEN: the player pets the dragon
    Pet(['purple', 'head']).do()
    output = capsys.readouterr().out

    # THEN: The player should receive some damage and be told about it.
    assert player.PLAYER.current_health == 50, \
        "The players health should be unchanged"
    assert "in health" not in output, \
        "The player should not be told they received damage"

def test_pet_treasure_and_damage(capsys: pytest.CaptureFixture[str]):
    # GIVEN: A dragon with that does damage and gives treasure
    player.PLAYER.place = 'mountain'
    player.PLAYER.current_health = 50
    player.PLAYER.inventory = {'gems':10}
    Place.place_dict["mountain"] = Place(
            key="mountain",
            name="The Misty Mountain",
            description="Big ol rock.",
            can=['pet'],
        )
    items_and_locations.Dragon_head.MOODS = [
            {"mood": "generous",
            "treasure": [15,15],
            "damage": [5,5],
            "message": ("He gives you {treasure} gems! But bites, costing you {damage} in health.")
            }
    ]
    Dragon_head.dragon_dict = {
            "purple": Dragon_head(
                key="purple",
                name="Purple Dragon",
                description="It's purple.",
            )
    }

    # WHEN: the player pets the dragon
    Pet(['purple', 'head']).do()
    output = capsys.readouterr().out

    # THEN: The player should receive some damage and treasure be told about it.
    assert player.PLAYER.current_health == 45, \
        "The players health should be reduced by the damage amount"
    assert "costing you -5 in health" in output, \
        "The player should be told they received damage"
    assert player.PLAYER.inventory['gems'] == 25, \
        "The gems should be added to the player's inventory"
    assert "15 gems" in output, \
        "The player should be told they received gems"

def test_eat_no_arg(capsys: pytest.CaptureFixture[str]):
    # WHEN: the player attempts to eat/drink but does not specify an item
    Eat([]).do()
    output = capsys.readouterr().out

    # THEN: the player is told they must specify an item
    assert "Error: You cannot eat nothing.\n" in output, \
    "Passing no argument should throw an error"

def test_drink_no_arg(capsys: pytest.CaptureFixture[str]):
    # WHEN: the player attempts to eat/drink but does not specify an item
    Drink([]).do()
    output = capsys.readouterr().out

    # THEN: the player is told they must specify an item
    assert "Error: You cannot drink nothing.\n" in output, \
    "Passing no argument should throw an error"


def test_consume_no_item(capsys: pytest.CaptureFixture[str]):
    # GIVEN: an empty player inventory
    player.PLAYER.inventory = {'gems':10}
    Item.item_dict = {
        "cracker": Item(
            key="cracker",
            name="saltine cracker",
            description="A flat square of carbs.",
            ),
    }

    # WHEN: the player attempts to eat/drink an item not in the player's inventory
    Eat(['cracker']).do()
    output = capsys.readouterr().out

    # THEN: the player is told they must possess an item to eat/drink it
    assert "you do not posses a cracker." in output, \
        "The player should be told if they are missing the desired consumable"

def test_consume_invalid_item(capsys: pytest.CaptureFixture[str]):
    # GIVEN: a non-consumable item in the player's inventory
    player.PLAYER.inventory = {'cracker':10}
    Item.item_dict = {
        "cracker": Item(
            key="cracker",
            name="saltine cracker",
            description="A flat square of carbs.",
            ),
    }

    # WHEN: the player ties to eat/drink the item
    Eat(['cracker']).do()
    output = capsys.readouterr().out
    
    # THEN: the player it told they cannot eat/drink that particular item
    assert "Sorry, your saltine cracker is not eatable." in output, \
    "The player should be told if they are missing the desired consumable"

def test_consume_eat(capsys: pytest.CaptureFixture[str]):
    # GIVEN: an eatable item in the player's inventory
    player.PLAYER.current_health = 50
    player.PLAYER.inventory = {'cracker':10}
    Item.item_dict = {
        "cracker": Item(
            key="cracker",
            name="saltine cracker",
            description="A flat square of carbs.",
            eat_message=("You place the cracker on your tongue.",
                         "It tastes salty.",
            ),
            health_change=10
            ),
    }

    # WHEN: the player tries to eat the item
    Eat(['cracker']).do()
    output = capsys.readouterr().out
    
    # THEN: The players inventory should be reduced
    assert player.PLAYER.inventory['cracker'] == 9, \
        "The player's inventory should be reduced when eating an item"

    # THEN: The player is told they ate the item
    assert "You place the cracker on your tongue" in output, \
        "The player should be told the items eat_message"
    
    # THEN: The players health is adjusted by the appropriate amount
    assert player.PLAYER.current_health == 60, \
        "The players health should be adjusted by the item's health value"

    # THEN: The player is told their health was adjusted
    assert "You feel your health change by 10." in output, \
        "The player should be told their health changed"

def test_consume_drink(capsys: pytest.CaptureFixture[str]):
    # GIVEN: a drinkable item in the player's inventory
    player.PLAYER.current_health = 50
    player.PLAYER.inventory = {'poison':5}
    Item.item_dict = {
        "poison": Item(
            key="poison",
            name="Rat Poison",
            description="A bottle of foul smelling rat poison.",
            drink_message=("You sip the contents of the bottle.",
                           "It tastes revolting.",
            ),
            health_change=-25
            ),
    }

    # WHEN: the player tries to drink the item
    Drink(['poison']).do()
    output = capsys.readouterr().out

    # THEN: The players inventory should be reduced
    assert player.PLAYER.inventory['poison'] == 4, \
        "The player's inventory should be reduced when drinking an item"

    # THEN: The players health is adjusted by the appropriate amount
    assert "You sip the contents of the bottle" in output, \
        "The player should be told the items drink_message"

    # THEN: The player is told they drank the item
    assert player.PLAYER.current_health == 25, \
        "The players health should be adjusted by the item's health value"

    # THEN: The player is told their health was adjusted
    assert "You feel your health change by -25." in output, \
        "The player should be told their health changed"

def test_consume_last_item(capsys: pytest.CaptureFixture[str]):
    # GIVEN: a drinkable item in the player's inventory
    player.PLAYER.current_health = 50
    player.PLAYER.inventory = {'poison':1}
    Item.item_dict = {
        "poison": Item(
            key="poison",
            name="Rat Poison",
            description="A bottle of foul smelling rat poison.",
            drink_message=("You sip the contents of the bottle.",
                           "It tastes revolting.",
            ),
            health_change=-25
            ),
    }

    # WHEN: the player tries to drink the item
    Drink(['poison']).do()
    output = capsys.readouterr().out

    # THEN: The players inventory should be reduced
    assert 'poison' not in player.PLAYER.inventory.keys(), \
        "The item should be removed from the player's inventory when there was only 1 qty"

# shlex.split('abc 123') == ['abc', '123']
# shlex.split('abc "xyz blah"') == ['abc', 'xyz blah']