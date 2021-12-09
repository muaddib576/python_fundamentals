"""
2021-12-08 Data & In-Depth -- Aggregate builtin functions

Attendees
---------
- Fiona
- Brian

Exercises
---------

1. Assign your name (capitalized) to the variable text and find out what the "minimum" letter is.
2. Find out the maximum length of a list of strings.
   ie: ["title", "author", "year"]
3. Write a function valid_row that checks if no fields in a csv row are blank.
   - valid_row should take one argument, line, a string
   - in the function:
    * split line on the comma delimiter
    * if all of the values are truthy, print "Valid" and return True
    * otherwise print "Error" and return False
   - test with the following arguments:
    * "a,b,c"
    * "x,,z"
"""


def min_let():
    text = "Brian"

    print(text, min(text))

    text = text.lower()

    print(text, min(text))

# min_let()

def max_str():
    strings = ["title", "author", "year", "book", "dragon"]
    string_length = []
    
    for x in strings:
        string_length.append(len(x))

    max_len = max(string_length)
    max_strings = []

    for x in strings:
        if len(x) == max_len:
            max_strings.append(x)

    print(max_len, max_strings)


def max_str():
    strings = ["title", "author", "year", "book", "dragon"]

    str_lengths = [len(x) for x in strings]
    max_len = max(str_lengths)

    max_strings = [x for x in strings if len(x) == max_len]

    print(max_len, max_strings)


max_str()


def valid_row(line):
    pass




test1 = "a,b,c"
test2 = "x,,z"