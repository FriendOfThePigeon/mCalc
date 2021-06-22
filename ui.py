#!/bin/env python3

import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, Gdk, GObject
from parser import stacky_parser
from parsy import ParseError
from stacky import Evaluator, EvalError
import stdlib
from string import ascii_uppercase
from basic import RootNamespace

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

namespace = RootNamespace(stdlib.stdlib).spawn()

def run_evaluation(label, name, callback):
    def result(buffer):
        expr = get_all_text(buffer)
        buffer.remove_tag_by_name('error', buffer.get_start_iter(), buffer.get_end_iter())
        try:
            parsed = stacky_parser.parse(expr)
            label.set_text(print_result(Evaluator(namespace, []).evaluate(parsed, name_result=name)))
            set_style_class(label, 'evalerror', False)
            if callback:
                callback()
        except ParseError as ex:
            buffer.apply_tag_by_name('error', buffer.get_iter_at_offset(ex.index), buffer.get_end_iter())
            set_style_class(label, 'evalerror', True)
        except EvalError as ex:
            set_style_class(label, 'evalerror', True)

    return result

def get_all_text(buffer):
    return buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)

def set_all_text(buffer, text):
    length = len(text)
    buffer.set_text(text, length)

def find_window(widget):
    parent = widget.get_parent()
    if not parent:
        return widget
    return find_window(parent)

def catch_special_keys(grid, rows):
    def result(text_view, event):
        if event.hardware_keycode == 24 and (Gdk.ModifierType.CONTROL_MASK & event.state):
            # Ctrl-Q = close window => quit
            find_window(grid).close()
            return True
        elif event.hardware_keycode == 36:
            # Enter = add new row;
            # with Shift: copy expression.
            initial_text = get_all_text(text_view.get_buffer()) if Gdk.ModifierType.SHIFT_MASK & event.state else ''
            add_row(grid, rows, initial_text=initial_text)
            return True
        # debug('group: %s; hardware_keycode: %s; is_modifier: %s; keyval: %s; length: %s; send_event: %s; state: %s; string: %s; time: %s; type: %s' % (event.group, event.hardware_keycode, event.is_modifier, event.keyval, event.length, event.send_event, event.state, event.string, event.time, event.type))

        return False

    return result

def attach_label(grid, label, index):
    def result():
        if not label.get_parent():
            grid.attach(label, 2, index, 1, 1)
            label.show()

    return result

def add_row(grid, rows, initial_text=''):
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
    result_label = Gtk.Label()
    result_label.set_selectable(True)
    result_label.set_hexpand(True)
    set_style_class(result_label, 'result', True)
    name = chr(65 + index)
    name_label = Gtk.Label.new(name)
    set_style_class(name_label, 'name', True)
    buffer = view.get_buffer()
    buffer.create_tag(tag_name='error', underline=Pango.Underline.ERROR_LINE, underline_rgba=Gdk.RGBA(1.0, 0, 0, 0))

    view.connect('key-press-event', catch_special_keys(grid, rows))
    view.add_events(Gdk.EventMask.KEY_PRESS_MASK)
    buffer.connect('changed', run_evaluation(result_label, name, attach_label(grid, name_label, index)))

    frame.add(view)
    grid.attach(frame, 0, index, 1, 1)
    grid.attach(result_label, 1, index, 1, 1)
    view.set_halign(Gtk.Align.FILL)
    view.set_valign(Gtk.Align.CENTER)
    frame.show()
    view.show()
    result_label.show()

    if initial_text:
        set_all_text(buffer, initial_text)

    rows.append((buffer, view, result_label))
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


def app_activate(app):
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
    app.connect('activate', app_activate)
    app.run(None)

if __name__ == '__main__':
    main()
