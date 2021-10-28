
class Thing:
    stuff_to_do = "things!"

    def __init__(self):
        self.x = 1

    @classmethod
    def do_stuff(cls):
        # print(cls.x)   # this breaks
        print(f"doin' some stuff: {cls.stuff_to_do}")

Thing.do_stuff()
thing = Thing()
thing.do_stuff()

class Vehicle():

    # doors = 4
    # features = []

    def __init__(self, make, model, color, year, is_clean=False, features=None, is_loaded=False):
        self.make = make
        self.model = model
        self.color = color
        self.year = year
        self.is_clean = is_clean

        if not features:
            features = []

        self.features = features
        self.is_loaded = is_loaded

    def wash(self):
        print(f"Washing the {self.year} {self.make.title()} {self.model.title()}")
        self.is_clean = True

    def load(self):
        self.is_loaded = True

class Car(Vehicle):
    doors = 4

    def load(self, stuff):
        super().load()
        print(f"The {stuff} is in the trunk.")

class Truck(Vehicle):
    doors = 2

    def load(self, stuff):
        super().load()
        print(f"The {stuff} is in the flatbed.")

car = Car(
    make='chevrolet',
    model='malibu',
    color='ugly',
    year=1999,
)

truck = Truck(
    make='chevrolet',
    model='silverado',
    color='gold',
    year=1995,
    is_clean=True,
)

# print(car.color , car.year, car.make, car.model)
# print(car.is_clean)
# print(truck.color , truck.year, truck.make, truck.model, truck.is_clean)

car.wash()
truck.wash()

# print(car.is_clean, truck.is_clean)

# print(Car.doors, car.doors, truck.doors)

car.features.append("big ol wheels")
car.features.append("subwoofer")
car.features.append("boat mode")

print(car.is_loaded)
print(truck.is_loaded)

car.load("body")
truck.load("rake")

print(car.is_loaded)
print(truck.is_loaded)