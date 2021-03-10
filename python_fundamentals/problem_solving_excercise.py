
# Dictionary to define letter grade thresholds
    # ignore ones place and just goes by tens to make the check simpler? (eg 9+ = A, 8 = B, etc)
    # + / - can be appended later in function

grade_thresholds = {9 : "A",
                    8 : "B",
                    7 : "C",
                    6 : "D",
                    5 : "F"
                    }


def get_letter(number):
    """Returns a letter based on the tens place of the number"""
    tens_place = int(number/10)
    
    if tens_place < 5:
        return "F"
    elif tens_place > 9:
        return "A"
    else:
        return grade_thresholds[tens_place]

def get_symbol(number, grade):
    """Returns a "+" or a "-" based on the ones place of the number"""
    #remember int() removes decimals so this is not as stupid as it looks
    ones_place = number - (int(number/10)*10)
    
    if ones_place > 6 and grade != "A" and grade != "F":
        return "+"
    elif ones_place < 4 and grade != "F" and number < 100:
        return "-"
    else:
        return ""

def letter_grade(number):
    """Returns a letter grade depending on a given number"""

    # check which range the given number falls into
    # get the appropriate letter from the letter grade ranges based on the tens place of the number
    grade = get_letter(number)
    
    # append a "+"" or a "-" to the letter based on the the ones place of the number
    symbol = get_symbol(number, grade)

    grade += symbol
    print(grade)
    # print the appropriate letter grade
    return grade


def test_letter_grade():
    assert letter_grade(85) == "B", "85 is B"
    assert letter_grade(61) == "D-", "60 is D-"
    assert letter_grade(79) == "C+", "79 is C+"
    assert letter_grade(59) == "F", "59 is F"
    assert letter_grade(31) == "F", "31 is F"
    assert letter_grade(5) == "F", "5 is F"
    assert letter_grade(99) == "A", "99 is A"
    assert letter_grade(100) == "A", "100 is A"
    assert letter_grade(120) == "A", "120 is A"

# def test_get_tens():
#     assert get_tens(85) == 8, "Should be 8"
#     assert get_tens(61) == 6, "Should be 6"

# def test_get_ones():
#     assert get_ones(85) == 5, "Should be 5"
#     assert get_ones(61) == 1, "Should be 1"

test_letter_grade()
# test_get_tens()
# test_get_ones()



# questions: better to alter dictionary or account for outlier in functuon
