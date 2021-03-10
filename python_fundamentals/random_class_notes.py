#dictionary/library examples:

inventory = [ "shoe", "shirt" ]
print(inventory[0]) # shoe
print(inventory[1]) # shirt

favs = {
  'color': "purple",
  'season': "fall"
}

print(favs['color'])

player_inventory = {}

info = player_inventory["horse"]
info["cost"]

player_inventory["horse"]["cost"]

#add'level up example:

def add(num1, num2):
    result = num1 + num2
    print(f"{num1} + {num2} = {result}")
    return result


add(2, 3)   # will print out "2 + 3 = 5"

newnum = add(2, 3)
newnum = add(2, 3) * 3

# string concatonation
"string one " + "string two"  # = "string one string two"

# print will concatonate all arguments with spaces between
print("string one", "string two")  # prints "string one string two"

# f-string -- string interpolation
string1 = "string one"
string2 = "string two"
f"{string1} {string2}"

"hello my name is __ and my age is __"



# 12/14

if False:
  print("this never happens!")

if True:
  ...
  print("yes")

# conditional operators

something, something_else = "", ""

a, b, c = 1, 2, 3

if something == something_else:
  ...

print("The boolean value of", repr(something), "is", bool(something))

if something:
  print("something is Truthy")
else:
  print("something is Falsy")


while not something:
    something = input("say something: ")
    print("something is a", type(something), "with a value of", repr(something), "and it is", bool(something))