import sublime

from Dart.sublime_plugin_lib.sublime import after


notification_tpl = """
<style type="text/css">
    html { background-color: #A9CCFF }
</style>
<div>
    %s
</div>
"""

severe_tpl = """
<style type="text/css">
    html { background-color: #FFA4A4 }
</style>
<div>
    %s
</div>
"""


def show_info(view, content, location=-1, timeout=0):
    view.show_popup(notification_tpl % content, location=location, max_width=500)

    if timeout:
        after(timeout, lambda: view.hide_popup())


def show_error(view, content, location=-1, timeout=0):
    view.show_popup(severe_tpl % content, location=location, max_width=500)

    if timeout:
        after(timeout, lambda: view.hide_popup())
