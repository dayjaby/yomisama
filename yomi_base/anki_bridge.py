# -*- coding: utf-8 -*-

import sys
import os
import time
import random
from PyQt6 import QtWidgets, QtCore, QtGui
import anki
import aqt
from anki.hooks import addHook
import anki.collection
from .yomichan import Yomichan
from .reader import MainWindowReader
from .file_state import FileState
from .scheduler import Scheduler
from .deckManager import DeckManager
from .errorHandler import ErrorHandler
# from .anki_server import AnkiConnect
from . import profiles
from .constants import extensions
from anki.utils import ids2str, int_time


class Anki:
    def createYomichanModel(self):
        models = self.collection().models
        if models.by_name(u'YomichanSentence') is None:
            model = models.new(u'YomichanSentence')
            model['css'] = """\
.card {
 font-family: arial;
 font-size: 22px;
 text-align: center;
 color: black;
 background-color: white;
}

.card1 { background-color: #ffff7f; }
.card2 { background-color: #efff7f; }
            """
            for field in [u'Expression',u'Translation',u'Reading']:
                models.addField(model,models.new_field(field))
            template = models.new_template(u'Production')
            template['qfmt'] = u'{{Translation}}'
            template['afmt'] = u'{{FrontSide}}<hr>{{Expression}}'
            models.addTemplate(model,template)
            models.add(model)
        if models.by_name(u'YomichanKanji') is None:
            model = models.new(u'YomichanKanji')
            model['css'] = """\
.card {
 font-family: arial;
 font-size: 22px;
 text-align: center;
 color: black;
 background-color: white;
}

.card1 { background-color: #dfffff; }
.card2 { background-color: #ffafaf; }
            """
            for field in [u'Kanji',u'Onyomi',u'Kunyomi',u'Glossary',u'Words']:
                models.addField(model,models.new_field(field))
            template = models.new_template(u'Recognition')
            template['qfmt'] = u'{{Kanji}}'
            template['afmt'] = u'{{FrontSide}}<hr>{{Glossary}}<br>{{Onyomi}} {{Kunyomi}}'
            models.addTemplate(model,template)
            template = models.new_template(u'Production')
            template['qfmt'] = u"""<span id="glossary">{{Glossary}}</span><br>{{Onyomi}} {{Kunyomi}}<br><br>
<span id="words">{{furigana:Words}}</span>
<script>
kanji = "{{Kanji}}";
document.getElementById("words").innerHTML = document.getElementById("words").innerHTML.split(kanji).join("~");
</script>
"""
            template['afmt'] = u'{{FrontSide}}<hr>{{Kanji}}'
            models.addTemplate(model,template)
            models.add(model)
        if models.by_name(u'Yomichan') is None:
            model = models.new(u'Yomichan')
            model['css'] = """\
.card {
 font-family: arial;
 font-size: 22px;
 text-align: center;
 color: black;
 background-color: white;
}

.card1 { background-color: #ffff7f; }
.card2 { background-color: #efff7f; }
            """
            for field in [u'Vocabulary-Furigana',u'v',u'Vocabulary-English',u'Expression',u'Reading',u'Sentence-English',u'Video',u'Examples+']:
                models.addField(model,models.new_field(field))
            template = models.new_template(u'Recognition')
            template['qfmt'] = u'<span style="font-size: 60px">{{v}}</span><br><br><br>\n<span style="font-size: 20px; font-family: \uff2d\uff33 \u30b4\u30b7\u30c3\u30af;">{{kanji:Reading}}</span>\n{{^Reading}}\n<span style="font-size: 20px;">{{kanji:Expression}}</span>\n{{/Reading}}'
            template['afmt'] = u'<span style="font-size: 50px; font-family: \uff2d\uff33 \u30b4\u30b7\u30c3\u30af;">{{furigana:Vocabulary-Furigana}}</span><br>\n{{^Vocabulary-Furigana}}\n<span style="font-size: 30px"></span><br>\n<span style="font-size: 60px">{{v}}</span><br><br>\n{{/Vocabulary-Furigana}}\n<span style="font-size: 20px; font-family: \uff2d\uff33 \u30b4\u30b7\u30c3\u30af;">{{furigana:Reading}}</span><br>\n{{^Reading}}\n<span style="font-size: 20px;">{{furigana:Expression}}</span>\n{{/Reading}}\n<hr id=answer>\n<img src="{{Video}}"/><br>\n<span style="font-size: 12px; ">{{Vocabulary-English}}</span> <span style="font-size: 15px; color: #5555ff"></span><br>\n<br>\n<span style="font-size: 15px; ">{{Sentence-English}}</span>\n'
            models.addTemplate(model,template)
            models.add(model)

        # Create decks if non-existing
        decks = self.collection().decks
        decks.id(u'Yomichan')
        decks.id(u'YomichanCards')
            
            
    def addNote(self, deckName, modelName, fields, tags=list()):
        note = self.createNote(deckName, modelName, fields, tags)
        if note is not None:
            collection = self.collection()
            collection.addNote(note)
            collection.autosave()
            self.startEditing()
            return note.id


    def canAddNote(self, deckName, modelName, fields):
        return bool(self.createNote(deckName, modelName, fields))


    def createNote(self, deckName, modelName, fields, tags=list()):
        model = self.models().by_name(modelName)
        if model is None:
            return None

        deck = self.decks().by_name(deckName)
        if deck is None:
            return None
        note = anki.notes.Note(self.collection(), model)
        self.note = note
        note.model()['did'] = deck['id']
        note.tags = tags

        for name, value in fields.items():
            if name in note:
                note[name] = value

        if not note.dupeOrEmpty():
            return note


    def browse(self, query):
        browser = aqt.dialogs.open('Browser', self.window())
        browser.form.searchEdit.lineEdit().setText(u' '.join([u'{0}:{1}'.format(key,value) for key,value in query.items()]))
        browser.onSearchActivated()
        
    
    def getNotes(self, modelName, key, value):
        self.query = key + u':"' + value + u'" note:"' + modelName + u'"'
        return self.collection().findNotes(self.query)
        
        
    def getCards(self, modelName, onlyFirst = False):
        model = self.models().by_name(modelName)
        if model is not None:
            modelid = int(model[u"id"])
            query = "select " + ("min(c.id)" if onlyFirst else "c.id")
            query+= ",n.sfld,n.id from cards c "
            query+= "join notes n on (c.nid = n.id) " 
            query+= "where n.mid=%d" % (modelid)
            if onlyFirst: query+= "group by n.id"
            return self.collection().db.execute(query)
        else:
            return []
    
    def getCardsByNote(self, modelName, key, value):
        return self.collection().find_cards(key + u':"' + value + u'" note:' + modelName)

    def getCardsByNoteAndNotInDeck(self, modelName, values, did):
        model = self.models().by_name(modelName)
        modelid = int(model[u"id"])
        query = u"select c.id from cards c "
        query+= u"join notes n on (c.nid = n.id) " 
        query+= u"where n.mid=%d " % (modelid)
        query+= u"and c.did!=%d " % (did)
        query+= u"and n.sfld in " + (u"(%s)" % u",".join([u"'%s'"%(s) for s in values]))
        self.query = query
        return self.collection().db.execute(query)
        
    
    def getModelKey(self, modelName):
        model = self.collection().models.by_name(modelName)
        if model is None:
            return None
        frstfld = model[u"flds"][0]
        return frstfld[u"name"]
        

    def startEditing(self):
        # TODO: Maybe replace with CollectionOp?
        # self.window().requireReset()
        pass

    def stopEditing(self):
        if self.collection():
            pass
            # TODO: Maybe replace with CollectionOp?
            # self.window().maybeReset()

    def window(self):
        return aqt.mw


    def addUiAction(self, action):
        self.window().form.menuTools.addAction(action)


    def collection(self):
        return self.window().col


    def models(self):
        return self.collection().models


    def modelNames(self):
        return [model.name for model in self.models().all_names_and_ids()]


    def modelFieldNames(self, modelName):
        model = self.models().by_name(modelName)
        if model is not None:
            return [field['name'] for field in model['flds']]


    def decks(self):
        return self.collection().decks


    def deckNames(self):
        return [deck.name for deck in self.decks().all_names_and_ids()]
    
    def moveCards(self,cardKeys,model,deck):
        key = self.getModelKey(model)                                                  
        did = self.collection().decks.id(deck)
        cids = [int(cid[0]) for cid in self.getCardsByNoteAndNotInDeck(model,cardKeys,did)]
        self.updateCards(cids,did)
        
    def updateCards(self,cids,did):
        deck = self.collection().decks.get(did)
        self.window().checkpoint(_("Update cards"))
        if not deck['dyn']:
            mod = int_time()
            usn = self.collection().usn()
            scids = ids2str(cids)
            self.collection().sched.remFromDyn(cids)
            self.collection().db.execute("""update cards set usn=?, mod=?, did=? where id in """ + scids, usn, mod, did)
        # TODO: Maybe replace with CollectionOp?
        # self.window().requireReset()


