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

s = []
s2 = []


def step(p):
    return hex(p[:1])[:2], p[1:]


def push(n):
    s.append(n)


def outpopint():
    n = s.pop() if s != [] else 0
    print(n, end='')
    return int(n)


def outpopuni():
    n = s.pop() if s != [] else 0
    print(chr(n), end='')
    return int(n)


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
            case '1':
                pass
            case '2':
                a = s.pop()
                b = s.pop()
                push(a+b)
            case '3':
                a = s.pop()
                b = s.pop()
                push(b-a)
            case '4':
                a = s.pop()
                b = s.pop()
                push(a*b)
            case '5':
                a = s.pop()
                b = s.pop()
                push(b//a)
            case '6':
                a = s.pop()
                b = s.pop()
                push(a)
                push(b)
            case '7':
                a = s.pop()
                push(a)
                push(a)
            case '8':
                pass
            case '9':
                pass
            case 'a':
                pass
            case 'b':
                pass
            case 'c':
                n = outpopint()
                push(n)
            case 'd':
                n = outpopuni()
                push(n)
            case 'e':
                outpopint()
            case 'f':
                outpopuni()
            case other:
                print('1')
