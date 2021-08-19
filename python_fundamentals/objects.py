import random
from pprint import pprint

def ex_38():
    nums = []

    while len(nums) < 6:
        nums.append(random.randint(1,49))
        nums = list(set(nums))

    return nums

if __name__ == "__main__":
    ex_38()


def mult_table():
    table = []

    for y in range(1,10):
        row = []

        for x in range(1,10):
            row.append(x*y)
        
        table.append(row)

    pprint(table)

mult_table()

