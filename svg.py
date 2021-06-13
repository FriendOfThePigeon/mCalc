
def hsv2rgb(h, s, v):
    (r, g, b) = (0, 0, 0)
    if s <= 0.0: #  < is bogus, just shuts up warnings
        r = v
        g = v
        b = v
        return (r, g, b)

    hh = h / 60.0 if h < 360.0 else 0.0
    i = int(hh)
    ff = hh - i
    p = v * (1.0 - s)
    q = v * (1.0 - (s * ff))
    t = v * (1.0 - (s * (1.0 - ff)))

    if i == 0:
        r = v
        g = t
        b = p
    elif i == 1:
        r = q
        g = v
        b = p
    elif i == 2:
        r = p
        g = v
        b = t
    elif i == 3:
        r = p
        g = q
        b = v
    elif i == 4:
        r = t
        g = p
        b = v
    else:
        r = v
        g = p
        b = q
    return (r, g, b)

def hex_it(r, g, b):
    return '#%x%x%x' % (r, g, b)

def mul_255(*args):
    return [int(255 * each) for each in args]

xml_prolog = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'

def svg_open(f, width, height):
    f.write('<svg xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" version="1.0" width="%d" height="%d">' % (width, height))


def plot_line(f, p1, p2):
    edge_color = 'blue'
    stroke_width = 2

    f.write('<path style="stroke:%s;stroke-width:%d" d="M%f,%f L%f,%f" />' % (edge_color, stroke_width, p1.x, p1.y, p2.x, p2.y))


def plot_circle(f, pos, radius):
    edge_color = 'red'
    stroke_width = 2

    f.write('<circle style="stroke:%s;stroke-width:%d;fill:none;" cx="%f" cy="%f" r="%f" />' % (edge_color, stroke_width, pos.x, pos.y, radius))