class YomichanPlugin(Yomichan):
    def __init__(self):
        Yomichan.__init__(self)

        self.toolIconVisible = False
        self.window = None
        self.anki = Anki()
        self.fileCache = dict()
        # self.ankiConnect = AnkiConnect(self, self.preferences)
        self.parent = None #self.anki.window()

        separator = QtWidgets.QAction(self.anki.window())
        separator.setSeparator(True)
        self.anki.addUiAction(separator)
        self.profiles = profiles.getAllProfileClasses()
        self.preventReload = False
        action = QtWidgets.QAction(QtGui.QIcon(':/img/img/icon_logo_32.png'), '&Yomichan...', self.anki.window())
        action.setIconVisibleInMenu(True)
        action.setShortcut('Ctrl+Y')
        action.triggered.connect(self.onShowRequest)
        self.anki.addUiAction(action)


    def onShowRequest(self):

        if self.window:
            self.window.setVisible(True)
            self.window.activateWindow()
        else:
            self.window = MainWindowReader(
                self,
                self.parent,
                self.preferences,
                self.languages,
                self.anki,
                self.onWindowClose
            )
            self.window.show()


    def fetchAllCards(self):
        if self.anki is None:
            return None
        allCards = dict()
        for p in self.profiles:
            profile = self.preferences['profiles'].get(p)
            d = dict()
            if profile is None:
                continue
            for cid,value,nid in self.anki.getCards(profile["model"]):
                if value not in d:
                    d[value] = self.anki.collection().get_card(cid)
            allCards[p] = d
                
        return allCards


    def loadAllTexts(self,rootDir=None):
        if not hasattr(self,'i'):
            self.i = 0
        self.i += 1
        if rootDir is None:
            rootDir = u"Yomichan"
        
        oldCache = self.fileCache
        self.fileCache = dict()
        self.allCards = self.fetchAllCards()
        if self.allCards is not None:
            mediadir = self.anki.collection().media.dir()
            yomimedia = os.path.join(mediadir,rootDir)
            def processFile(file,relDir):
              if file[-4:] in extensions['text']:
                  path = os.path.join(relDir,file)
                  fullPath = u'::'.join(path.split(os.sep))
                  if fullPath in oldCache:
                      fileState = oldCache[fullPath]
                      fileState.load()
                  else:
                      fileState = FileState(os.path.join(mediadir,path),self.preferences['stripReadings'],profiles=self.profiles)
                  self.fileCache[fullPath] = fileState
                  # create deck if necessary
                  self.anki.collection().decks.id(fullPath,create=True)
                  fileState.findVocabulary(self.anki.collection().sched,self.allCards,needContent=False)

            if os.path.isdir(yomimedia):
                for root,dirs,files in os.walk(yomimedia):
                    relDir = os.path.relpath(root,mediadir)
                    for file in files:
                        processFile(file,relDir)
                    for dir in dirs:
                        path = os.path.join(relDir,dir)
                        self.fileCache[u'::'.join(path.split(os.sep))] = None
            elif os.path.isfile(yomimedia):
                processFile(os.path.basename(yomimedia),os.path.dirname(rootDir))
            


    def onWindowClose(self):
        self.window = None
        ### this becomes obsolote due to onAfterStateChange
        #if not sum(list(aqt.mw.col.sched.counts())):
        #    aqt.mw.moveToState('deckBrowser')
        
        
        
    def getFileCache(self):
        return self.fileCache


