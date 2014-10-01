'''
Google Analytics
'''
import sublime

import uuid
import os

import urllib.parse
import urllib.request
import random

from Dart import PluginLogger
from Dart.lib.sdk import SDK


_logger = PluginLogger(__name__)


class HitBase(object):
    def __init__(self):
        self._data = {}
        self._endpoint = "https://ssl.google-analytics.com/collect"

        setts = sublime.load_settings(
            'Dart - Plugin Settings.sublime-settings')
        self._enabled = setts.get('dart_enable_telemetry') is True

        # Test tracking id: UA-55288482-1
        self.tracking_id = 'UA-55288482-1'
        self.protocol_version = 1

        self.client_id = str(uuid.uuid4())
        self.hit_type = None

    @property
    def user_agent(self):
        # FIXME(guillermooo): This is probably wrong.
        ua = "ST-Dart-Plugin/{version} ({os}; {os}; {os}; {language})"
        data = {
            'os': os.name,
            'language': os.environ.get('LANG', 'unknown'),
            'version': SDK().check_version().strip(),
        }
        return ua.format(**data)

    def send(self, data):
        if not self._enabled:
            return
        payload = {
            'v': self.protocol_version,
            'tid': self.tracking_id,
            'aip': 1,
            'cid': self.client_id,
            't': self.hit_type,
            }
        payload.update(data)
        encoded = self.encode(payload)
        # Bust through cache. This param should come last.
        encoded += '&z=' + str(int(random.random() * 10000))
        _logger.debug('sending analytics payload: %s', encoded)
        encoded = encoded.encode('utf-8')
        r = urllib.request.Request(self._endpoint, data=encoded)
        r.add_header('User-Agent', self.user_agent)
        resp = urllib.request.urlopen(r)
        if 199 <= resp.status >= 300:
            _logger.error(
                'error sending analytics request. Code: %d', resp.status)
            raise SyntaxError('bad request')

    @property
    def protocol_version(self):
        return self._data['protocol_version']

    @protocol_version.setter
    def protocol_version(self, value):
        self._data['protocol_version'] = value

    @property
    def tracking_id(self):
        return self._data['tracking_id']

    @tracking_id.setter
    def tracking_id(self, value):
        self._data['tracking_id'] = value

    def encode(self, data):
        return urllib.parse.urlencode(data)


class Event(HitBase):
    def __init__(self, category, action, label, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert isinstance(value, int), 'wrong args'
        assert value > 0

        self.hit_type = 'event'
        self.category = category
        self.action = action
        self.label = label
        self.value = value

    def send(self):
        data = {
        'ec': self.category,
        'ea': self.action,
        'el': self.label,
        'ev': self.value,
        }
        super().send(data)