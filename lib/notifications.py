import sublime

from Dart.sublime_plugin_lib.sublime import after


notification_tpl = """
<style type="text/css">
    html { background-color: #99CCFF }
    strong.ERROR { padding: 1px 3px; color: white; background-color: red }
    strong.WARNING { padding: 1px 3px; color: white; background-color: #E68A00 }
    strong.INFO { padding: 1px 3px; color: white; background-color: #3399FF }
</style>
<div>
    %s
</div>
"""

severe_tpl = """
<style type="text/css">
    html { background-color: #FFFFD1 }
    strong.ERROR { color: white; background-color: red }
    strong.WARNING { color: white; background-color: #E68A00 }
    strong.INFO { color: white; background-color: #3399FF }
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
