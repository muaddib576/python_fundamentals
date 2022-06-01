from copy import deepcopy
import pytest
import python_fundamentals.adventure as adventure
from python_fundamentals.adventure import (
    PLACES,
    Go,
    Examine,
    Command,
    Place,
    Item,
    error,
    debug,
    header,
    write,
    Look,
    Take,
    )

PLAYER_STATE = deepcopy(adventure.PLAYER)
PLACES_STATE = deepcopy(adventure.PLACES)
ITEMS_STATE = deepcopy(adventure.ITEMS)
MARGIN_STATE = deepcopy(adventure.MARGIN)


def revert():
    """Revert game data to its original state."""
    adventure.PLAYER = deepcopy(PLAYER_STATE)
    adventure.PLACES = deepcopy(PLACES_STATE)
    adventure.ITEMS = deepcopy(ITEMS_STATE)
    adventure.MARGIN = deepcopy(MARGIN_STATE)


@pytest.fixture(autouse=True)
def teardown(request):
    """Auto-add teardown method to all tests."""
    request.addfinalizer(revert)

def test_error(capsys):
    error("error test")
    output = capsys.readouterr().out
    
    assert output == "Error: error test\n"

def test_debug(capsys):
    debug("debug test")
    output = capsys.readouterr().out

    assert output == f"!!! debug test\n"

def test_header(capsys):
    header("header test")
    output = capsys.readouterr().out

    assert output == f"\n{adventure.MARGIN}header test\n\n"

def test_write(capsys):
    write("write test")
    output = capsys.readouterr().out

    assert output == f"{adventure.MARGIN}write test\n"

def test_go(capsys):
    Go(['east']).do()
    output = capsys.readouterr().out

    assert "The square part of town." in output

def test_examine_no_arg(capsys):
    Examine([]).do()
    output = capsys.readouterr().out

    assert "Error: You cannot examine nothing.\n" in output, \
        "Passing no argument should throw an error"

def test_examine_missing_from_place(capsys):
    # GIVEN: That the item the player wants to examine is not in the current
    #        place
    adventure.PLAYER.place = 'shire'
    adventure.PLACES = {
        "shire": Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            contents=['grass','hills']
        )
    }
    
    # WHEN: The player tries to examine it
    Examine(['castle']).do()
    output = capsys.readouterr().out

    # THEN: The player should be told they can't
    assert "Error: There is no castle in the shire." in output, \
        "An Examine target not in the current location should throw an error"

def test_examine_missing_item(capsys):
    adventure.PLAYER.place = 'shire'
    adventure.PLACES = {
        "shire": Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            contents=['grass','hills']
        )
    }
    adventure.ITEMS = {}

    Examine(['hills']).do()
    output = capsys.readouterr().out

    assert 'Hmmm, "hills" seems to be missing from my files.' in output, \
        "An Examine target not in the the ITEMS dictionary should throw an error"

