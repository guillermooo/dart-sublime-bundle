import logging

import sublime


LOG_LEVEL = None


def plugin_loaded():
    """ Runs when this file has been loaded by Sublime Text.
    """
    global LOG_LEVEL
    LOG_LEVEL = _get_logging_level()


def _get_logging_level():
    """ If `LOG_LEVEL` has already been set, it returns that.
    Otherwise, it gets its value from the settings.
    """
    global LOG_LEVEL

    if LOG_LEVEL is not None:
        return LOG_LEVEL

    v = sublime.active_window().active_view()
    level = v.settings().get('dart_log_level', 'ERROR')

    return getattr(logging, level.upper(), logging.ERROR)


class PluginLogger(object):
    """A logger intented to be used from plugin files inside this package.
    """
    def __init__(self, name):
        self.logger = self._new_logger(name)

    def _print(self, msg):
        # Give feedback if the api isn't ready yet. Otherwise messages logged
        # while the plugin is loading would go unnoticed.
        if LOG_LEVEL is None:
            print("Dart temp logger: ", msg)

    def debug(self, msg, *args, **kwargs):
        self._print(msg)
        self.logger().debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._print(msg)
        self.logger().info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._print(msg)
        self.logger().warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._print(msg)
        self.logger().error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._print(msg)
        self.logger().critical(msg, *args, **kwargs)

    def _make_logger(self, name):
        """ Returns a new configured logger.

        @name
          The name of the logger, typically a module path.
        """
        logger = logging.getLogger(name)
        logger.setLevel(LOG_LEVEL)
        return logger

    # TODO(guillermooo): Consider using a config file to avoid ST3 api issue.
    #
    # Works around ST3 delayed loading of plugins. We cannot call the API until
    # after the plugin file has been loaded. We just need the api to retrieve
    # the setting indicating the logging level.
    def _new_logger(self, name):
        """ Returns a generator that in turn returns a valid logger for @name
        each time it's called. Once the ST3 API is active, the generator will
        always return the same logger. In the meantime, it will return a logger
        with a default config so calls to it won't fail for levels ERROR+.
        """
        _logger = None

        def loggers():
            nonlocal _logger
            while True:
                try:
                    if _logger is None:
                        _logger = self._make_logger(name)
                    yield _logger
                except TypeError:
                    temp_logger = logging.getLogger(name)
                    temp_logger.setLevel(logging.ERROR)
                    yield temp_logger

        return lambda: next(loggers())
