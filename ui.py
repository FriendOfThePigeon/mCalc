import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, Gdk
from parser import stacky_parser
from parsy import ParseError
from stacky import Evaluator
import stdlib

def print_result(result):
    return ' '.join(str(each) for each in result)

def debug(msg, nl=True):
    sys.stderr.write(msg)
    if nl:
        sys.stderr.write('\n')


def update_label(label):
    def result(buffer):
        expr = get_all_text(buffer)
        buffer.remove_tag_by_name('error', buffer.get_start_iter(), buffer.get_end_iter())
        try:
            parsed = stacky_parser.parse(expr)
            label.set_text(print_result(Evaluator(stdlib.stdlib, []).evaluate(parsed).as_list()))
        except ParseError as ex:
            buffer.apply_tag_by_name('error', buffer.get_iter_at_offset(ex.index), buffer.get_end_iter())
            
    return result

def get_all_text(buffer):
    return buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)

def view_insert(grid, rows):
    def result(view, string):
        if '\n' in string:
            add_row(grid, rows)
            return True
        return False
    return result

def add_row(grid, rows):
    index = len(rows)
    if rows:
        # If the last buffer is empty, set the focus there instead of adding a new one.
        if get_all_text(rows[-1][0]) == '':
            rows[-1][1].grab_focus()
            return
    view = Gtk.TextView()
    buffer = view.get_buffer()
    label = Gtk.Label()
    label.set_selectable(True)
    label.set_line_wrap(True)
    label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)  # WORD_CHAR
    buffer.create_tag(tag_name='error', underline=Pango.Underline.ERROR_LINE, underline_rgba=Gdk.RGBA(1.0, 0, 0, 0))
    buffer.connect('changed', update_label(label))
    view.connect('insert-at-cursor', view_insert(grid, rows))

    grid.attach(view, 0, index, 1, 1)
    grid.attach(label, 1, index, 1, 1)
    view.show()
    label.show()

    rows.append((buffer, view, label))
    view.grab_focus()

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
