# microstack
## A stack based esoteric language

### Description

Microstack uses two stacks as memory.

Every instruction is an operation on one of those stacks.

In a microstack program, each character (roughly) represents two instructions.
For example, `/`, U+002F, represents instructions `2` and `f`

### Interpreter

Not working yet.

Some instructions will probably change.

There currently is a need for interaction between stacks.

### Instruction set (in hexadecimal)

- `0x`: push the next `x`+1bit integer to the stack

    `x` can only be `3`, `7`, `b` or `f`

    Example:

    ```0f8bba```

    Pushes the `f`+1bit integer 35770 to the stack
- `1`: pop top, factorial, push result
- `2`: add top and second, pop both, push result
- `3`: sub top from second, pop both, push result
- `4`: mult top and second, pop both, push result
- `5`: div top from second, pop both, push result
- `6`: swap top and second
- `7`: push top on the stack (duplicate top)
- `8`: go to matching `9` if top is 0 (Like a bf `[`)
- `9`: go to matching `8` if top is not 0 (Like a bf `]`)
- `a`: push input
- `b`: switch to other stack
- `c`: output the top of the stack
- `d`: output the top of the stack as unicode
- `e`: output the top of the stack and pop
- `f`: output the top of the stack as unicode and pop

### file extensions
- .µ    : microstack program