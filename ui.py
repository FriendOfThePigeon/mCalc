import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, Gdk, GObject
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

def buffer_insert(grid, rows, signal_name):
    def result(buffer, location, text, length):
        if '\n' in text:
            GObject.signal_stop_emission_by_name(buffer, signal_name)
            add_row(grid, rows)
            return True
        return False
    return result

def set_css_class(widget, css_class):
    context = widget.get_style_context()
    context.add_class(css_class)

def add_row(grid, rows):
    index = len(rows)
    if rows:
        # If the last buffer is empty, set the focus there instead of adding a new one.
        if get_all_text(rows[-1][0]) == '':
            rows[-1][1].grab_focus()
            return
    view = Gtk.TextView()
    label = Gtk.Label()
    label.set_selectable(True)
    label.set_line_wrap(True)
    label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
    set_css_class(label, 'result')
    buffer = view.get_buffer()
    buffer.create_tag(tag_name='error', underline=Pango.Underline.ERROR_LINE, underline_rgba=Gdk.RGBA(1.0, 0, 0, 0))
    buffer.connect('changed', update_label(label))
    buffer.connect('insert-text', buffer_insert(grid, rows, 'insert-text'))

    grid.attach(view, 0, index, 1, 1)
    grid.attach(label, 1, index, 1, 1)
    view.show()
    label.show()

    rows.append((buffer, view, label))
    view.grab_focus()

def setup_styles():
    provider = Gtk.CssProvider()
    provider.load_from_data('''
textview  {
    font: 20px "Monospace";
}
.result {
    font: 20px "Monospace";
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

    rows = []
    add_row(grid, rows)

    setup_styles()

    win.show_all()


def main():
    app = Gtk.Application(application_id='org.gtk.Example')
    app.connect('activate', on_activate)
    app.run(None)

if __name__ == '__main__':
    main()
