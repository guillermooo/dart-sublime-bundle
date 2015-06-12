import sublime


# todo: move these tests to sublime_plugin_lib
class FlexibleSettingByPlatform(object):
    '''
    Base class.

    Data descriptor that encapsulates access to a Sublime Text setting that
    can take any of the following forms:

        Scalar value
        ======================================================================
        "color": "blue"
        ----------------------------------------------------------------------
        Dictionary keyed by platform
        ======================================================================
        "color" : {
            "windows": "blue",
            "linux": "orange",
            "osx": "green"
        }
        ----------------------------------------------------------------------

    This way, users can specify the same setting globally as a scalar value, or
    more granularly, by platform, and the plugin code can read it in the same
    way in both cases.

    For example:

        class SomeSettingsClass:
            path_to_thing = FlexibleSettingByPlatformSubclass(name='path_to_thing')

        settings = SomeSettingsClass()
        value = settings.path_to_thing

    Optionally, basic validation is configurable:

        class SomeSettingsClass:
            path_to_thing = FlexibleSettingByPlatformSubclass(name='path_to_thing', expected_type=str)

        settings = SomeSettingsClass()
        value = settings.path_to_thing

    Validation errors raise a ValueError.

    Subclasses must at a minimum implement the .get() method.
    '''

    def __init__(self, name, expected_type=None, default=None):
        self.name = name
        self.expected_type = expected_type
        self.default = default

    def __get__(self, obj, typ):
        if obj is None:
            return self

        scalar_or_dict = self.get(self.name)

        value = None
        try:
            value = scalar_or_dict[sublime.platform()]
        except TypeError:
            value = scalar_or_dict
        except KeyError:
            raise ValueError("no platform settings found for '%s' (%s)" % (self.name, sublime.platform()))

        value = value if (value is not None) else self.default

        value = self.validate(value)
        value = self.post_validate(value)
        return value

    def __set__(self, obj, val):
        raise NotImplementedException("can't do this now")

    def validate(self, value):
        if self.expected_type is None:
            return value
        assert isinstance(value, self.expected_type), 'validation failed for "%s". Got %s, expected %s' % (self.name, type(value), self.expected_type)
        return value

    def post_validate(self, value):
        '''
        Subclasses should override this method if they need to do any
        postprocessing after the the value has been gotten and validated.

        Returns a settings' value.
        '''
        return value

    def get(self, name):
        '''
        Abstract method.

        Subclasses must implement here access to self.name's setting top-level
        value (a scalar value or a dictionary).
        '''
        raise NotImplementedException('implement me')
