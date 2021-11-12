from functools import reduce

#3.2 Exercise

letters = ["c","u","r","l","i","c","u","e"]

word = ""

for i in letters:
    word += i

print(word)

# -------------------

def concat(res, cur):
    res += cur
    return res

word = reduce(concat, letters)

print(word)

# I see now from your example that I could have used the add function... woops


# 3.3 Exercise

vowel_count = reduce(
                    lambda res, cur: res + int(cur.lower() in "aeiou"),
                    word,
                    int()
            )

print(vowel_count)


# Challenge: Fibonacci

# fib = reduce(
#             lambda res, cur:
#         )


# Challenge: Hex

rgb = (231, 5, 0)

# print(f"{rgb[0]:x}")

hex = reduce(
            lambda res, cur: res + f"{cur:0>2x}",
            rgb,
            ""
        )

print(hex)