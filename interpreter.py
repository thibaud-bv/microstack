from math import factorial
import sys


class Interpreter:

    def __init__(self) -> None:
        self.l_stack = []
        self.r_stack = []
        self.onLeft = True
        self.program_pointer = 0
        self.hex_program = ""

    def push(self, n: int | str):
        """If only composed of digits, pushes the number,
         else pushes all characters individually.

        Empty string pushes 0"""
        if type(n) == str:
            if len(n) == 0:
                n = chr(0)
            if n.isdecimal():
                if self.onLeft:
                    self.l_stack.append(int(n))
                else:
                    self.r_stack.append(int(n))
            else :
                for c in n:
                    if self.onLeft:
                        self.l_stack.append(ord(c))
                    else:
                        self.r_stack.append(ord(c))
        elif type(n) == int:
            if self.onLeft:
                self.l_stack.append(n)
            else:
                self.r_stack.append(n)
        else:
            print("nuh uh")

    def hexify(self, ascii_program: str) -> str:
        hexed_program = ""
        for c in ascii_program:
            hex_c = hex(ord(c))[2:]
            if len(hex_c) <= 2:
                (2-len(hex_c))*'0'+hex_c
                hexed_program += hex_c
        return hexed_program

    def pop(self) -> int:
        """Returns the top of the stack and removes it

        Returns 0 if stack is empty"""
        return (self.l_stack.pop() if self.l_stack != [] else 0) if self.onLeft else (self.r_stack.pop() if self.r_stack != [] else 0)

    def peek(self) -> int:
        """Returns the top of the stack

        Returns 0 if stack is empty"""
        return (self.l_stack[-1] if self.l_stack != [] else 0) if self.onLeft else (self.r_stack[-1] if self.r_stack != [] else 0)

    def inc(self):
        """Does nothing if stack is empty"""
        if self.onLeft:
            if self.l_stack != []:
                self.l_stack[-1] += 1
            else:
                self.l_stack.append(1)
        else:
            if self.r_stack != []:
                self.r_stack[-1] += 1
            else:
                self.r_stack.append(1)

    def dec(self):
        """Does nothing if stack is empty"""
        if self.onLeft:
            if self.l_stack != []:
                self.l_stack[-1] += 1
        else:
            if self.r_stack != []:
                self.r_stack[-1] += 1

    def switch(self):
        self.onLeft = not self.onLeft

    def find_parens(self, s):
        """Code by Baltasarq on StackOverflow:
        https://stackoverflow.com/a/29992065"""
        toret = {}
        pstack = []
        for i, c in enumerate(s):
            if c == '8':
                pstack.append(i)
            elif c == '9':
                if len(pstack) == 0:
                    {}
                toret[pstack.pop()] = i

        if len(pstack) > 0:
            return {}

        return toret

    def find_match_paren(self, index: int, expr: str) -> int:
        all_paren_indexes = self.find_parens(expr)
        instruction = expr[index]
        if index < 0 or index >= len(expr):
            return -8000
        if index in all_paren_indexes.keys():
            if instruction == '8':
                return all_paren_indexes.get(index)
        if index in all_paren_indexes.values():
            if instruction == '9':
                return {all_paren_indexes[k]: k for k in all_paren_indexes}.get(index)
        else:
            return -1

    def run(self, hex_program: str):
        program_pointer = 0
        while program_pointer < len(hex_program):
            instruction = hex_program[program_pointer]
            match instruction:
                case '0':
                    # Instruction 0 used as padding for the end
                    # of the program, nothing left to do
                    if program_pointer == len(hex_program)-1:
                        return
                    elif hex_program[program_pointer+1] in ['3', '7', 'b', 'f']:
                        nb_bytes = (
                            int(hex_program[program_pointer+1], base=16)+1)//4
                        number_to_push = int(
                            "".join(hex_program[program_pointer+2:program_pointer+2+nb_bytes]))
                        self.push(number_to_push)
                        program_pointer += (1+nb_bytes)
                    else:
                        pass  # noop, ignore, whatever this doesn't work

                case '1':  # factorial
                    self.push(factorial(self.pop()))
                case '2':  # addition
                    a = self.pop()
                    b = self.pop()
                    self.push(a+b)
                case '3':  # substraction
                    a = self.pop()
                    b = self.pop()
                    self.push(b-a)
                case '4':  # increment
                    self.inc()
                case '5':  # decrement
                    self.dec()
                case '6':  # swap top two elements
                    a = self.pop()
                    b = self.pop()
                    self.push(a)
                    self.push(b)
                case '7':  # duplicate top
                    a = self.peek()
                    self.push(a)
                case '8':  # [
                    end = self.find_match_paren(program_pointer, hex_program)
                    a = self.peek()
                    if (end != -1) and (a == 0):
                        program_pointer = end
                case '9':  # ]
                    start = self.find_match_paren(program_pointer, hex_program)
                    a = self.peek()
                    if (start != -1) and (a != 0):
                        program_pointer = start
                case 'a':  # push input
                    """
                    I still need to decide if input is always
                    convert from text to int, or if
                    it ignores all inputs except integers
                    """
                    self.push(input())
                case 'b':  # switch to other stack
                    self.switch()
                case 'c':  # output top
                    n = self.peek()
                    print(n, end="")
                case 'd':  # output top as unicode
                    n = self.peek()
                    print(chr(n), end="")
                case 'e':  # pop
                    self.pop()
                case 'f':  # pop into other stack
                    a = self.pop()
                    self.switch()
                    self.push(a)
                    self.switch()
                case other:  # ?
                    pass
            program_pointer += 1

if len(sys.argv) != 2:
    print("interpreter takes one (1) microstack program as input")
    sys.exit()

program = open(file=sys.argv[1], encoding='ISO-8859-1', mode='r')
program = program.read()

interpreter = Interpreter()

hex_program = interpreter.hexify(program)
#print(hex_program)
interpreter.run(hex_program)
