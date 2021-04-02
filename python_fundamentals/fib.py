from functools import lru_cache
import datetime

@lru_cache(maxsize=5)
def fib1(n):
    if n <= 1:
        return n
    return fib1(n-1) + fib1(n-2)

def main1():
    a = datetime.datetime.now()
    for i in range(400):
        print(i, fib1(i))
    b = datetime.datetime.now()
    print(f"--done1--: {b-a}")


seq = []

def fib2(n):
    if n <= 1:
        seq.append(n)
        return n
    new_num = seq[n-1] + seq[n-2]
    seq.append(new_num)
    return new_num

def main2():
    a = datetime.datetime.now()
    for i in range(400):
        print(i, fib2(i))
    b = datetime.datetime.now()
    print(f"--done2--: {b-a}")

if __name__ == '__main__':
    main1()
    main2()