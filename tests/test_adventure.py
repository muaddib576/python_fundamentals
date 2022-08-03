from copy import deepcopy
import pytest
import python_fundamentals.adventure as adventure
from python_fundamentals.adventure import (
    ITEMS,
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
    Inventory,
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

def test_collectable_get():
    # GIVEN: An item
    adventure.ITEMS = {}
    adventure.ITEMS['cup'] = Item(
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
    adventure.ITEMS = {}

    # WHEN: get() class method is called on an key that is not present
    with pytest.raises(Exception) as info:
        Item.get('cup')

    # THEN: An exception is raised for the player
    exception = info.value
    assert "This is embarrasing" in str(exception)

@pytest.mark.skip(reason="method to be deleted")
def test_towards():
    # GIVEN: Two linked locations

    adventure.PLACES["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            east="mordor"
        )
    adventure.PLACES["mordor"] = Place(
            key="mordor",
            name="Mordor",
            description="Buncha orcs.",
            west="shire"
        )


    # WHEN: One is passed a direction
    place = PLACES["mordor"]

    # place.get("xxx")
    # Place.get("mordor")

    destination = place.towards('west')

    # THEN: The linked location is returned
    assert destination == 'shire'

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

def test_examine_missing_from_place_and_player_inv(capsys):
    # GIVEN: That the item the player wants to examine is not in the current
    #        place, and not in the player's inventory
    adventure.PLAYER.place = 'shire'
    adventure.PLAYER.inventory = {}
    adventure.PLACES = {
        "shire": Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={}
        )
    }
    
    # WHEN: The player tries to examine it
    Examine(['grass']).do()
    output = capsys.readouterr().out

    # THEN: The player should be told they can't
    assert "Error: There is no grass in the shire." in output, \
        "An Examine target not in the current location or player inventory should throw an error"

def test_examine_missing_from_place(capsys):
    # GIVEN: That the item the player wants to examine is not in the current
    #        place, but is in the player's inventory
    adventure.PLAYER.place = 'shire'
    adventure.PLAYER.inventory = {'grass':1}
    adventure.PLACES = {
        "shire": Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={}
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

def test_examine_missing_from_player_inv(capsys):
    # GIVEN: That the item the player wants to examine is not in the player's inventorty
    #        but is in the current place
    adventure.PLAYER.place = 'shire'
    adventure.PLAYER.inventory = {}
    adventure.PLACES = {
        "shire": Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={'grass':1,'hills':1}
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

def test_examine_missing_item(capsys):
    adventure.PLAYER.place = 'shire'
    adventure.PLACES = {
        "shire": Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={'grass':1,'hills':1}
        )
    }
    adventure.ITEMS = {}

    Examine(['hills']).do()
    output = capsys.readouterr().out

    assert 'Hmmm, "hills" seems to be missing from my files.' in output, \
        "An Examine target not in the the ITEMS dictionary should throw an error"

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
            inventory={'grass':1}
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
            inventory={'grass':1}
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
    assert 'grass' not in adventure.PLACES["shire"].inventory, "the tooken item should no longer be at the place"

    # AND: the player is informed
    assert "You pick up" in output, "The player should be told they have aquired the item"

def test_take_missing_item(capsys):
    # GIVEN: The player's current location and an item that is not present
    adventure.PLAYER.place = 'shire'
    adventure.PLAYER.inventory = {}
    adventure.PLACES["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={}
        )

    # WHEN: The player tries to take the item
    Take(['grass']).do()
    output = capsys.readouterr().out

    # THEN: The player is told the item is not present
    assert "there is no grass here" in output, "The player should be told the desired item is not present"

    # AND: gets nothing
    assert 'grass' not in adventure.PLAYER.inventory, "The desired item should not be in the player's inventory"

def test_take_invalid_item(capsys):
    # GIVEN: The player's current location and a invalid item
    adventure.PLAYER.place = 'shire'
    adventure.PLAYER.inventory = {}
    adventure.PLACES["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={'grass':1}
        )
    adventure.ITEMS = {}

    # WHEN: The player tries to take the item
    with pytest.raises(Exception) as info:
        Take(['grass']).do()

    # THEN: The player is told the item info is missing
    exception = info.value
    assert "This is embarrasing" in str(exception)

    # AND: gets nothing
    assert 'grass' not in adventure.PLAYER.inventory, "The desired item should not be put in the player's inventory"

    # AND: the item is not removed from the location
    assert 'grass' in adventure.PLACES["shire"].inventory, "the desired item should remain at the place"

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

def test_take_untakable_item(capsys):
    # GIVEN: The player's current location and an untakable item
    adventure.PLAYER.place = 'shire'
    adventure.PLAYER.inventory = {}
    adventure.PLACES["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={'grass':1}
        )

    adventure.ITEMS = {
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
    assert 'grass' not in adventure.PLAYER.inventory, "The desired item should not be put in the player's inventory"

    # AND: the item is not removed from the location
    assert 'grass' in adventure.PLACES["shire"].inventory, "the desired item should remain at the place"

def test_inventory(capsys):
    # GIVEN: Items in the player inventory
    adventure.PLAYER.inventory = {'lockpicks':1, 'knife':2}
    adventure.ITEMS = {
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
    Inventory('args').do()
    output = capsys.readouterr().out

    # THEN: The inventory contents are displayed
    assert '(x 1) lockpicking tools' in output, "The player should be told the items their inventory"

    # AND: The inventory contents are displayed
    assert '(x 2) blunt knife' in output, "The player should be told the items their inventory"

def test_inventory_empty(capsys):
    # GIVEN: An empty player inventory
    adventure.PLAYER.inventory = {}

    # WHEN: The inventory is checked
    Inventory('args').do()
    output = capsys.readouterr().out

    # THEN: The player is told their inventory is empty
    assert 'empty' in output, "When the inventory is empty, the player should be told this"

#TODO add test_do_shop

# shlex.split('abc 123') == ['abc', '123']
# shlex.split('abc "xyz blah"') == ['abc', 'xyz blah']