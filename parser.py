from basic import Sym, WS
from parsy import alt, decimal_digit, regex, seq, string

number_literal = seq(decimal_digit.at_least(1).concat(), string('.').then(decimal_digit.at_least(1).concat()).optional()).combine(lambda a, b: float(a + '.' + b) if b else int(a))

string_literal = string('"') >> regex(r'[^"]*') << string('"')

operator = regex(r'[+*^/.\\@d-]').map(Sym)

whitespace = string(' ').at_least(1).map(WS)

stacky_parser = alt(number_literal, operator, whitespace).many()
