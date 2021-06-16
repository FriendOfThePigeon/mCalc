import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from parser import stacky_parser
from stacky import Evaluator
import stdlib

def print_result(result):
    return ' '.join(str(each) for each in result)

def debug(msg, nl=True):
    sys.stderr.write(msg)
    if nl:
        sys.stderr.write('\n')


def update_label(label):
    def result(entry):
        expr = entry.get_chars(0, -1)
        parsed = stacky_parser.parse(expr)
        label.set_text(print_result(Evaluator(stdlib.stdlib, []).evaluate(parsed).as_list()))
    return result

def entry_activate(grid, rows):
    def result(entry):
        add_row(grid, rows)
    return result

def add_row(grid, rows):
    index = len(rows)
    if rows:
        last_entry = rows[-1][0]
        if last_entry.get_chars(0, -1) == '':
            last_entry.grab_focus()
            return
    entry = Gtk.Entry()
    label = Gtk.Label()
    entry.connect('changed', update_label(label))
    entry.connect('activate', entry_activate(grid, rows))
    grid.attach(entry, 0, index, 1, 1)
    grid.attach(label, 1, index, 1, 1)
    entry.show()
    label.show()
    rows.append((entry, label))
    entry.grab_focus()

def on_activate(app):
    win = Gtk.ApplicationWindow(application=app)
    grid = Gtk.Grid()
    win.add(grid)

    rows = []
    add_row(grid, rows)

    win.show_all()

def main():
    app = Gtk.Application(application_id='org.gtk.Example')
    app.connect('activate', on_activate)
    app.run(None)

if __name__ == '__main__':
    main()
