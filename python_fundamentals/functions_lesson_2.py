"1.2 Exercise"

# def write(message, before=0, after=0):
#     print("\n"*before, end="")
#     print(message)
#     print("\n"*after, end="")
#     print("----")

# write("testing",3,4)
# write("testing",before=4)
# write("testing",after=8)
# write("testing")

"2.1 Exercise"

# def write(*args, before=0, after=0):
    
#     args_str = ""
#     for arg in args:
#         args_str += f"{str(arg)} "
    
#     args_str = args_str.strip()
    
#     print("\n"*before, end="")
#     print(args_str)
#     print("\n"*after, end="")
#     print("----")

# write("testing",123,before=3,after=4)
# write("testing",before=4)
# write("testing",after=8)
# write("testing")

"2.2 Exercise"

# def write(*args, before=0, after=0, **kwarg):
    
#     args_list = [str(x) for x in args]

#     args_list += [f"{k}={v}" for k,v in kwarg.items()]

#     args_str = " ".join(args_list)
    
#     print("\n"*before, end="")
#     print(args_str)
#     print("\n"*after, end="")
#     print("----")

# write("testing",123,before=3,after=4, a=1, b=2, up="down")
# write("testing",before=4)
# write("testing",after=8)
# write("testing")

"3.1 Excercise"

cities = ['san francisco','austin','concord','merced']

# def print_cities(*args):
    
#     city_list = [str(x) for x in args]
    
#     city_str= ", ".join(city_list)

#     print(f"Places I have been: {city_str}")

# print_cities(*cities)

"3.2 Excercise"

options = {
    "sep" : ", ",
    "end" : " ",
}

print("Cities I have been:", *cities, **options)