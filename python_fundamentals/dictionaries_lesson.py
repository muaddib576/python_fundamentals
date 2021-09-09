def shape_dictionary_ex():
    shapes = {
        "triangle": 3,
        "square": 3,
        "pentagon": 5,
        "hexagon": 6,
    }

# lookup sides excercise
    # print(f"A triangle has {shapes['triangle']} sides.")
    # print(f"A square has {shapes['square']} sides.")

# w/ fallback excercise
    # selection = input("Name a shape: ").lower()

    # selection_side = shapes.get(selection, -1)

    # if selection_side >= 0:
    #     print(f"A {selection} has {selection_side} side(s).")
    # else:
    #     print(f"Sorry, I don't know the shape: {selection}")

# add and change excercise
    # print(shapes)
    # shapes.update({"oval": 0, "square": 4})
    # print(shapes)

# add and change multi excercise
    shapes.update({"triangle": "three", "star": 10, "nonagon": 9})
    print(shapes)

shape_dictionary_ex()