yomichanInstance = YomichanPlugin()


def onBeforeStateChange(state, oldState, *args):
    yomichanInstance.newestState = state
    yomichanInstance.anki.createYomichanModel()
    if not getattr(aqt.mw.col.decks,"customDeckManager",None):
        aqt.mw.col.decks = DeckManager(aqt.mw.col,yomichanInstance.getFileCache())
    if not getattr(aqt.mw.errorHandler,"customErrorHandler",None):
        aqt.mw.errorHandler = ErrorHandler(aqt.mw)
    if state == 'overview':
        did = aqt.mw.col.decks.selected()
        name = aqt.mw.col.decks.name_if_exists(did)
        path = name.split(u'::')
        if len(path) > 0 and path[0] == u'Yomichan':
            yomichanInstance.onShowRequest()
            completePath = aqt.mw.col.media.dir()
            for i in path:
                completePath = os.path.join(completePath,i)
            # if clicked on a directory, choose deck with most due cards
            if os.path.isdir(completePath):
                maxDue = 0
                maxDueDeck = None
                for name, id in aqt.mw.col.decks.children(did):
                    if aqt.mw.col.sched.dueCache[name] >= maxDue:
                        maxDue = aqt.mw.col.sched.dueCache[name]
                        maxDueDeck = name
                if maxDueDeck is None:
                    return
                path = maxDueDeck.split(u'::')
                completePath = aqt.mw.col.media.dir()
                for i in path:
                    completePath = os.path.join(completePath,i)
                if os.path.isdir(completePath):
                    return
            if yomichanInstance.window.state.filename != completePath:
                yomichanInstance.window.openFile(completePath)
                dirName = os.path.dirname(os.path.realpath(completePath))
                fileName = os.path.basename(os.path.splitext(completePath)[0])
                try:
                    for file in os.listdir(dirName):
                        if fileName == os.path.basename(os.path.splitext(file)[0]):
                            aqt.mw.isfile = os.path.join(dirName,file)
                        if fileName == os.path.basename(os.path.splitext(file)[0]) and os.path.isfile(os.path.join(dirName,file)):
                            extension = file[file.rfind("."):]
                            yomichanInstance.window.currentFile.loadedExtensions.append(extension)
                            if extension not in [".srt",".mkv",".mp4"] and extension not in extensions['text']:
                                openFile = os.path.join(dirName,file)
                                if sys.platform == 'linux2':
                                    subprocess.call(["xdg*-open", openFile])
                                else:
                                    aqt.mw.file = openFile
                                    os.startfile(openFile)
                except:
                    pass
                          
                for profile in yomichanInstance.window.profiles.values():
                    profile.afterFileLoaded()
                yomichanInstance.window.showMaximized()
    elif state == 'deckBrowser':
        if not getattr(aqt.mw.col.sched,"earlyAnswerCard",None):
            sched_variation_percent = yomichanInstance.preferences["scheduleVariationPercent"]
            week_days = yomichanInstance.preferences["weekDays"]
            def deck_due_tree(*args, **kwargs):
                raise Exception("deck_due_tree")
            aqt.mw.col.sched.deck_due_tree = deck_due_tree
            aqt.mw.col.sched = Scheduler(aqt.mw.col,
                yomichanInstance.getFileCache,
                scheduleVariationPercent=sched_variation_percent,
                weekDays=week_days)
        if yomichanInstance.preventReload:
            yomichanInstance.preventReload = False
        else:
            yomichanInstance.loadAllTexts()
        yomichanDeck = aqt.mw.col.decks.by_name(u'Yomichan')
        for name,id in aqt.mw.col.decks.children(yomichanDeck['id']):
            if name not in yomichanInstance.fileCache and aqt.mw.col.decks.get(id)['id']!=1:
                aqt.mw.col.decks.rem(id)
                
