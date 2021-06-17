from basic import Sym, WS
from parsy import alt, decimal_digit, regex, seq, string

def make_number(sign, int_part, frac_part):
    result = float(int_part + '.' + frac_part) if frac_part else int(int_part)
    return result * -1 if sign else result

number_literal = seq(string('-').optional(), decimal_digit.at_least(1).concat(), string('.').then(decimal_digit.at_least(1).concat()).optional()).combine(make_number)

string_literal = string('"') >> regex(r'[^"]*') << string('"')

operator = regex(r'[+*^/.\\@d_-]').map(Sym)

whitespace = string(' ').at_least(1).map(WS)

stacky_parser = alt(number_literal, operator, whitespace).many()
