# Copyright (c) 2012, Benjamin Vanheuverzwijn <bvanheu@gmail.com>
# All rights reserved.
#
# Thanks to Marc-Etienne M. Leveille
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of pytoutv nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Benjamin Vanheuverzwijn BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import shelve
from datetime import datetime
from datetime import timedelta


class Cache:
    def __init__(self):
        pass

    def get_shows(self):
        pass

    def get_show_episodes(self, show_id):
        pass

    def get_page_repertoire(self):
        pass

    def set_shows(self, shows):
        pass

    def set_show_episodes(self, show_id, episodes):
        pass

    def set_page_repertoire(self, page_repertoire):
        pass

    def invalidate(self):
        pass


class EmptyCache(Cache):
    def get_shows(self):
        return None

    def get_show_episodes(self, show_id):
        return None

    def get_page_repertoire(self):
        return None


class ShelveCache(Cache):
    def __init__(self, shelve_filename):
        try:
            self.shelve = shelve.open(shelve_filename)
        except Exception as e:
            self.shelve = None
            raise e

    def __del__(self):
        if self.shelve is not None:
            self.shelve.close()

    def _has_key(self, key):
        if key in self.shelve:
            expire, value = self.shelve[key]
            if datetime.now() < expire:
                return True

        return False

    def _get(self, key):
        if not self._has_key(key):
            return None

        expire, value = self.shelve[key]

        return value

    def _set(self, key, value, expire=timedelta(hours=2)):
        self.shelve[key] = (datetime.now() + expire, value)

    def _del(self, key):
        if key in self.shelve:
            del shelve[key]

    def get_shows(self):
        return self._get('shows')

    def get_show_episodes(self, show):
        emid = show.Id
        show_episodes = self._get('show_episodes')
        if show_episodes is None:
            return None
        if emid not in show_episodes:
            return None

        return show_episodes[emid]

    def get_page_repertoire(self):
        return self._get('page_repertoire')

    def set_shows(self, shows):
        self._set('shows', shows)

    def set_show_episodes(self, show, episodes):
        emid = show.Id
        show_episodes = self._get('show_episodes')
        if show_episodes is None:
            show_episodes = {}
        show_episodes[emid] = episodes
        self._set('show_episodes', show_episodes)

    def set_page_repertoire(self, page_repertoire):
        self._set('page_repertoire', page_repertoire)

    def invalidate(self):
        self._del('shows')
        self._del('show_episodes')
        self._del('page_repertoire')
