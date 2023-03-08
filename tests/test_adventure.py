from copy import deepcopy
import pytest
import python_fundamentals.adventure as adventure
from python_fundamentals.adventure import (
    ITEMS,
    PLACES,
    PLAYER,
    Contents,
    Go,
    Examine,
    Command,
    Place,
    Item,
    InvalidItemError,
    InvalidPlaceError,
    error,
    abort,
    debug,
    header,
    write,
    wrap,
    Look,
    Take,
    Inventory,
    Drop,
    Shop,
    Buy,
    Read,
    )

PLAYER_STATE = deepcopy(adventure.PLAYER)
PLACES_STATE = deepcopy(adventure.PLACES)
ITEMS_STATE = deepcopy(adventure.ITEMS)
MARGIN_STATE = deepcopy(adventure.MARGIN)
WIDTH_STATE = deepcopy(adventure.WIDTH)


def revert():
    """Revert game data to its original state."""
    adventure.PLAYER = deepcopy(PLAYER_STATE)
    adventure.PLACES = deepcopy(PLACES_STATE)
    adventure.ITEMS = deepcopy(ITEMS_STATE)
    adventure.MARGIN = deepcopy(MARGIN_STATE)
    adventure.WIDTH = deepcopy(WIDTH_STATE)


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

def test_teardown():
    """Test that item key added in previous test does not persist"""
    assert "shire" not in adventure.PLACES, \
        """Each test should have a fresh data set"""

def test_error(capsys):
    error("error test")
    output = capsys.readouterr().out
    
    assert output == "Error: error test\n"

def test_abort():
    with pytest.raises(SystemExit):
        abort("abort test")

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

def test_wrap(capsys):
    # GIVEN: The default WIDTH and MARGIN
    adventure.WIDTH = 10
    adventure.MARGIN = ' '*3

    # WHEN: the wrap function is called
    test_string = '*' * 14
    wrap(test_string)
    output = capsys.readouterr().out

    # THEN: the default WIDTH and MARGIN are used
    assert output == f"{adventure.MARGIN}*******\n{adventure.MARGIN}*******\n"

def test_wrap_custom(capsys):
    # WHEN: the wrap function is passed custom width and margin values
    test_string = '*' * 11
    width = 10
    initial_indent = ' '*4
    subsequent_indent = ' '*5

    wrap(test_string, width, initial_indent, subsequent_indent)
    output = capsys.readouterr().out

    # THEN: the specified indent values are used
    assert output == f"{initial_indent}******\n{subsequent_indent}*****\n"

