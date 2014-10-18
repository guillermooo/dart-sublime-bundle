# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)



class FatalError(Exception):
    '''An error from which we cannot recover.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class FatalConfigError(FatalError):
    '''Something with the configuration is really wrong.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ConfigError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
