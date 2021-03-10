'''numbers = [2, 1, 3, 4, 7]
more_numbers = [*numbers, 11, 18]
print(*more_numbers, sep=', ')
'''

'''
guessed = ['a','o']
word = "potato"



def remaining_letters():
    counter = len(word)
    i = 0

    while i < len(guessed):
        counter -= word.count(guessed[i])
        i += 1

    print(counter)

remaining_letters()


def test_is_palindrome():
    assert is_palindrome('racecar'), "racecar is a palindrome"
    assert not is_palindrome('screwdriver'), "screwdriver is not a palindrome" 
'''


# float("")


blah = {1,5,6,8,2}


def blah_da(nums):
    for da in nums:
        return da
    return nums


print(blah_da(blah))

# second = flavors[i+1:-1]
# import string
# letters = list(string.ascii_lowercase)

test_t = True

test_f = False

print(type(test_t))

print(type(test_f))