def test_go(capsys):
    adventure.PLAYER.place = 'home'
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
    adventure.ITEMS = {
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

    with pytest.raises(InvalidItemError) as info:
        Examine(['hills']).do()

def test_examine_in_shop(capsys):
    # GIVEN: That the item the player wants to examine is not in the player's inventorty
    #        but is in the current place, and the current place is a shop
    adventure.PLAYER.place = 'shire'
    adventure.PLAYER.inventory = {}
    adventure.PLACES = {
        "shire": Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={'grass':3,'hills':1},
            can=['shop']
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

    # THEN: The player should be told the description of the item and its price.
    assert "It's grass. The shop has 3, you can buy one for 10 gems." in output, \
        "An Examine target should print the item description. Also, if the location can shop, the quantity/price."

def test_get_place_start(capsys):
    assert Command([]).player_place == adventure.PLACES[adventure.PLAYER.place], \
        "Starting location should be 'your cottage'"
    
def test_get_place_missing_place(capsys):
    adventure.PLAYER.place = 'shire'
    adventure.PLACES = {}

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

def test_look_place(capsys):
    
    # GIVEN: The player's current location
    adventure.PLAYER.place = 'shire'
    adventure.PLACES["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
        )

    # WHEN: The player activates Look
    Look([]).do()
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
    Look([]).do()
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
    Look([]).do()
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
    Look([]).do()
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
    Look([]).do()
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
    assert "there are not 1 grass here" in output, "The player should be told the desired item is not present"

    # AND: gets nothing
    assert 'grass' not in adventure.PLAYER.inventory, "The desired item should not be in the player's inventory"

def test_take_invalid_item():
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

def test_take_quantity_one(capsys):
    # GIVEN: The current location with items present and player's inventory
    adventure.PLAYER.place = 'shire'
    adventure.PLAYER.inventory = {}
    adventure.PLACES["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={'ring': 1}
    ) 
    adventure.ITEMS = {
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
    assert 'ring' not in adventure.PLACES["shire"].inventory, \
        "the tooken item should be removed from the current location inventory"

    # AND: The item is added to the player's inventory
    assert 'ring' in adventure.PLAYER.inventory, \
        "The tooken item should be added to player's inventory"

    # AND: The player is informed
    assert "You pick up 1 ring and put it in your bag." in output, \
        "The player should be told they picked up the item"

def test_take_qty(capsys):
    # GIVEN: The current location and the items in the player's inventory
    adventure.PLAYER.place = 'shire'
    adventure.PLAYER.inventory = {}
    adventure.PLACES["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={'ring':10}
    )  
    adventure.ITEMS = {
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
    assert adventure.PLACES["shire"].inventory['ring'] == 7, \
        "the tooken item quantity should be decreased by 3 in the location's inventory"

    # AND: The item is added from the players inventory
    assert adventure.PLAYER.inventory['ring'] == 3, \
        "The tooken item quantity should be increased by 3 in player's inventory"

    # AND: The player is informed
    assert "You pick up 3 ring and put it in your bag." in output, \
        "The player should be told they took the item"

def test_take_invalid_qty(capsys):
    # GIVEN: The current location and the items in the player's inventory
    adventure.PLAYER.place = 'shire'
    adventure.PLAYER.inventory = {}
    adventure.PLACES["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={'ring':3}
    )  
    adventure.ITEMS = {
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
    assert adventure.PLACES["shire"].inventory['ring'] == 3, \
        "the tooken item quantity should be decreased by 3 in the location's inventory"

    # AND: The item is not added from the players inventory
    assert "ring" not in adventure.PLAYER.inventory.keys(), \
        "The invalid qty item should not be added to the player's inventory"

    # AND: The player is informed
    assert "Sorry, there are not 4 ring here" in output, \
        "The player should be told there are not enough"

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
    Inventory([]).do()
    output = capsys.readouterr().out

    # THEN: The inventory contents are displayed
    assert '(x 1) lockpicking tools' in output, "The player should be told the items their inventory"

    # AND: The inventory contents are displayed
    assert '(x 2) blunt knife' in output, "The player should be told the items their inventory"

def test_inventory_empty(capsys):
    # GIVEN: An empty player inventory
    adventure.PLAYER.inventory = {}

    # WHEN: The inventory is checked
    Inventory([]).do()
    output = capsys.readouterr().out

    # THEN: The player is told their inventory is empty
    assert 'empty' in output, "When the inventory is empty, the player should be told this"


@pytest.mark.parametrize(
    ["args", "expected"], [
    (['1','thing'],['thing',1]),
    (['thing','1'],['thing',1]),
    # note: this is not ideal, but works for now
    (['thing', '1', 'option'],['option', 'thing', 1]),
    (['2', 'thing', '1', 'option'],['option', 'thing', 2, 1]),
])

def test_order_args_qty(args, expected):
    # GIVEN: args consistenting of a string and qty in arbitrary order
    # THEN: The args are parsed correctly
    # Command(args).order_args_qty()

    cmd = Command(args)
    cmd.order_args_qty()

    assert cmd.args == expected
    # assert Command(args).order_args_qty() == expected

@pytest.mark.parametrize(
    ["a", "b", "expected"], [
    (1, 1, 2),
    (2, 2, 4),
])
def test_example(a, b, expected):
    assert a + b == expected


def test_drop_no_arg(capsys):
    # WHEN: The player calls Drop with no argument
    Drop([]).do()
    output = capsys.readouterr().out

    # Then an error is displayed to the player
    assert "Error: You cannot drop nothing.\n" in output, \
        "Passing no argument should throw an error"

def test_drop_no_item(capsys):
    # GIVEN: The items in the player's inventory
    adventure.PLAYER.inventory = {}

    # WHEN: The player tries to drop an item not in their inventory
    Drop(['ring']).do()
    output = capsys.readouterr().out

    # THEN: The player is told they do not have the item to drop
    assert "You dont have 1 ring to drop" in output, "The player cannot drop an item not in their inventory"

def test_drop_quantity_one(capsys):
    # GIVEN: The current location and the items in the player's inventory
    adventure.PLAYER.place = 'shire'
    adventure.PLAYER.inventory = {'ring':1}
    adventure.PLACES["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={}
    )
    
    # WHEN: The player tries to drop an item in their inventory
    Drop(['ring', 1]).do()
    output = capsys.readouterr().out

    # THEN: The item is removed from the players inventory
    assert 'ring' not in adventure.PLAYER.inventory, \
        "The dropped item should be removed from player's inventory"
    
    # AND: The item is added to the current location's inventory
    assert 'ring' in adventure.PLACES["shire"].inventory, \
        "the dropped item should be added to the current location inventory"

    # AND: The player is informed
    assert "You dropped 1 ring on the ground." in output, \
        "The player should be told they dropped the item"

def test_drop_qty(capsys):
    # GIVEN: The current location and the items in the player's inventory
    adventure.PLAYER.place = 'shire'
    adventure.PLAYER.inventory = {'ring':2}
    adventure.PLACES["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={'ring':1}
    )
    
    # WHEN: The player tries to drop an item in their inventory
    Drop(['ring', 1]).do()
    output = capsys.readouterr().out

    # THEN: The item is removed from the players inventory
    assert adventure.PLAYER.inventory['ring'] == 1, \
        "The dropped item quantity should be reduced by 1 in player's inventory"
    
    # AND: The item is added to the current location's inventory
    assert adventure.PLACES["shire"].inventory['ring'] == 2, \
        "the dropped item quantity should be increased by 1 in the location inventory"

    # AND: The player is informed
    assert "You dropped 1 ring on the ground." in output, \
        "The player should be told they dropped the item"

def test_drop_invalid_qty(capsys):
    # GIVEN: The current location and the items in the player's inventory
    adventure.PLAYER.place = 'shire'
    adventure.PLAYER.inventory = {'ring':2}
    adventure.PLACES["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={'ring':1}
    )
    
    # WHEN: The player tries to drop an item in their inventory
    Drop(['ring', 3]).do()
    output = capsys.readouterr().out

    # THEN: The item is not removed from the players inventory
    assert adventure.PLAYER.inventory['ring'] == 2, \
        "The invalid qty item should not be removed from the players's inventory"
    
    # AND: The item is not added to the current location's inventory
    assert adventure.PLACES["shire"].inventory['ring'] == 1, \
        "The invalid qty item should not be added to the location's inventory"

    # AND: The player is informed
    assert "You dont have 3 ring to drop." in output, \
        "The player should be told they do not have enough of the qty"

# TODO rename these tests, and add some versions of these tests for Item
def test_player_has_true():
    # GIVEN: The player's inventory
    adventure.PLAYER.inventory = {'ring':2}

    # WHEN: has_item() is called for an item/quantity the player possesses
    assert adventure.PLAYER.has_item('ring', 1), \
        "Should return True if the player has at least the specified qty"

def test_player_has_false():
    # GIVEN: The player's inventory
    adventure.PLAYER.inventory = {}

    # WHEN: has_item() is called for an item/quantity the player does not possess
    assert adventure.PLAYER.has_item('ring', 1) == False, \
        "Should return False if the player does not have the item"

def test_player_has_false_quantity():
    # GIVEN: The player's inventory
    adventure.PLAYER.inventory = {'ring':2}

    # WHEN: has_tiem() is called for an item/quantity the player does not possess
    assert adventure.PLAYER.has_item('ring', 3) == False, \
        "Should return False if the player does not have the specified qty"

def test_place_has_true():
    # GIVEN: A place with an inventory
    adventure.PLACES["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        inventory={'ring':2} 
    )

    # WHEN: has_item() is called for an item/quantity the place possesses
    assert adventure.PLACES["shire"].has_item('ring', 1) == True, \
        "Should return True if the place has at least the specified qty"

def test_place_has_false():
    # GIVEN: A place with an inventory
    adventure.PLACES["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        inventory={} 
    )

    # WHEN: has_item() is called for an item/quantity the place possesses
    assert adventure.PLACES["shire"].has_item('ring', 1) == False, \
        "Should return False if the place does not have the item"

def test_place_has_false_quantity():
    # GIVEN: A place with an inventory
    adventure.PLACES["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        inventory={'ring':1} 
    )

    # WHEN: has_item() is called for an item/quantity the place possesses
    assert adventure.PLACES["shire"].has_item('ring', 2) == False, \
        "Should return False if the place does not have the specified qty"

def test_is_for_sale():
    # GIVEN: An item with a price
    adventure.ITEMS = {
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
    assert adventure.ITEMS["lockpicks"].is_for_sale(), \
        "An item with a price should return True"
    
    # AND: An item without a price returns False
    assert not adventure.ITEMS["knife"].is_for_sale(), \
        "An item without a price should return False"

# TODO add more shop tests, this one only covers part of what determines if an item shows in the shop
def test_shop_can(capsys):
    # GIVEN: A place that can "shop" and has an inventory
    adventure.PLAYER.place = 'shire'
    adventure.PLACES["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        can=['shop'],
        inventory={'ring':1,
                   'stew':1, 
        } 
    )
    adventure.ITEMS = {
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

def test_shop_no_can(capsys):
    # GIVEN: A place that does not have can = ["shop"]
    adventure.PLAYER.place = 'shire'
    adventure.PLACES["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        inventory={'ring':1,
                   'stew':1, 
        } 
    )
    adventure.ITEMS = {
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

def test_buy_no_arg(capsys):
    adventure.PLAYER.place = 'shire'
    adventure.PLACES["shire"] = Place(
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

def test_buy_no_can(capsys):
    # GIVEN: A place that does not have can = ["shop"]
    adventure.PLAYER.place = 'shire'
    adventure.PLACES["shire"] = Place(
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

def test_buy_not_for_sale(capsys):
    # GIVEN: A place that can "shop" and has an inventory without a price
    adventure.PLAYER.place = 'shire'
    adventure.PLACES["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        can=['shop'],
        inventory={'ring':1,
        } 
    )
    adventure.ITEMS = {
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

def test_buy_for_sale(capsys):
    # GIVEN: A place that can "shop" and has an inventory with a price
    adventure.PLAYER.place = 'shire'
    adventure.PLACES["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        can=['shop'],
        inventory={'stew':1, 
        } 
    )
    adventure.ITEMS = {
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

def test_buy_no_money(capsys):
    # GIVEN: A place that can "shop" and has an inventory with a price, and a poor player
    adventure.PLAYER.place = 'shire'
    adventure.PLAYER.inventory = {'gems':1}
    adventure.PLACES["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        can=['shop'],
        inventory={'stew':1, 
        } 
    )
    adventure.ITEMS = {
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

def test_buy_no_qty(capsys):
    # GIVEN: A place that can "shop" and has a single item with a price, and a moneyed player
    adventure.PLAYER.place = 'shire'
    adventure.PLAYER.inventory = {'gems':50}
    adventure.PLACES["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        can=['shop'],
        inventory={'stew':1, 
        } 
    )
    adventure.ITEMS = {
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
    assert 'stew' in adventure.PLAYER.inventory, "The bought item should be in the player's inventory"

    # AND: the item is removed from the place
    assert 'stew' not in adventure.PLACES["shire"].inventory, "the bought item should no longer be at the place"

    # AND: The player's gems are reduced by the cost of the item
    assert adventure.PLAYER.inventory['gems'] == 40, "The place's gems should be increased by the cost of the item"

    # AND: The place's gems are increased by the cost of the item
    assert adventure.PLACES["shire"].inventory['gems'] == 10, "The players gems should be reduced by the cost of the item"

    # AND: the player is informed
    assert "You bought 1 Rabbit Stew for 10 gems" in output, "The player should be told they have bought the item"

def test_buy_invalid_qty(capsys):
    # GIVEN: A place that can "shop" and has a multiple items with a price, and a moneyed player
    adventure.PLAYER.place = 'shire'
    adventure.PLAYER.inventory = {'gems':50}
    adventure.PLACES["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        can=['shop'],
        inventory={'stew':2, 
        } 
    )
    adventure.ITEMS = {
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
    assert 'stew' not in adventure.PLAYER.inventory.keys(), "The invalid qty purchase should not be in the player's inventory"

    # AND: the location's item qty should not change
    assert adventure.PLACES["shire"].inventory['stew'] == 2, "The invalid qty purchase attempt should not change the location inv"

    # AND: The player's gems should not change
    assert adventure.PLAYER.inventory['gems'] == 50, "The invalid qty purchase should not change the player's gems"

    # AND: The place's gems are increased by the cost of the item
    assert 'gems' not in adventure.PLACES["shire"].inventory.keys(), "The invalid qty purchase should not change the place's gems"

    # AND: the player is informed
    assert "Sorry, there are not 3 Rabbit Stew here." in output, "The player should be told the location does not have the requested qty"

def test_buy_qty(capsys):
    # GIVEN: A place that can "shop" and has a multiple items with a price, and a moneyed player
    adventure.PLAYER.place = 'shire'
    adventure.PLAYER.inventory = {'gems':50}
    adventure.PLACES["shire"] = Place(
        key="shire",
        name="The Shire",
        description="Buncha hobbits.",
        can=['shop'],
        inventory={'stew':5, 
        } 
    )
    adventure.ITEMS = {
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
    assert adventure.PLAYER.inventory['stew'] == 3, "The bought item qty should be in the player's inventory"

    # AND: the item is removed from the place
    assert adventure.PLACES["shire"].inventory['stew'] == 2, "the bought item qty should be removed from the place"

    # AND: The player's gems are reduced by the cost of the item
    assert adventure.PLAYER.inventory['gems'] == 20, "The players gems should be reduced by the cost of the items"

    # AND: The place's gems are increased by the cost of the item
    assert adventure.PLACES["shire"].inventory['gems'] == 30, "The place's gems should be increased by the cost of the items"

    # AND: the player is informed
    assert "You bought 3 Rabbit Stew" in output, "The player should be told they have bought the item"

def test_read_no_arg(capsys):
    # WHEN: The player calls read with no argument
    Read([]).do()
    output = capsys.readouterr().out

    # Then an error is displayed to the player
    assert "Error: You cannot read nothing.\n" in output, \
        "Passing no argument should throw an error"

def test_read_no_item(capsys):
    # GIVEN: a location and player inventory
    adventure.PLAYER.place = 'shire'
    adventure.PLAYER.inventory = {}
    adventure.PLACES["shire"] = Place(
            key="shire",
            name="The Shire",
            description="Buncha hobbits.",
            inventory={}
        )

    # WHEN: the player tries to read an item that is not present
    Read(['magazine']).do()
    output = capsys.readouterr().out
    
    # THEN: the plater is told the item is not present
    assert "There is no magazine here." in output, \
        "The player should be told the desired item is not present"

def test_read_no_writing():
    ...

def test_read():
    ...

def test_read_formatting():
    # you might not need this, and instead could update the test_wrap() function
    ...

# shlex.split('abc 123') == ['abc', '123']
# shlex.split('abc "xyz blah"') == ['abc', 'xyz blah']