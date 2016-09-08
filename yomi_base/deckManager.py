# -*- coding: utf-8 -*-

# Copyright (C) 2016  David Jablonski
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import aqt
import anki.decks
import anki.utils
from anki.consts import *
import os,shutil
import copy
import yomi_base.anki_bridge
from yomi_base.constants import extensions

class DeckManager(anki.decks.DeckManager):
    customDeckManager = True

    def __init__(self,col,filecache):
        anki.decks.DeckManager.__init__(self,col)
        self.decks = col.decks.decks
        self.dconf = col.decks.dconf
        self.changed = col.decks.changed
        self.filecache = filecache

    def isYomiDeck(self, did):
        return self.get(did)["name"].split("::")[0]=="Yomichan"

    def get_yomi_cids(self, did):
        deck = self.get(did)
        return self.col.db.list("select c.id from cards c join notes n on n.id = c.nid where " + yomi_base.anki_bridge.searchYomichanDeck(deck["name"]))

    def cids(self, did, children=False):
        if self.isYomiDeck(did):
            return self.get_yomi_cids(did)
        else:
            return anki.decks.DeckManager.cids(self,did,children)

    def get_card_ids(self, did, children=False, include_from_dynamic=False):
        if self.isYomiDeck(did):
            return self.get_yomi_cids(did)
        else:
            deck_ids = [did] + ([deck_id for _, deck_id in self.children(did)] if children else [])
            request = "select id from cards where did in {}" + (" or odid in {}" if
                                                            include_from_dynamic else "")
            parameters = (anki.utils.ids2str(deck_ids),) + ((anki.utils.ids2str(deck_ids),) if include_from_dynamic else tuple())
            return self.col.db.list(request.format(*parameters))

    def createDeck(self,path):
        completePath = self.col.media.dir()
        for i in path[:-1]:
            completePath = os.path.join(completePath,i)
        fullPath = os.path.join(completePath,path[-1])
        if path[-1].endswith(extensions['text']):
            if not os.path.isdir(completePath):
                os.makedirs(completePath)
        elif not os.path.isdir(fullPath):
            os.makedirs(fullPath)
        if path[-1].endswith(extensions['text']) and not os.path.isfile(fullPath):
            f = open(fullPath,'w')
            f.close()
        return fullPath

    def id(self, name, create=True, type=anki.decks.defaultDeck):
        did = anki.decks.DeckManager.id(self,name,create,type)
        name = self.nameOrNone(did)
        if name is not None and create:
            path = name.split(u'::')
            if len(path) > 1 and path[0] == u'Yomichan':
                self.createDeck(path)
        return did

    def rem(self, did, cardsToo=False, childrenToo=True):
        name = self.nameOrNone(did)
        if name is not None:
            path = name.split(u'::')
            if len(path) > 1 and path[0] == u'Yomichan':
                completePath = self.col.media.dir()
                for i in path:
                    completePath = os.path.join(completePath,i)
                if os.path.isdir(completePath):
                    shutil.rmtree(completePath)
                elif os.path.isfile(completePath):
                    os.remove(completePath)
                    if name in self.filecache:
                        del self.filecache[name]
            if len(path) > 1 or path[0] != u'Yomichan':
                anki.decks.DeckManager.rem(self,did,cardsToo,childrenToo)

    def rename(self, g, name):
        path = name.split(u'::')
        gname = g['name'] # old name
        path2 = gname.split(u'::')
        isYomichan = len(path) > 1 and path[0] == u'Yomichan'
        isYomichan2 = len(path2) > 1 and path2[0] == u'Yomichan'
        isFile = name.endswith(extensions['text'])
        isFile2 = gname.endswith(extensions['text'])
        if isYomichan == isYomichan2 and isFile==isFile2:
            anki.decks.DeckManager.rename(self,g,name)
        elif isYomichan2 and not isYomichan:
            # when "renaming" a Yomichan deck to a non-Yomichan deck, 
            # create a filtered deck for the Yomichan deck
            dynParent = None
            if '::' in name:
                newParent = '::'.join(name.split('::')[:-1])
                newParentDeck = self.byName(newParent)
                if newParentDeck['dyn']:
                    dynParent = newParentDeck
            searchQuery = 'deck:\"%s\" (is:due or is:new)' % gname
            if dynParent:
                dynParent['terms'][0][0] = "({0}) or ({1})".format(dynParent['terms'][0][0],searchQuery)
                self.save(dynParent)
            else:
                dyn = copy.deepcopy(anki.decks.defaultDynamicDeck)
                dyn['terms'][0] = [searchQuery, DYN_MAX_SIZE, DYN_RANDOM]
                did = self.id(name,type=dyn)
                self.debug = self.get(did)
                aqt.mw.col.sched.rebuildDyn(did)
        else:
            # don't allow renaming of non-Yomichan deck to Yomichan deck
            if '::' in name:
                newParent = '::'.join(name.split('::')[:-1])
                if self.byName(newParent)['dyn']:
                    raise DeckRenameError(_("A filtered deck cannot have subdecks."))
        if isYomichan and isYomichan2 and (isFile==isFile2):
            root_dst_dir = self.createDeck(path)
            root_src_dir = self.col.media.dir()
            for i in path2:
                root_src_dir = os.path.join(root_src_dir,i)
            if root_src_dir.endswith(extensions['text']):
                shutil.move(root_src_dir, root_dst_dir)
            else:
                for src_dir, dirs, files in os.walk(root_src_dir):
                    dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
                    if not os.path.exists(dst_dir):
                        os.makedirs(dst_dir)
                    for file_ in files:
                        src_file = os.path.join(src_dir, file_)
                        dst_file = os.path.join(dst_dir, file_)
                        if os.path.exists(dst_file):
                            os.remove(dst_file)
                        shutil.move(src_file, dst_dir)
            if gname in self.filecache:
                self.filecache[name] = self.filecache[gname]
                del self.filecache[gname]
            elif not gname.endswith(extensions['text']):
                for file in self.filecache:
                    if file.startswith(gname+'::'):
                        nname = file.replace(gname+'::',name+'::',1)
                        self.filecache[nname] = self.filecache[gname]
                        del self.filecache[gname]
            aqt.mw.moveToState("deckBrowser")
