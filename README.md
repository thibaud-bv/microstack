# microstack
## A stack based esoteric language

### Description

Microstack uses one stack as storage.

Every instruction is an operation on that stack.

In a microstack program, each character represents two instructions (except one).
For example, `/`, U+002F, 00101111 in binary, represents instructions 0010 and 1111

### Instruction set (in binary)

- 0000 numb (0N): push the next numb+1bit integer to the stack
    numb+1 must be 4, 8, 12 or 16
    Example:
    Push the 15+1bit number 35770 to the stack
    - 0000 1111 1000 1011 1011 1010
- 0001 (1):
- 0010 (2): add top and second, pop both, push result
- 0011 (3): sub top from second, pop both, push result
- 0100 (4): mult top and second, pop both, push result
- 0101 (5): div top from second, pop both, push result
- 0110 (6): swap top and second
- 0111 (7): push top on the stack (duplicate top)
- 1000 (8): 
- 1001 (9):
- 1010 (a):
- 1011 (b):
- 1100 (c): output the top of the stack
- 1101 (d): output the top of the stack as unicode
- 1110 (e): output the top of the stack and pop
- 1111 (f): output the top of the stack as unicode and pop

### extensions:
- .    : microstack program written as characters
- .bms : microstack program written in binary