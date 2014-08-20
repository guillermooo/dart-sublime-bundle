from subprocess import Popen
from subprocess import PIPE
from subprocess import TimeoutExpired
import threading

from Dart import PluginLogger
from Dart.lib.plat import supress_window


_logger = PluginLogger(__name__)


class TextFilter(object):
    '''Filters text through an external program (sync).
    '''
    def __init__(self, args, timeout=10):
        self.args = args
        self.timeout = timeout
        # Encoding the external program likes to receive.
        self.in_encoding = 'utf-8'
        # Encoding the external program will emit.
        self.out_encoding = 'utf-8'

        self._proc = None

    def encode(self, text):
        return text.encode(self.in_ecoding)

    def decode(self, encoded_bytes):
        return encoded_bytes.decode(self.out_encoding)

    def clean(self, text):
        return text.replace('\r', '').rstrip()

    def _start(self):
        try:
            self._proc = Popen(self.args,
                               stdout=PIPE,
                               stderr=PIPE,
                               stdin=PIPE,
                               startupinfo=supress_window())
        except OSError as e:
            _logger.error('while starting text filter program: %s', e)
            return

    def filter(self, input_text):
        self._start()
        try:
            in_bytes = input_text.encode(self.in_encoding)
            out_bytes, err_bytes = self._proc.communicate(in_bytes,
                                                          self.timeout)
            if err_bytes:
                _logger.error('while filtering text: %s',
                    self.clean(self.decode(err_bytes)))
                return

            return self.clean(self.decode(out_bytes))

        except TimeoutExpired:
            _logger.debug('text filter program response timed out')
            return

        except Exception as e:
            _logger.error('while running TextFilter: %s', e)
            return
