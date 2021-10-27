class Car():
    def __init__(self, make, model, color, year, is_clean=False):
        self.make = make
        self.model = model
        self.color = color
        self.year = year
        self.is_clean = is_clean

    def wash(self):
        print(f"Washing the {self.year} {self.make.title()} {self.model.title()}")
        self.is_clean = True

car = Car(
    make='chevrolet',
    model='malibu',
    color='ugly',
    year=1999,
)

truck = Car(
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

print(car.is_clean, truck.is_clean)