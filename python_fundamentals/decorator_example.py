class Shape():
    """Way #1: do setup stuff in init"""
    shape_names = {
        0: "circle",
        3: "triangle",
        4: "square",
    }

    def __init__(self, sides):
        self.sides = sides
        
        if sides not in self.shape_names:
            name = None
        else:
            self.name = self.shape_names[self.sides]


class Shape():
    """Way #2: make a setup function"""
    shape_names = {
        0: "circle",
        3: "triangle",
        4: "square",
    }

    def __init__(self, sides):
        self.sides = sides
        self.setup_name()
        
    def setup_name(self):
        if self.sides not in self.shape_names:
            name = None
        else:
            self.name = self.shape_names[self.sides]


class Shape():
    """Way #3: Use properties instead"""
    shape_names = {
        0: "circle",
        3: "triangle",
        4: "square",
    }

    def __init__(self, sides):
        self.sides = sides
        
    @property
    def name(self):
        if self.sides not in self.shape_names:
            return None
        else:
            return self.shape_names[self.sides]

class Shape():
    """Way #4: Use a property setter"""
    shape_names = {
        0: "circle",
        2: "line",
        3: "triangle",
        4: "square",
    }

    def __init__(self, sides):
        self.sides = sides
        
    @property
    def sides(self):
        """Called on shape.sides"""
        if "_sides" not in self.__dict__:
            self._sides = None

        return self._sides
    
    #
    @sides.setter
    def sides(self, value):
        """Called on self.sides = value"""
        self._sides = value

        if self._sides not in self.shape_names:
            self.name = None
            self.is_valid = False
        else:
            self.name = self.shape_names[self._sides]
            self.is_valid = True

        
triangle = Shape(3)
print(triangle.sides, triangle.name)

rectangle = Shape(4)
rectangle.name = "rectangle"
rectangle.is_valid = False
print(rectangle.sides, rectangle.name, rectangle.is_valid)

octagon = Shape(8)
octagon.is_parallel = True
print(octagon.sides, octagon.name, octagon.is_paralle)