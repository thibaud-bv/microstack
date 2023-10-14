# microstack
## A stack based esoteric language

### Description

In a microstack program, each instruction is half a byte (one nibble), meaning one ASCII character (one byte) encodes two instructions.

Because of this, code is better read and written directly in hexadecimal, for example with [HxD](https://mh-nexus.de/en/hxd/)

Microstack uses two stacks as memory, and a pointer to one of those stacks

### Interpreter

The interpreter isn't fully functionnal yet.

Some instructions of the language may change.

### Instruction set (in hexadecimal)

- `0`: push max of two top values
- `1`: pop top, factorial, push result
- `2`: add top and second, pop both, push result
- `3`: sub top from second, pop both, push result
- `4`: increment top
- `5`: decrement top
- `6`: swap top and second
- `7`: duplicate top
- `8`: go to matching `9` if top is 0 (Like a bf `[`)
- `9`: go to matching `8` if top is not 0 (Like a bf `]`)
- `a`: take input and push to the stack
- `b`: switch to other stack
- `c`: output the top of the stack
- `d`: output the top of the stack as unicode
- `e`: pop
- `f`: pop from current current stack and push to other

*Detailed description for each instruction coming soon*

### Flags (not yet implemented)

Flags can be used to alter the way the program will run, for example:

- ignore the last nibble (as the instruction `0` is both `max` and padding)
- other stuff probably

### file extensions
- .µ    : microstack program
- .µdoc : file for comments/explanations
