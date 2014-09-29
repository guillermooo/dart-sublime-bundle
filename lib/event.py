from Dart import PluginLogger

_logger = PluginLogger(__name__)


class EventSource(object):
    ON_PUB_BUILD = 'on_pub_build_event'
    ON_DART_RUN = 'on_dart_run_event'

    handlers = {
        ON_PUB_BUILD: [],
        ON_DART_RUN: [],        
    }
    
    def raise_event(self, name, *args, **kwargs):
        for handler in EventSource.handlers.get(name, []):
            handler(source.__class__.__qualname__, *args, **kwargs)

    def add_event_handler(self, name, func):
      if name not in EventSource.handlers:
        raise KeyError('unknown event "{}"'.format(name))
      EventSource.handlers[name].append(func)
