from random import randint

######################################################
# lambdas
######################################################

def rand(upto=100):
    return randint(1, upto)

rand = lambda upto=100: randint(1, upto)

doit = lambda x, y: x+y

print(rand(10))
print(rand())

text = "  hello world!"

title_string = lambda string: string.title().strip()

print(title_string(text))

number_list = lambda x,y: list(range(x,y))

print(number_list(1,5))

######################################################
# list comprehensions for mapping
######################################################

text = "hello world!"

codepoints = []

for char in text:
    codepoints.append(ord(char))

print(codepoints)

codepoints = [ord(char) for char in text]

words = ['restore', 'pile', 'writer', 'trial', 'former', 'tape', 'stay']

word_lengths = [len(x) for x in words]

print(word_lengths)

######################################################
# map()
######################################################

word_lengths = list(map(len, words))

print(word_lengths)

types = list(map(type, word_lengths))

print(types)

######################################################
# list comprehensions for filtering
######################################################

lower = []

text = "Something Here"

for char in text:
    if char.islower():
        lower.append(ord(char))

print(lower)

lower = [ord(x) for x in text if ord(x) >= 97]

print(lower)

small_words = [x for x in words if len(x) < 6]

print(small_words)

######################################################
# filter() to remove falsy values
######################################################

print("="*60)

# generate a list of 10 numbers between 0 and 2
nums = [randint(0, 2) for _ in range(10)]

print(nums)

# filter to just the ones over zero
gtz = []

for num in nums:
    if num:
        gtz.append(num)

print(gtz)

# same thing with a comprehension
gtz = [num for num in nums if num]

print(gtz)

# same thing using filter()

gtz = list(filter(None, nums))

######################################################
# filter() using a callable
######################################################

nums = [randint(1, 100) for _ in range(10)]

print(nums)

high_nums = [x for x in nums if x > 50]

print(high_nums)

def keeper(x):
    return x > 50

high_nums = filter(keeper, nums)

print(list(high_nums))

######################################################
# set comprehension
######################################################

nums = {randint(1, 100) for _ in range(10)}

print(f"there are {len(nums)} unique numbers: {nums}")

text = "some kind of sentence."

text_set = {x for x in text if x.isalpha()}

print(f"this is the unique aplha chars: {text_set}")

######################################################
# dict comprehensions
######################################################

from string import ascii_uppercase
from pprint import pprint

# {key: value for var in iter}
letters = {i: c for i, c in enumerate(ascii_uppercase, 1)}

pprint(letters)

word_dict = {x: len(x) for x in words}

pprint(word_dict)