import functools
import sublime
import sublime_plugin
import os
import re
import subprocess
import threading
import tempfile

class DartAnalyzerError:
  """ Contains the data of an error output by the Dart analyzer. """
  def __init__(self, error_type_one, error_type_two, error_type_three, path,
               region, message):
    self.error_type_one = error_type_one
    self.error_type_two = error_type_two
    self.error_type_three = error_type_three
    self.path = path
    self.region = region
    self.message = message

class DartAnalyzerPlugin(sublime_plugin.EventListener):
  """ This plugin automatically runs the Dart analyzer on Dart files and shows
      errors in the editor without the user needed to run it manually. """

  # This is a counter used to keep track of when the user is idle.
  pending = 0

  # This map holds a revision number for each buffer, so we can track analysis
  # passes and not show old passes. Keys are the the id computed by get_id().
  revisions = {}

  # This map holds the errors for each view. This is used to update the status
  # when the user moves their cursor so that we can display the error in the
  # status bar. Keys are the id computed by get_id().
  errors = {}

  def __init__(self, *args, **kwargs):
    sublime_plugin.EventListener.__init__(self, *args, **kwargs)

  def handle_timeout(self, view):
    """ Call the idle handler when there hasn't been a recent modification. """
    self.pending -= 1
    if self.pending == 0:
      self.on_idle(view)

  def get_id(self, view):
    """ Returns a unique id for this buffer. """
    return "%d-%d" % (view.id(), view.buffer_id())

  def increment_revision(self, view):
    if self.get_id(view) in self.revisions:
      self.revisions[self.get_id(view)] += 1
    else:
      self.revisions[self.get_id(view)] = 0

  def on_modified(self, view):
    """ Queue an analysis pass when the file is changed. """
    if not self.is_dart_file(view):
      return
    self.clear_errors(view)
    self.increment_revision(view)
    self.pending += 1
    sublime.set_timeout(functools.partial(self.handle_timeout, view), 1000)

  def is_dart_file(self, view):
    """ Check if this is a Dart file by looking at the language mode. """
    syntax = view.settings().get('syntax')
    if syntax is None:
      return False
    return re.search('Dart', syntax, flags=re.IGNORECASE)

  def on_idle(self, view):
    """ Called when the file hasn't been modified recently. """
    self.run_analyzer(view)

  def on_load(self, view):
    """ Called when the file is first loaded. """
    if self.is_dart_file(view):
      self.increment_revision(view)
      self.run_analyzer(view)

  def on_post_save(self, view):
    """ Called when the user saves the file. """
    if self.is_dart_file(view):
      self.increment_revision(view)
      self.run_analyzer(view)

  def run_analyzer(self, view):
    """ Starts the Dart analyzer thread. """
    dartsdk_path = view.settings().get('dartsdk_path')
    content = view.substr(sublime.Region(0, view.size()))
    DartAnalyzerThread(self, view, dartsdk_path, view.file_name(),
                       self.get_id(view), content,
                       self.revisions[self.get_id(view)]).start()

  def clear_errors(self, view):
    if self.get_id(view) in self.errors:
      del self.errors[self.get_id(view)]
    view.erase_regions('dartanalyzer')

  def draw_errors(self, view, errors, revision):
    """ Show the errors in the buffer. This is the callback from analyzer
        thread. """
    # Only show the errors we got if the file revision is still the same.
    if revision != self.revisions[self.get_id(view)]:
      return
    self.errors[self.get_id(view)] = errors
    view.add_regions('dartanalyzer', [error.region for error in errors],
                     'keyword', 'dot', sublime.DRAW_OUTLINED)
    # Trigger the status bar update.
    self.on_selection_modified(view)


  def on_selection_modified(self, view):
    """ Updates the status bar to show an error if the user moves their cursor
        into an error region. """
    view.erase_status('dartanalyzer')
    # Don't do anything if there are no errors for this file.
    if not self.get_id(view) in self.errors:
      return
    for sel in view.sel():
      for error in self.errors[self.get_id(view)]:
        if error.region.contains(sel):
          view.set_status('dartanalyzer', error.message)
          return

class DartAnalyzerThread(threading.Thread):
  """ This class is responsible for running the analyzer in its own thread,
      and delivering the resulting errors back to the plugin. """
  def __init__(self, plugin, view, dartsdk_path, path, id, content, revision):
    super(DartAnalyzerThread, self).__init__()
    self.plugin = plugin
    self.view = view
    self.dartsdk_path = dartsdk_path
    self.path = path
    self.id = id
    self.content = content
    self.revision = revision

  def is_windows(self):
    """ Convenience method for if the platform is running Windows. """
    return sublime.platform() == 'windows'

  def get_startupinfo(self):
    """ Get the extra options to prevent Windows from showing a command prompt
        when running external programs. """
    if self.is_windows():
      startupinfo = subprocess.STARTUPINFO()
      startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
      startupinfo.wShowWindow = subprocess.SW_HIDE
      return startupinfo
    return None

  def parse_errors(self, lines):
    """ Takes the output lines from the Dart analyzer and parses it into a
        useful format, sending the result back to the plugin. """
    errors = []
    for line in lines:
      parsed = line.rstrip().split('|')
      error_type_one = parsed[0]
      error_type_two = parsed[1]
      error_type_three = parsed[2]
      path = parsed[3]
      row = int(parsed[4])
      col = int(parsed[5])
      length = int(parsed[6])
      message = parsed[7]
      start = self.view.text_point(row - 1, col - 1) - 1
      end = start + length

      # Bail out if this error has a length of 0, because we'll have nothing to
      # display.
      if length == 0:
        continue

      errors.append(
        DartAnalyzerError(error_type_one, error_type_two, error_type_three,
                          path, sublime.Region(start, end), message))
    
    # Send the errors back to main plugin.
    self.plugin.draw_errors(self.view, errors, self.revision)

  def run(self):
    """ Runs the Dart analyzer executable. """
    print('*** Running Dart analyzer...')

    dartanalyzer_path = os.path.join(self.dartsdk_path, 'bin', 'dartanalyzer')
    if (self.is_windows()):
      dartanalyzer_path += '.bat'

    if (self.path is None):
      directory = tempfile.gettempdir()
      file_name = '~TMP-%s-%d.dart' % (self.id, self.revision)
    else:
      directory = os.path.dirname(self.path)
      file_name = '~TMP-%d-%s' % (self.revision, os.path.basename(self.path))

    f = open(os.path.join(directory, file_name), 'w')
    f.write(self.content)
    f.close()

    proc = subprocess.Popen([dartanalyzer_path, '--machine',
                             '--package-root=packages/', file_name],
      cwd=directory,
      stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
      startupinfo=self.get_startupinfo())
    
    if proc.stdout is not None:
      lines = proc.stdout.readlines()
      # Parsing needs to be done on the main thread to access the view object.
      sublime.set_timeout(lambda: self.parse_errors(lines), 50)

    # Delete the temporary file.
    os.remove(os.path.join(directory, file_name))
    print('*** Done.')
