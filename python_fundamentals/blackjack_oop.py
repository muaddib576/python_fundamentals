'''
- make a Card class that takes a face and suit in its constructor
- suits are: D, H, C and S
- faces are: 2-9 and T, J, K, A
- when converted to a string using str(), it should print the two characters
    representing its face and suit. ie: "TS"
- when converted to a string using repr(), it should show the code to make
    that object, ,ie: Card("T", "S")
- define a __eq__ method that will determine if two cards are equal. In
    addition to self, it should take one argument, other, which represents the
    other card object.
- write pytest tests to ensure that things work as expected

Homework:
- write an __lt__ method which compares Card objects based on the cards value
- finish the test_repr function
'''

from random import choice

class Card:
    SUITS = ('D','H','C','S')
    FACES = ('A','2','3','4','5','6','7','8','9','T','J','Q','K')
    COLORS = {'D': 'red', 'H': 'red', 'C': 'black', 'S': 'black'}
    
    def __init__(self, face, suit):
        if face not in self.__class__.FACES:
            raise ValueError(f"Not a valid face: {face!r}")

        if suit not in self.__class__.SUITS:
            raise ValueError(f"Not a valid suit: {suit!r}")
        
        self.face = face
        self.suit = suit
        # self.color = self.COLORS[self.suit]

    def __str__(self):
        return f"{self.face}{self.suit}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}('{self.face}', '{self.suit}')>"

    def __eq__(self, other_card):
        if str(self) == str(other_card):
            return True
        else:
            return False

    @property
    def color(self):
        """Return the color ("red" or "black") of the card depending on the
           suit."""
        return self.COLORS[self.suit]
        
    @property
    def value(self):
        """Return the numeric value of the card's face"""
        return self.FACES.index(self.face) + 1

if __name__ == "__main__":
    card1 = Card(
        suit = choice(Card.SUITS),
        face = choice(Card.FACES)
    )

    card2 = Card(
        suit = choice(Card.SUITS),
        face = choice(Card.FACES)
    )

    card3 = Card(suit="H", face="X")

    print(str(card1))
    print(card1.__eq__(card2))
    print(repr(card1))