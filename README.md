mCalc.pl
========

A RPN (stack-based) calculator with history.

Language
========

Literals
--------
Literals are simply pushed onto the stack.

1234 Integer

1234.0 Float

"a string" String

Operators
---------
When an operator is encountered, the required operands are popped from the stack and the result is pushed on.

In the following, (1) refers to the first value popped from the stack; (2) the second; and so on.

| Operator | Description | Result |
| -------- | ----------- | ------ |
| \+       | Addition    | (2) (1) -> (2) + (1) |
| \-       | Subtraction | (2) (1) -> (2) - (1) |
| \*, x    | Multiplication | (2) (1) -> (2) * (1) |
| /        | Division    | (2) (1) -> (2) / (1) |
| ^        | Exponentiation | (2) (1) -> (2) raised to the power of (1) |
| \\       | Swap the first two values on the stack | (2) (1) -> (1) (2) |
| d        | Remove the first value from the stack and drop (discard) it | (2) (1) -> (2) |
| .        | Duplicate the first value on the stack | (1) -> (1) (1) | 
| @        | Rotate the first 3 values on the stack | (3) (2) (1) -> (2) (1) (3) |
| _        | Floor (discard fractional part) | 1.3 -> 1.0 |
