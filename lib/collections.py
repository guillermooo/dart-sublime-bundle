# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)


class CircularArray(object):
    def __init__(self, items):
        self._index = -1
        self._items = items

    def __iter__(self):
        return self

    def __next__(self):
        self._index += 1
        if self._index >= len(self._items):
            self._index = 0
        return self._items[self._index]

    def __len__(self):
        return len(self._items)
