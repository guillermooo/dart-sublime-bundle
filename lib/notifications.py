import sublime

from Dart.sublime_plugin_lib.sublime import after


ERROR_TEMPLATE = """
<style type="text/css">
    html { background-color: #FFFFD1 }
    strong.ERROR { color: white; background-color: red }
    strong.WARNING { color: white; background-color: #E68A00 }
    strong.INFO { color: white; background-color: #3399FF }
</style>
<div>
    <strong class="%(severity)s">&nbsp;%(tag)s&nbsp;</strong> %(message)s'
</div>
"""

STATUS_TEMPLATE = """
<style type="text/css">
    html { background-color: #99CCFF }
</style>
<div>
    %s
</div>
"""

TOOLTIP_ID = 0


def next_id():
    global TOOLTIP_ID
    while True:
        TOOLTIP_ID += 1
        yield TOOLTIP_ID
        if TOOLTIP_ID > 100:
            TOOLTIP_ID = 0


id_generator = next_id()


def show_status_tooltip(content, view=None, location=-1, timeout=0):
    content = STATUS_TEMPLATE % content
    show_tooltip(content, view, location, timeout)


def show_analysis_tooltip(content, view=None, location=-1, timeout=0):
    content['tag'] = content['severity'][0]
    show_tooltip(ERROR_TEMPLATE % content, view, location, timeout)


def show_tooltip(content, view=None, location=-1, timeout=0):
    '''
    Shows a tooltip.

    @content
      The tooltip's content (minihtml).

    @view
      The view in which the tooltip should be shown. If `None`, the active view
      will be used if available.

    @location
      Text location at which the tooltip will be shown.

    @timeout
      If greater than 0, the tooltip will be autohidden after @timeout
      milliseconds.
    '''
    if not view:
        try:
            view = sublime.active_window().active_view()
        except AttributeError as e:
            return

    view.show_popup(content, location=location, max_width=500)

    if timeout > 0:
        def hide(current_id):
            global TOOLTIP_ID
            if TOOLTIP_ID == current_id:
                view.hide_popup()

        current_id = next(id_generator)
        after(timeout, lambda: hide(current_id))
