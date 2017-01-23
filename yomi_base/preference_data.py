# -*- coding: utf-8 -*-

import codecs
import json
import operator
import os
import collections

def update(d, u):
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


class Preferences(object):
    def __init__(self):
        self.filename = os.path.expanduser('~/.yomichan.json')
        self.defaults = os.path.join(os.path.dirname(__file__), 'defaults.json')
        self.settings = dict()


    def __getitem__(self, name):
        return self.settings.get(name)


    def __setitem__(self, name, value):
        self.settings[name] = value

    def __delitem__(self, name):
        del self.settings[name]

    def load(self):
        with codecs.open(self.defaults, 'rb', 'utf-8') as fp:
            self.settings = json.load(fp)

        try:
            if os.path.exists(self.filename):
                with codecs.open(self.filename, 'rb', 'utf-8') as fp:
                    update(self.settings,json.load(fp))
            else:
                with codecs.open(self.defaults, 'rb', 'utf-8') as fp:
                    update(self.settings,json.load(fp))
            if 'vocab' in self['profiles']:
                self['profiles']['vocabulary'] = self['profiles']['vocab']
                del self['profiles']['vocab']
                
        except ValueError:
            pass


    def save(self):
        with codecs.open(self.filename, 'wb', 'utf-8') as fp:
            json.dump(self.settings, fp, indent=4, sort_keys=True, ensure_ascii=False)


    def filePosition(self, filename):
        matches = filter(lambda f: f['path'] == filename, self['recentFiles'])
        return 0 if len(matches) == 0 else matches[0]['position']


    def recentFiles(self):
        return map(operator.itemgetter('path'), self['recentFiles'])


    def updateFactTags(self, tags):
        if tags in self['tags']:
            self['tags'].remove(tags)
        self['tags'].insert(0, tags)


    def updateRecentFile(self, filename, position):
        self['recentFiles'] = filter(lambda f: f['path'] != filename, self['recentFiles'])
        self['recentFiles'].insert(0, {'path': filename, 'position': position})


    def clearRecentFiles(self):
        self['recentFiles'] = list()
