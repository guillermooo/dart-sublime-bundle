import sublime
import sublime_plugin


from Dart import editor_context


class DartGoToDeclaration(sublime_plugin.WindowCommand):
    def run(self):
        try:
            view = self.window.active_view()
            if not view:
                return
        except Exception as e:
            return

        sel = view.sel()[0]        
        self.get_navigation(sel)

    def get_navigation(self, r):
        sources = editor_context.navigation.regions

        target = None
        for source in sources:
            if (source.offset <= r.begin()
                and (source.offset + source.length) >= r.begin()):
                    target = source
                    break

        first_target = target.targets[0]

        first_target = editor_context.navigation.targets[first_target]
        
        fname = editor_context.navigation.files[first_target.fileIndex]
        row = first_target.startLine
        col = first_target.startColumn

        # XXX(guillermooo): can we optimize this for the current view?
        self.window.open_file("{}:{}:{}".format(fname, row, col), sublime.ENCODED_POSITION)
