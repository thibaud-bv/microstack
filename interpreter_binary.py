import sys
if len(sys.argv) != 2:
    print("interpreter takes one (1) microstack program as input")
    sys.exit()

program = open(sys.argv[1], 'r')
print(f"Interpreting {program.name}:")
program_string = program.read()
program = program_string
print(program)
instruction = ""

s = []


def step(p):
    return p[:4], p[4:]


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


while program_string != "":
    instruction, program_string = step(program_string)
    match instruction:
        case "0000":
            length, program_string = step(program_string)
            number = ""
            for _ in range((int(length, base=2)//4)+1):
                bits, program_string = step(program_string)
                number += bits
            push(int(number, base=2))
        case "0001":
            pass
        case "0010":
            a = s.pop()
            b = s.pop()
            push(a+b)
        case "0011":
            a = s.pop()
            b = s.pop()
            push(b-a)
        case "0100":
            a = s.pop()
            b = s.pop()
            push(a*b)
        case "0101":
            a = s.pop()
            b = s.pop()
            push(b//a)
        case "0110":
            a = s.pop()
            b = s.pop()
            push(a)
            push(b)
        case "0111":
            a = s.pop()
            push(a)
            push(a)
        case "1000":
            pass
        case "1001":
            pass
        case "1010":
            pass
        case "1011":
            pass
        case "1100":
            n = outpopint()
            push(n)
        case "1101":
            n = outpopuni()
            push(n)
        case "1110":
            outpopint()
        case "1111":
            outpopuni()
        case other:
            pass