def onAfterStateChange(state, oldState, *args):
    if state == 'overview':
        did = aqt.mw.col.decks.selected()
        name = aqt.mw.col.decks.name_if_exists(did)
        path = name.split(u'::')
        if len(path) > 0 and path[0] == u'Yomichan':
            yomichanInstance.preventReload = True
            aqt.mw.moveToState('deckBrowser')

addHook('beforeStateChange',onBeforeStateChange)
addHook('afterStateChange',onAfterStateChange)
    
def searchYomichanDeck(val):
    yomichanInstance.searchPath = val.replace(u"::",os.sep)
    yomichanInstance.loadAllTexts(val.replace(u"::",os.sep))
    words = set()
    for text,state in yomichanInstance.fileCache.items():
        if state is not None:
            for k,profile in state.profiles.items():
                words |= set(profile['wordsAll'].keys())
    arg = "(" + ",".join(["\""+val+"\"" for val in words]) + ")"
    where = "(n.sfld in " + arg + ")"
    return where

def onSearch(cmds):
    def findByYomichanFile(oldfn):
        def inner(val, args=None):
            val, args = val
            if val.split("::")[0]=="Yomichan":
                return searchYomichanDeck(val)
            else:
                return oldfn((val,args))
        return inner    
    cmds['deck'] = findByYomichanFile(cmds['deck'])    
addHook('search',onSearch)
