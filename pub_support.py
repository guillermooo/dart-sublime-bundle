import sublime
import sublime_plugin
import os
import subprocess
import threading

from os.path import join

class PubspecListener(sublime_plugin.EventListener):
    def __init__(self, *args, **kwargs):
        sublime_plugin.EventListener.__init__(self, *args, **kwargs)

    def on_post_save(self, view):
        name = view.file_name()

        if os.path.basename(name) == 'pubspec.yaml':
            RunPub(view, name)

def RunPub(view, fileName):
    settings = view.settings()
    dartsdk_path = settings.get('dartsdk_path')

    if dartsdk_path:
        PubThread(view.window(), dartsdk_path, fileName).start()
         

class PubThread(threading.Thread):
    def __init__(self, window, dartsdk_path, fileName):
        super(PubThread, self).__init__()
        self.daemon = True
        self.window = window
        self.dartsdk_path = dartsdk_path
        self.fileName = fileName

    def run(self):
        working_directory = os.path.dirname(self.fileName)
        pub_path = join(self.dartsdk_path, 'bin', 'pub')        
        if IsWindows():
            pub_path += '.bat'

        print 'pub install %s' % self.fileName
        proc = subprocess.Popen([pub_path, 'install'], cwd=working_directory,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, _ = proc.communicate()
        
        if proc.returncode != 0:
            self.output = 'error running pub: %s\n%s' % (self.fileName, out)
            sublime.set_timeout(self.callback, 0)

    def callback(self):
        output_panel = self.window.get_output_panel('pub')
        self.window.run_command('show_panel', {'panel': 'output.pub'})
        edit = output_panel.begin_edit()
        output_panel.insert(edit, output_panel.size(), self.output)
        output_panel.end_edit(edit)


def IsWindows():
    return sublime.platform() == 'windows'

