# text = format(" Sunday", "d>30s")
# print(text)





# 1

num = 48.7052

print(f"#1:\n{num:.2f}\n")

# 2

num = 2.5

print(f"#2:\n{num:.2f}\n")

# 3

num = .25

print(f"#3:\n{num:.0%}\n")

# 4

num = "September"

print(f"#4:\n{num:.3}\n")

# 5

num = "Game Over"

print(f"#5:\n{num:^80}\n")

# 6

num = "8 of 10"

print(f"#6:\n{num:>80}\n")

# 7

num = "Question"

print(f"#7:\n{num:=<30}\n")

exercises = [
    (6, "8 of 10", "{:>80}"),
    (7, "Question", "{:=<30}"),
]

for num, val, fmt in exercises:
    print(f"#{num}\n", fmt.format(val), "\n\n")