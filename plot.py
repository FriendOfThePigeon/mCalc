
import svg
from evaluate import Evaluator

from basic import Point, BasicNamespace


def plot_point(namespace, f, tag, x, y):
    namespace.set(tag, Point(x, y))

def plot_line(namespace, f, p1, p2):
    svg.plot_line(f, p1, p2)
    
def plot_circle(namespace, f, pos, radius):
    svg.plot_circle(f, pos, radius)
    
def do_(namespace, f, *args):
    pass  # args have been plotted as a side-effect

top_level_namespace = BasicNamespace({
    'plot': do_,
    'point': plot_point,
    'line': plot_line,
    'circle': plot_circle
})

def plot(filename, w, h, tree):
    with open(filename, 'w') as f:
        f.write(svg.xml_prolog)
        svg.svg_open(f, w, h)
        Evaluator(top_level_namespace, [f]).evaluate(tree)
        f.write('</svg>')

