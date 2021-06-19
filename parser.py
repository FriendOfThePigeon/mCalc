from basic import Sym, WS, Punc
from parsy import alt, decimal_digit, regex, seq, string

def make_number(sign, int_part, frac_part):
    result = float(int_part + '.' + frac_part) if frac_part else int(int_part)
    return result * -1 if sign else result

number_literal = seq(string('-').optional(), decimal_digit.at_least(1).concat(), string('.').then(decimal_digit.at_least(1).concat()).optional()).combine(make_number)

string_literal = string('"') >> regex(r'[^"]*') << string('"')

operator = regex(r'[]+*^/.\\@d_:!-]').map(Sym)

func = regex(r'sin|cos|tan|asin|acos|atan|deg|rad|pi|e|ln|log').map(Sym)

variable = regex(r'[A-Z]').map(Sym)

punc = regex(r'[\[]').map(Punc)

whitespace = string(' ').at_least(1).map(WS)

stacky_parser = alt(number_literal, operator, punc, func, variable, whitespace).many()
