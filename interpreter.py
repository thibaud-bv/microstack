from math import factorial
import sys


class Interpreter:

    def __init__(self) -> None:
        self.l_stack: list = []
        self.r_stack: list = []
        self.onLeft: bool = True
        self.program_pointer: int = 0
        self.hex_program: str = ""
        self.hasOutputed: bool = False

    def push(self, n: int | str):
        """
        If n is an int, pushes n

        If n is a str and decimal, pushes n converted to int

        If n is a str and not decimal, pushes 1

        If n is empty, pushes 0
        """
        number_to_push = 0
        if type(n) == str:
            if len(n) == 0:  # n == ""
                number_to_push = 0
            elif n.isdecimal():  # n == "79"
                number_to_push = int(n)
            elif len(n) >= 2 and n[0] == '-' and n[1:].isdecimal():  # n == "-45"
                number_to_push = int(n)
            else:  # n == "bob"
                number_to_push = 1
        elif type(n) == int:  # n == 15
            number_to_push = n
        else:  # invalid input pushes 1, this shouldn't happen but just in case
            number_to_push = 1

        if self.onLeft:
            self.l_stack.append(number_to_push)
        else:
            self.r_stack.append(number_to_push)

    def parse(self, ascii_program: str) -> str:
        hexed_program = ""
        for c in ascii_program:
            hex_c = hex(ord(c))[2:]
            if len(hex_c) <= 2:
                hex_c = (2-len(hex_c))*'0'+hex_c
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
        """
        Increments the stack by 1
        Pushes 1 on the stack if it is empty
        """
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
        """
        Decrements the stack by 1
        Pushes -1 on the stack if it is empty
        """
        if self.onLeft:
            if self.l_stack != []:
                self.l_stack[-1] -= 1
            else:
                self.l_stack.append(-1)
        else:
            if self.r_stack != []:
                self.r_stack[-1] -= 1
            else:
                self.r_stack.append(-1)

    def switch(self):
        self.onLeft = not self.onLeft

    def output(self, value: int, type: str, end_with: str):
        if type == "number":
            print(value, end=end_with)
        elif type == "unicode":
            print(chr(value), end=end_with)
        self.hasOutputed = True

    def find_parens(self, s):
        # TODO : Find a better way to handle nested loops
        """Code adapted from Baltasarq on StackOverflow:
        https://stackoverflow.com/a/29992065"""
        toret = {}
        parenthesis_stack = []
        for index, character in enumerate(s):
            if character == '8':
                parenthesis_stack.append(index)
            elif character == '9':
                if len(parenthesis_stack) == 0:
                    return {}
                toret[parenthesis_stack.pop()] = index

        if len(parenthesis_stack) > 0:
            return {}

        return toret

    def find_match_paren(self, index: int, expr: str) -> int:
        # TODO : Find a better way to handle nested loops
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
                case '0':  # max
                    a = self.pop()
                    b = self.peek()
                    self.push(a)
                    self.push(max(a, b))
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
                    if (end > -1) and (a == 0):
                        program_pointer = end
                case '9':  # ]
                    start = self.find_match_paren(program_pointer, hex_program)
                    a = self.peek()
                    if (start > -1) and (a != 0):
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
                    self.output(value=n, type="number", end_with="")
                case 'd':  # output top as unicode
                    n = self.peek()
                    self.output(value=n, type="unicode", end_with="")
                case 'e':  # pop
                    self.pop()
                case 'f':  # pop into other stack
                    a = self.pop()
                    self.switch()
                    self.push(a)
                    self.switch()
                case other:  # There shouldn't be any way for this to happen
                    print(f"Instruction {other} at position {program_pointer} doesn't exist.")
            # Go to the next instruction
            program_pointer += 1
        # "implicit" output, if nothing was ever outputed,
        # output the top of the stack as a number
        if not self.hasOutputed:
            self.output(self.peek(), "number", "\n")



if len(sys.argv) != 2:
    print("interpreter takes one (1) microstack program as input")
    sys.exit()

program = open(file=sys.argv[1], encoding='ISO-8859-1', mode='r')
program = program.read()

interpreter = Interpreter()

hex_program = interpreter.parse(program)
interpreter.run(hex_program)
