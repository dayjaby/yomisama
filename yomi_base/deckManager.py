import aqt
import anki.decks
import os,shutil
import yomi_base.anki_bridge

class DeckManager(anki.decks.DeckManager):
    customDeckManager = True

    def __init__(self,col,filecache):
        anki.decks.DeckManager.__init__(self,col)
        self.decks = col.decks.decks
        self.dconf = col.decks.dconf
        self.changed = col.decks.changed
        self.filecache = filecache
        
    def cids(self, did, children=False):
        deck = self.get(did)
        if deck["name"].split("::")[0]=="Yomichan":
            return self.col.db.list("select c.id from cards c join notes n on n.id = c.nid where " + yomi_base.anki_bridge.searchYomichanDeck(deck["name"]))
        else:
            return anki.decks.DeckManager.cids(self,did,children)

        
    def createDeck(self,path):
        completePath = self.col.media.dir()
        for i in path[:-1]:
            completePath = os.path.join(completePath,i)
        fullPath = os.path.join(completePath,path[-1])
        if path[-1].endswith(".txt"):
            if not os.path.isdir(completePath):
                os.makedirs(completePath)
        elif not os.path.isdir(fullPath):
            os.makedirs(fullPath)
        if path[-1].endswith(".txt") and not os.path.isfile(fullPath):
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
        gname = g['name']
        path2 = gname.split(u'::')
        isYomichan = len(path) > 1 and path[0] == u'Yomichan'
        isYomichan2 = len(path2) > 1 and path2[0] == u'Yomichan'
        isFile = name.endswith('.txt')
        isFile2 = gname.endswith('.txt')
        if isYomichan == isYomichan2 and isFile==isFile2:
            anki.decks.DeckManager.rename(self,g,name)
        else:
            pass # don't allow renaming of Yomichan deck to non-Yomichan deck and vice-versa
        if isYomichan and isYomichan2 and (isFile==isFile2):
            root_dst_dir = self.createDeck(path)
            root_src_dir = self.col.media.dir()
            for i in path2:
                root_src_dir = os.path.join(root_src_dir,i)
            if root_src_dir.endswith(".txt"):
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
            elif not gname.endswith('.txt'):
                for file in self.filecache:
                    if file.startswith(gname+'::'):
                        nname = file.replace(gname+'::',name+'::',1)
                        self.filecache[nname] = self.filecache[gname]
                        del self.filecache[gname]
            aqt.mw.moveToState("deckBrowser")