def test_examine_full(capsys):
    # GIVEN: The player is in a place that exists and tries to examine an item that is present,
    adventure.PLAYER.place = 'shire'
    adventure.PLACES = {
        "shire": Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            contents=['grass','hills']
        )
    }
    adventure.ITEMS = {
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

def test_get_place_start(capsys):
    
    assert Command('args').player_place == adventure.PLACES[adventure.PLAYER.place], \
        "Starting location should be 'your cottage'"
    
def test_get_place_missing_place(capsys):
    adventure.PLAYER.place = 'shire'
    adventure.PLACES = {}

    Command('args').player_place
    output = capsys.readouterr().out

    assert output == "Error: It seems the player exists outside the known universe...\n", \
        "A location not in Places should throw an error"

def test_comma_list_3():
    # GIVEN: a list of 3 or more elements
    test_list = ['1','2','3']
    # WHEN: the list is passed to the comma_list() method
    test_string = Command('args').comma_list(test_list)
    # THEN: a comma seperated string is returned
    assert test_string == "1, 2, and 3", " A list of three should be comma seperated"

def test_comma_list_2():
    # GIVEN: a list of 2 elements
    test_list = ['1','2']
    # WHEN: the list is passed to the comma_list() method
    test_string = Command('args').comma_list(test_list)
    # THEN: a string with both elements seperated by an 'and' is returned
    assert test_string == "1 and 2", "A list of 2 should be and seperated"

def test_comma_list_1():
    # GIVEN: a list of 1 element
    test_list = ['1']
    # WHEN: the list is passed to the comma_list() method
    test_string = Command('args').comma_list(test_list)
    # THEN: a string with that element is returned
    assert test_string == "1", "A list of one should return itself"

def test_comma_list_0():
    # GIVEN: a list of 0 elements
    test_list = []
    # WHEN: the list is passed to the comma_list() method
    test_string = Command('args').comma_list(test_list)
    # THEN: an error is returned
    assert test_string == "", "A list of nothing should return an empty string"

def test_look_place(capsys):
    
    # GIVEN: The player's current location
    adventure.PLAYER.place = 'shire'
    adventure.PLACES["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
        )

    # WHEN: The player activates Look
    Look('args').do()
    output = capsys.readouterr().out

    # THEN: The player is told the description of the current location
    assert "Buncha hobbits" in output, "The description of the current location should print"

def test_look_items(capsys):
    
    # GIVEN: The player's current location
    adventure.PLAYER.place = 'shire'
    adventure.PLACES["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            contents=['grass']
        )

    adventure.ITEMS = {
        "grass": Item(
            key="grass",
            name="grass blades",
            description="It's grass.",
            price=-10,
        )
    }

    # WHEN: The player activates Look
    Look('args').do()
    output = capsys.readouterr().out

    # THEN: The player is told the list of items present in the location
    assert "grass blades" in output, "The names of the items in the current locations should print"

def test_look_no_items(capsys):
    
    # GIVEN: The player's current location
    adventure.PLAYER.place = 'shire'
    adventure.PLACES["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
        )

    # WHEN: The player activates Look
    Look('args').do()
    output = capsys.readouterr().out

    # THEN: The player is told the list of items present in the location
    assert "You see" not in output, "If there are no items in the location, you can't see anything"

def test_look_nearby(capsys):
    
    # GIVEN: The player's current location
    adventure.PLAYER.place = 'shire'
    adventure.PLACES = {
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
    Look('args').do()
    output = capsys.readouterr().out

    # THEN: The player is told the list of nearby places
    assert "Mordor" in output, "The names of the nearby locations should print"
    assert "The Sea" in output, "The names of the nearby locations should print"

def test_look_no_nearby(capsys):
    
    # GIVEN: The player's current location
    adventure.PLAYER.place = 'shire'
    adventure.PLACES["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
        )

    # WHEN: The player activates Look
    Look('args').do()
    output = capsys.readouterr().out

    # THEN: The player is told the list of nearby places
    assert "To the" not in output, "If there is nothing nearby, the names of the nearby locations should not print"

def test_take_valid_item(capsys):
    
    # GIVEN: The player's current location and a valid item
    adventure.PLAYER.place = 'shire'
    adventure.PLAYER.inventory = {}
    adventure.PLACES["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            contents=['grass']
        )

    adventure.ITEMS = {
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
    assert 'grass' in adventure.PLAYER.inventory, "The tooken item should be in the player's inventory"

    # AND: the item is removed from the place
    assert 'grass' not in adventure.PLACES["shire"].contents, "the tooken item should no longer be at the place"

    # AND: the player is informed
    assert "You pick up" in output, "The player should be told they have aquired the item"

def test_take_invalid_item():
    ...
    # GIVEN: The player's current location and a invalid item

    # WHEN: The player tries to take an invalid item

    # THEN: The player gets nothing



#TODO add test_do_shop

# shlex.split('abc 123') == ['abc', '123']
# shlex.split('abc "xyz blah"') == ['abc', 'xyz blah']