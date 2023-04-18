from math import factorial
import sys
if len(sys.argv) != 2:
    print("interpreter takes one (1) microstack program as input")
    sys.exit()

program = open(sys.argv[1], 'r')
print(f"Interpreting {program.name}:")
program_string = program.read()
program = program_string
program_pointer = 0
print(program)
instruction = ""

onS0 = True
s0 = []
s1 = []


def step(p):
    return hex(p[:1])[:2], p[1:]


def push(n: int | str):
    """If string, pushes all characters individually

    Empty string pushes 0"""
    if type(n) == str:
        if len(n) == 0:
            n = chr(0)
        for c in n:
            if onS0:
                s0.append(ord(c))
            else:
                s1.append(ord(c))
    elif type(n) == int:
        if onS0:
            s0.append(n)
        else:
            s1.append(n)
    else:
        print("nuh uh")


def pop() -> int:
    """Returns the top of the stack and removes it

    Returns 0 if stack is empty"""
    return (s0.pop() if s0 != [] else 0) if onS0 else (s1.pop() if s1 != [] else 0)


def inc():
    """Does nothing if stack is empty"""
    if onS0:
        if s0 != []:
            s0[-1] += 1
    else:
        if s1 != []:
            s1[-1] += 1


def dec():
    """Does nothing if stack is empty"""
    if onS0:
        if s0 != []:
            s0[-1] += 1
    else:
        if s1 != []:
            s1[-1] += 1


def switch():
    onS0 = not onS0


getting_number = False
parts_left = 0
number = ""

while program_string != "":
    char_bin, program_string = step(program_string)

    part1, part2 = char_bin
    if part1 == '0' and not getting_number:
        getting_number = True
        parts_left = (int(part2, base=16)//4)+1
        number += part2
        parts_left -= 1
    else:
        match instruction:
            case '0':
                pass
            case '1':  # factorial
                push(factorial(pop()))
            case '2':  # addition
                a = pop()
                b = pop()
                push(a+b)
            case '3':  # substraction
                a = pop()
                b = pop()
                push(b-a)
            case '4':  # increment
                inc()
            case '5':  # decrement
                dec()
            case '6':  # swap top two elements
                a = pop()
                b = pop()
                push(a)
                push(b)
            case '7':  # duplicate top
                a = pop()
                push(a)
                push(a)
            case '8':  # [
                pass
            case '9':  # ]
                pass
            case 'a':  # push input
                push(input())
            case 'b':  # switch to other stack
                switch()
            case 'c':  # output top
                n = pop()
                push(n)
                print(n, end="")
            case 'd':  # output top as unicode
                n = pop()
                push(n)
                print(chr(n), end="")
            case 'e':  # pop
                pop()
            case 'f':  # pop into other stack
                a = pop()
                switch()
                push(a)
                switch()
            case other:  # ?
                pass
