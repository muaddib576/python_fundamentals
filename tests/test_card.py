import pytest
from python_fundamentals.blackjack_oop import Card

def test_card():
    test_card = Card(
        suit = 'D',
        face = '7'
    )

    # assert syntax
    # assert CONDITION [, MESSAGE]
    # assert 1 == 3.0
    # assert 1 == 2.0, "1 should be equal to 2.0"

    assert str(test_card) == '7D', "Converting to string should return '7D'"

def test_invalid_card():

    # with pytest.raises(EXCEPTION_CLASS): 
        # code that would raise

    with pytest.raises(ValueError):

        invalid_card = Card(
            suit = 'D',
            face = '10'        
        )

    with pytest.raises(ValueError):

        invalid_card = Card(
            suit = 'X',
            face = '7'        
        )


def test_eq():

    test_card1 = Card(
        suit = 'D',
        face = '7'
    )

    test_card2 = Card(
        suit = 'D',
        face = '7'
    )

    assert test_card1.__eq__(test_card2), "Two 7D cards should be equal"
    assert test_card1 == test_card2, "Two 7D cards should be equal"

def test_not_eq():

    test_card1 = Card(
        suit = 'H',
        face = '4'
    )

    test_card2 = Card(
        suit = 'D',
        face = '7'
    )

    assert not test_card1.__eq__(test_card2), "4H and 7D should not be equal"
    assert test_card1 != test_card2, "4H and 7D should not be equal"

def test_color():
    card = Card(suit="H", face="8")
    assert card.color == "red"

    card.suit = "S"
    assert card.color == "black"

def test_value():
    card = Card(suit='H', face='2')
    card2 = Card(suit='H', face='Q')
    assert card.value == 2, "the value of a 2 card should be 2"
    assert card2.value == 12, "the value of Queen should be 12"


@pytest.mark.skip(reason="todo")
def test_repr():
    ...
# print(repr(card1))