print('Welome to Pypet!')

cat = {
    'name': 'Fluffy',
    'hungry': True,
    'weight': 9.5,
    'age': 5,
    'photo': '(=^o.o^=)__',
}

mouse = {
    'name': 'Mouse',
    'age': 6,
    'weight': 1.5,
    'hungry': True,
    'photo': '<:3 )~~~~',
}

pets = [cat, mouse]

def feed(pet):
    if pet['hungry'] == True:
        pet['hungry'] = False
        pet['weight'] = pet['weight'] + 1
    else:
        print('The Pypet is not hungry!')

for pet in pets:
    feed(pet)
    print(pet)