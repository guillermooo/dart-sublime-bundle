# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)


from collections import Counter
import os
import glob


class CompletionsList(object):
    def __init__(self, items):
        self.items = items

    def __iter__(self):
        yield from self.items

    def iter_with_prefix(self, prefix, casesensitive=False):
        if casesensitive:
            yield from (item for item in self
                              if item.startswith(prefix))
        else: 
            yield from (item for item in self
                              if item.lower().startswith(prefix.lower()))


class FileSystemCompletion(object):
    def __init__(self, casesensitive=False):
        self.cached_items = None
        # path as provided by user
        self.user_path = None
        # TODO(guillermooo): set automatically based on OS
        self._casesensitive = casesensitive

    def do_refresh(self, new_path, force_refresh):
        seps_new = Counter(new_path)["/"]
        seps_old = Counter(self.user_path)["/"]
        if self.cached_items is None:
            self.user_path = os.path.abspath('.')
            return True
        # if we have 2 or more additional slashes, we can be sure the user
        # wants to drill down to a different directory.
        # if we had only 1 additional slash, it may indicate a directory, but
        # not necessarily any  user-driven intention of drilling down in the
        # dir hierarchy. This is because we return items with slashes to
        # indicate directories.
        if abs(seps_old - seps_new) > 1:
            return True
        return force_refresh

    def get_completions(self, path, force_refresh=False):
        # we are cycling through items in the same directory as last time,
        # so reuse the cached items
        if not self.do_refresh(path, force_refresh):
            cl = CompletionsList(self.cached_items)
            leaf = os.path.split(path)[1]
            return list(cl.iter_with_prefix(
                                        leaf,
                                        casesensitive=self._casesensitive)
                                        )

        # we need to refresh the cache, as we are in a different directory
        # now or we've been asked to nevertheless.
        abs_path = os.path.abspath(os.path.dirname(path))
        leaf = os.path.split(path)[1]
        self.user_path = path

        fs_items = glob.glob(self.user_path + '*')
        fs_items = self.process_items(fs_items)

        cl = CompletionsList(fs_items)
        self.cached_items = list(cl)

        return list(cl.iter_with_prefix(leaf,
                                        casesensitive=self._casesensitive))

    def process_items(self, items):
        processed = []
        is_dir = False
        for it in items:
            if os.path.isdir(it):
                is_dir = True
            leaf = os.path.split(it)[1]
            leaf = leaf if (not is_dir) else (leaf + "/")
            processed.append(self.escape(leaf))
            is_dir = False
        return processed

    @classmethod
    def escape(self, name):
        return name.replace(' ', '\\ ')

    @classmethod
    def unescape(self, name):
        return name.replace('\\ ', ' ')
