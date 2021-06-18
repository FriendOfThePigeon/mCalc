mCalc.pl
========

A RPN (stack-based) calculator with history.

Language
========

Literals
--------
Literals are simply pushed onto the stack.

`-1234` Integer

`1234.0` Float

`"a string"` String

Operators
---------
When an operator is encountered, the required operands are popped from the stack and the result is pushed on.

In the following, (1) refers to the first value popped from the stack; (2) the second; and so on.

| Operator  | Description | Result |
| --------  | ----------- | ------ |
| `\+`      | Addition    | `2 1 -> 3` |
| `\-`      | Subtraction | `2 1 -> 1` |
| `\*`, `x` | Multiplication | `3 2 -> 6` |
| `/`       | Division    | `5 2 / -> 2.5` |
| `^`       | Exponentiation | `2 3 ^ -> 8` |
| `\\`      | Swap the first two values on the stack | `2 1 -> 1 2` |
| `d`       | Remove the first value from the stack and drop (discard) it | `2 1 -> 2` |
| `.`       | Duplicate the first value on the stack | 1 -> 1 1 | 
| `@`       | Rotate the first 3 values on the stack | `3 2 1 -> 2 1 3` |
| `_`       | Floor (discard fractional part) | `1.3 -> 1` |
| `sin`
  `cos`
  `tan`
  `asin`
  `acos`
  `atan`     | The respective geometric functions | |
| `deg`      | Convert radians to degrees | |
| `rad`      | Convert degrees to radians | |
| `pi`       | Pushes the constant pi | |
| `e`        | Pushes the constant e | |
| `ln`       | Natural logorithm | `0 ln -> 1.0` |
| `log`      | Logorithm in a given base | `8 2 log -> 3.0` |
| `:`        | Split number into integer and fractional parts and push them | `1.5 : -> 1.0 0.5` |
| `!`        | Push the elements of the array | `[ 1 2 3 ]! -> 1 2 3` |



Arrays
------
The start of an array can be created by entering `[`, and the array is pushed when `]` is entered.

Most unary operators, if applied to an array, will be mapped over the elements of the array.

Most binary operators will be used to reduce the array, ie. apply the operator to the first pair of elements, then apply the operator to the result of that and the next element, and so on, until the whole array has been used. If the array only contains one element, then that is the result. It is an error to apply such an operator to an empty array.
