fluffy = {
    "is_hungry": True,
    "weight": 3,
    "name": "Fluffy",
}

def feed_pet(pet):
    pet["weight"] += 1
    pet["is_hungry"] = False

    
feed_pet(fluffy)


class Pet():
    attrs = {
        "is_hungry": True,
        "weight": None,
        "name": "",
    }
    def __init__(self, **kwargs):
        # set all attributes included in Pet.attrs
        # raise if unknown kwargs
        for k, v in kwargs.items():
            if k not in self.attrs:
                raise Exception(f"No such keyword argument for a Pet object: {k}")

            setattr(self, k, v)

        # set default values based on kwargs
        for k, v in self.attrs.items():
            if k not in self.__dict__:
                setattr(self, k, v)

    def feed(self):
        self.weight += 1
        self.is_hungry = False