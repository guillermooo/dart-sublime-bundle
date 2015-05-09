import sublime

from Dart.sublime_plugin_lib.sublime import after


notification_tpl = """
<style type="text/css">
	html { background-color: #FFFF99 }
</style>
<div>
	%s
</div>
"""


def show_info(view, content, location=-1, timeout=0):
	view.show_popup(notification_tpl % content, location=location)

	if timeout:
		after(timeout, lambda: view.hide_popup())

