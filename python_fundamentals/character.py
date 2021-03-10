import random

def character_info(character_name, character_level, character_title):
    print(f"{character_name} is a level {character_level} {check_rank(character_level)} {character_title}.")

def check_level(character_name, character_level, character_title):
    print(f"{character_name} is now a level {character_level} {check_rank(character_level)} {character_title}.")

def check_rank(level_check):
    if level_check <= 3:
        character_rank = "novice"
    elif level_check <= 7:
        character_rank = "intermediate"
    elif level_check > 7:
        character_rank = "bomb-ass"
    return character_rank

def add_level(character_level, num):
    temp_level = character_level + num
    if temp_level >= 10:
        return 10
    else:
        return temp_level

name = 'Gunther'
level = random.randint(1,5)
title = 'wizard'

character_info(name, level, title)

level = add_level(level, random.randint(1,5))

check_level(name, level, title)

level = add_level(level, random.randint(1,5))

check_level(name, level, title)