from subprocess import Popen

from Dart.lib.plat import supress_window


class GenericBinary(object):
    '''Starts a process.
    '''
    def __init__(self, *args, show_window=True):
        '''
        @show_window
          Windows only. Whether to show a window.
        '''
        self.args = args
        self.startupinfo = None
        if not show_window:
            self.startupinfo = supress_window()

    def start(self, args=[], env={}, shell=False, cwd=None):
        cmd = self.args + tuple(args)
        Popen(cmd, startupinfo=self.startupinfo, env=env, shell=shell,
              cwd=cwd)


class AsyncStreamReader(threading.Thread):
    '''Reads a process stream from an alternate thread.
    '''
    def __init__(self, stream, on_data, *args, **kwargs):
        '''
        @stream
          Stream to read from.

        @on_data
          Callback to call with bytes read from @stream.
        '''
        super().__init__(*args, **kwargs)
        self.stream = stream
        self.on_data = on_data
        assert(self.on_data, 'wrong call: must provide callback')

    def run(self):
        while True:
            data = self.stream.readline()
            if not data:
                return

            self.on_data(data)

