""""Example of multiple inheritance"""

class Animal:
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    def roar(self):
        if not self.can_roar:
            raise NotImplementedError("roar not available for this animal")

        print(f"{self.name} says GRrrrr")
    
class Roaring:
    def roar(self):
        print(f"{self.name} says GRrrrr")

class Climbing:
    def climb(self, structure):
        print(f"{self.name} climbs the {structure}.")
        
class Pettable:
    def pet(self):
        print(f"You pet {self.name}.")

        
class Dog(Animal, Pettable):
    ...
    
class Cat(Animal, Pettable, Climbing):
    ...
    
class Lion(Animal, Climbing, Roaring):
    ...

simba = Lion(name="Simba")
mocha = Dog(name="Mocha")
cinder = Cat(name="Cinder")

cinder.climb("bookshelf")
simba.roar()
mocha.pet()