# common elements

import sublime
# import sublime_plugin


def MarkGutter(view, line_num):
    pass


def SelectText(view, line_num, target):
    # Should return a range obj I think
    pass


def Underline(view, line_num, u_type, target):
    pass


def DisplayInQuickPanel(view, dd_list, select_fn, highlight_fn):
    view.window().show_quick_panel(
        dd_list,
        on_select=select_fn,
        on_highlight=highlight_fn)
