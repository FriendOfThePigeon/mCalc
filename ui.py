#!/bin/env python3

import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, Gdk, GObject
from parser import stacky_parser
from parsy import ParseError
from stacky import Evaluator, EvalError
import stdlib

def print_result(result):
    return ' '.join(str(each) for each in result.as_list())

def debug(msg, nl=True):
    sys.stderr.write(msg)
    if nl:
        sys.stderr.write('\n')

def set_style_class(widget, css_class, value):
    context = widget.get_style_context()
    is_set = context.has_class(css_class)
    if value and not is_set:
        context.add_class(css_class)
    elif is_set and not value:
        context.remove_class(css_class)

def update_label(label):
    def result(buffer):
        expr = get_all_text(buffer)
        buffer.remove_tag_by_name('error', buffer.get_start_iter(), buffer.get_end_iter())
        try:
            parsed = stacky_parser.parse(expr)
            label.set_text(print_result(Evaluator(stdlib.stdlib, []).evaluate(parsed)))
            set_style_class(label, 'evalerror', False)
        except ParseError as ex:
            buffer.apply_tag_by_name('error', buffer.get_iter_at_offset(ex.index), buffer.get_end_iter())
            set_style_class(label, 'evalerror', True)
        except EvalError as ex:
            set_style_class(label, 'evalerror', True)

    return result

def get_all_text(buffer):
    return buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)

def buffer_insert(grid, rows, signal_name):
    def result(buffer, location, text, length):
        if '\n' in text:
            GObject.signal_stop_emission_by_name(buffer, signal_name)
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
    frame = Gtk.Frame()
    frame.set_hexpand(True)
    set_style_class(frame, 'expr', True)
    view = Gtk.TextView()
    view.set_justification(Gtk.Justification.CENTER)
    label = Gtk.Label()
    label.set_selectable(True)
    label.set_line_wrap(True)
    label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
    label.set_hexpand(True)
    set_style_class(label, 'result', True)
    buffer = view.get_buffer()
    buffer.create_tag(tag_name='error', underline=Pango.Underline.ERROR_LINE, underline_rgba=Gdk.RGBA(1.0, 0, 0, 0))
    buffer.connect('changed', update_label(label))
    buffer.connect('insert-text', buffer_insert(grid, rows, 'insert-text'))

    frame.add(view)
    grid.attach(frame, 0, index, 1, 1)
    grid.attach(label, 1, index, 1, 1)
    view.set_halign(Gtk.Align.FILL)
    view.set_valign(Gtk.Align.CENTER)
    frame.show()
    view.show()
    label.show()

    rows.append((buffer, view, label))
    view.grab_focus()

def setup_styles():
    provider = Gtk.CssProvider()
    provider.load_from_data('''
frame.expr {
    background-color: white;
}
frame.expr border {
    border: 1px solid gray;
}
textview  {
    padding: 6px;
    font: 20px "Monospace";
}
grid label.evalerror {
    border: 1px solid red;
}
.result {
    font: 20px "Monospace";
    border: 1px solid gray;
    padding: 6px;
}
grid{
    margin: 12px; 
}
'''.encode('utf-8'))
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider, 100)


def on_activate(app):
    win = Gtk.ApplicationWindow(application=app)
    grid = Gtk.Grid()
    grid.set_column_spacing(12)
    grid.set_row_spacing(12)
    win.add(grid)
    win.set_title('mCalc')

    rows = []
    add_row(grid, rows)

    setup_styles()

    win.set_default_size(300, 100)
    win.show_all()


def main():
    app = Gtk.Application(application_id='org.gtk.Example')
    app.connect('activate', on_activate)
    app.run(None)

if __name__ == '__main__':
    main()
