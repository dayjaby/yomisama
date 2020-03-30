# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui
from anki.utils import ids2str, intTime
import os
import io
import aqt
import sys
from . import preferences
from . import reader_util
from . import updates
from . import about
from . import constants
from .gen import reader_ui
from . import profiles
from .file_state import FileState
from .constants import extensions


class Container(object):
        pass
                
class MyKeyFilter(QtCore.QObject):
    obj = None
    
    def eventFilter(self, unused, event):
        obj = self.obj
        if event.type() != QtCore.QEvent.KeyPress:
            return False
        if QtCore.Qt.Key_F1 == event.key() and event.modifiers() & QtCore.Qt.ControlModifier:
            obj.executeDefCommand('sentence_add',0)
        elif event.key() == preferences.lookupKeys[obj.preferences['lookupKey']][1]:
            obj.updateSampleFromPosition()
        elif (event.key() == QtCore.Qt.Key_W and event.modifiers() & QtCore.Qt.AltModifier):
            obj.createAlias()
        elif (event.key() == QtCore.Qt.Key_S and event.modifiers() & QtCore.Qt.AltModifier):
            obj.createSubscription()
        elif (event.key() == QtCore.Qt.Key_R and event.modifiers() & QtCore.Qt.AltModifier):
            obj.restoreRecentIncorrect()
        elif (event.key() == QtCore.Qt.Key_N and event.modifiers() & QtCore.Qt.AltModifier):
            obj.showNotFoundWords()
        elif ord('0') <= event.key() <= ord('9') and obj.anki is not None:
            index = (event.key() - ord('0') - 1) % 10
            if event.modifiers() & QtCore.Qt.ShiftModifier:
                if event.modifiers() & QtCore.Qt.ControlModifier:
                    obj.executeDefCommand('kanji_add', index)
                else:
                    return False
            else:
                if event.modifiers() & QtCore.Qt.ControlModifier:
                    obj.executeDefCommand('vocabulary_add', index)
                elif event.modifiers() & QtCore.Qt.AltModifier:
                    obj.executeDefCommand('vocabulary_add_reading', index)
                else:
                    return False
        elif event.key() == ord('[') and obj.state.scanPosition > 0:
            obj.state.scanPosition -= 1
            obj.updateSampleFromPosition()
        elif event.key() == ord(']') and obj.state.scanPosition < len(obj.textContent.toPlainText()) - 1:
            obj.state.scanPosition += 1
            obj.updateSampleFromPosition()
        else:
            return False
        return True


class MainWindowReader(QtWidgets.QMainWindow, reader_ui.Ui_MainWindowReader):
            
                
    class State:
        def __init__(self):
            self.filename = ""
            self.scanPosition = 0
            self.searchPosition = 0
            self.searchText = ""


    def __init__(self, plugin, parent, preferences, languages, anki=None, closed=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.debug = []
        self.setupUi(self)
        self.parent = parent
        self.textContent.mouseMoveEvent = self.onContentMouseMove
        self.textContent.mousePressEvent = self.onContentMousePress
        self.dockAnki.setEnabled(anki is not None)
        self.currentFile = None
        self.plugin = plugin
        self.preferences = preferences
        self.anki = anki
        self.facts = list()
        self.recentIncorrect = None
        self.listDefinitions.clear()
        self.closed = closed
        self.languages = languages
        self.state = self.State()
        self.updates = updates.UpdateFinder()
        self.zoom = 0
        self.updateRecentFiles()


        self.actionAbout.triggered.connect(self.onActionAbout)
        self.actionFeedback.triggered.connect(self.onActionFeedback)
        self.actionFind.triggered.connect(self.onActionFind)
        self.actionFindNext.triggered.connect(self.onActionFindNext)
        self.actionHomepage.triggered.connect(self.onActionHomepage)
        self.actionKindleDeck.triggered.connect(self.onActionKindleDeck)
        self.actionWordList.triggered.connect(self.onActionWordList)
        self.actionOpen.triggered.connect(self.onActionOpen)
        self.actionSave.triggered.connect(self.onActionSave)
        self.actionPreferences.triggered.connect(self.onActionPreferences)
        self.actionToggleWrap.toggled.connect(self.onActionToggleWrap)
        self.actionToggleJapanese.toggled.connect(self.onActionToggleLanguage("japanese"))
        self.actionToggleKorean.toggled.connect(self.onActionToggleLanguage("korean"))
        self.actionToggleChinese.toggled.connect(self.onActionToggleLanguage("chinese"))
        self.actionToggleGerman.toggled.connect(self.onActionToggleLanguage("german"))
        self.actionToggleSpanish.toggled.connect(self.onActionToggleLanguage("spanish"))
        self.actionToggleFrench.toggled.connect(self.onActionToggleLanguage("french"))
        self.actionZoomIn.triggered.connect(self.onActionZoomIn)
        self.actionZoomOut.triggered.connect(self.onActionZoomOut)
        self.actionZoomReset.triggered.connect(self.onActionZoomReset)
        self.dockAnki.visibilityChanged.connect(self.onVisibilityChanged)
        if self.anki is not None:
            self.learnVocabulary.clicked.connect(self.onLearnVocabularyList)
            self.removeVocabulary.clicked.connect(self.onRemoveVocabulary)
        self.listDefinitions.itemDoubleClicked.connect(self.onDefinitionDoubleClicked)
        self.updates.updateResult.connect(self.onUpdaterSearchResult)

        self.keyFilter = MyKeyFilter()
        self.keyFilter.obj = self
        self.installEventFilter(self.keyFilter)
        self.textContent.installEventFilter(self.keyFilter)
        
        if self.preferences['checkForUpdates']:
            self.updates.start()
        self.profiles = profiles.getAllProfiles(self)
        for profile in self.profiles.values():
            profile.updateDefinitions()
        if self.preferences['rememberTextContent']:
            self.textContent.setPlainText(self.preferences['textContent'])
        elif self.anki is not None:
            self.currentFile = FileState(None, self.preferences['stripReadings'],self.languages,self.profiles)

        self.applyPreferences()

            
    def getSortedProfiles(self):
        def sortFunction(profile):
            return profile.sortIndex
        return sorted(self.profiles.values(),key=sortFunction)

    def onRemoveVocabulary(self):
        row = self.listDefinitions.currentRow()
        word = self.facts[row]['word']
        profile = self.facts[row]['profile']
        self.listDefinitions.takeItem(row)
        if word in self.currentFile.profiles[profile]['wordsAll']:
            del self.currentFile.profiles[profile]['wordsAll'][word]
        if word in self.currentFile.profiles[profile]['wordsBad']:
            del self.currentFile.profiles[profile]['wordsBad'][word]
        self.setStatus(u'Removed {0} from vocabulary list'.format(word))
    
    def onLearnVocabularyList(self):
        if self.anki is None:
            return
        self.currentFile.onLearnVocabularyList(self.anki.collection().sched)
        totalSeconds = int(self.currentFile.timeTotal) %  60
        totalMinutes = int(self.currentFile.timeTotal) // 60
        perCardSeconds = int(self.currentFile.timePerWord) %  60
        perCardMinutes = int(self.currentFile.timePerWord) // 60
        QtWidgets.QMessageBox.information(
            self,
            'Yomichan', '{0} correct and {1} wrong\n{2} minutes {3} seconds for all\n{4} minutes {5} seconds per card'
            .format(self.currentFile.correct,self.currentFile.wrong,
                totalMinutes,totalSeconds,
                perCardMinutes,perCardSeconds)
        )


    def applyPreferences(self):
        if self.preferences['windowState'] is not None:
            self.restoreState(QtCore.QByteArray.fromBase64(self.preferences['windowState'].encode("utf-8")))
        if self.preferences['windowPosition'] is not None:
            self.move(QtCore.QPoint(*self.preferences['windowPosition']))
        if self.preferences['windowSize'] is not None:
            self.resize(QtCore.QSize(*self.preferences['windowSize']))

        self.comboTags.addItems(self.preferences['tags'])
        self.applyPreferencesContent()

        if self.preferences['firstRun']:
            QtWidgets.QMessageBox.information(
                self,
                'Yomichan',
                'This may be the first time you are running Yomichan.\nPlease take some time to configure this extension.'
            )

            self.onActionPreferences()

    def applyPreferencesContent(self):
        palette = self.textContent.palette()
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(self.preferences['bgColor']))
        palette.setColor(QtGui.QPalette.Text, QtGui.QColor(self.preferences['fgColor']))
        self.textContent.setPalette(palette)

        self.textContent.setReadOnly(not self.preferences['allowEditing'])
        self.textContent.setAttribute(QtCore.Qt.WA_InputMethodEnabled)

        font = self.textContent.font()
        font.setFamily(self.preferences['fontFamily'])
        font.setPointSize(self.preferences['fontSize'] + self.zoom)
        self.textContent.setLineWrapMode(QtWidgets.QPlainTextEdit.WidgetWidth if self.preferences['wordWrap'] else QtWidgets.QPlainTextEdit.NoWrap)
        self.textContent.setFont(font)

        self.actionToggleWrap.setChecked(self.preferences['wordWrap'])
        self.actionToggleJapanese.setChecked(self.preferences['japanese'])
        self.actionToggleKorean.setChecked(self.preferences['korean'])
        self.actionToggleChinese.setChecked(self.preferences['chinese'])
        self.actionToggleGerman.setChecked(self.preferences['german'])
        self.actionToggleSpanish.setChecked(self.preferences['spanish'])
        self.actionToggleFrench.setChecked(self.preferences['french'])

    def closeEvent(self, event):
        self.preferences['windowState'] = str(self.saveState().toBase64())
        self.closeFile()
        self.preferences.save()

        if self.anki is not None:
            self.anki.stopEditing()

        if self.closed is not None:
            self.closed()
            
        for key,profile in self.profiles.items():
            profile.close()

            


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()


    def dropEvent(self, event):
        url = event.mimeData().urls()[0]
        self.openFile(url.toLocalFile())

        
    def moveEvent(self, event):
        self.preferences['windowPosition'] = event.pos().x(), event.pos().y()


    def resizeEvent(self, event):
        self.preferences['windowSize'] = event.size().width(), event.size().height()

    def getFileFilter(self):
        return ';;'.join(
            ['Text files (' + 
             ' '.join(map(lambda x:'*'+x,extensions['text'])) +')',
             'All files (*.*)'])


    def onActionOpen(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a file to open',
            directory=self.state.filename,
                filter=self.getFileFilter()
        )
        if filename:
            self.openFile(filename)
    
    def onActionSave(self):
        filename, filter_str = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            caption='Select a file to save',
            directory=self.state.filename,
            filter=self.getFileFilter()
        )
        if filename:
            self.saveFile(filename)
    

    def onActionKindleDeck(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a Kindle deck to import',
            filter='Deck files (*.db)'
        )
        if filename:
            words = reader_util.extractKindleDeck(filename)
            self.importWordList(words)


    def onActionWordList(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a word list file to import',
            filter=self.getFileFilter()
        )
        if filename:
            words = reader_util.extractWordList(filename)
            self.importWordList(words)
                                            
          
    def onActionPreferences(self):
        dialog = preferences.DialogPreferences(self, self.preferences, self.anki, self.profiles)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.applyPreferencesContent()


    def onActionAbout(self):
        dialog = about.DialogAbout(self)
        dialog.exec_()


    def onActionZoomIn(self):
        font = self.textContent.font()
        if font.pointSize() < 72:
            font.setPointSize(font.pointSize() + 1)
            self.textContent.setFont(font)
            self.zoom += 1


    def onActionZoomOut(self):
        font = self.textContent.font()
        if font.pointSize() > 1:
            font.setPointSize(font.pointSize() - 1)
            self.textContent.setFont(font)
            self.zoom -= 1


    def onActionZoomReset(self):
        if self.zoom:
            font = self.textContent.font()
            font.setPointSize(font.pointSize() - self.zoom)
            self.textContent.setFont(font)
            self.zoom = 0


    def onActionFind(self):
        searchText = self.state.searchText

        cursor = self.textContent.textCursor()
        if cursor.hasSelection():
            searchText = cursor.selectedText()

        searchText, ok = QtWidgets.QInputDialog.getText(self, 'Find', 'Search text:', text=searchText)
        if searchText and ok:
            self.findText(searchText)


    def onActionFindNext(self):
        if self.state.searchText:
            self.findText(self.state.searchText)


    def onActionToggleWrap(self, wrap):
        self.preferences['wordWrap'] = wrap
        self.textContent.setLineWrapMode(QtWidgets.QPlainTextEdit.WidgetWidth if self.preferences['wordWrap'] else QtWidgets.QPlainTextEdit.NoWrap)

    def onActionToggleLanguage(self, language):
        def inner(enable):
            self.preferences[language] = enable
            if language not in self.languages and enable:
                self.plugin.loadLanguage(language,callback=None)
            elif language in self.languages and not enable:
                del self.languages[language]
        return inner
            
    def onActionHomepage(self):
        url = QtCore.QUrl('http://dayjaby.wordpress.com')
        QtWidgets.QDesktopServices().openUrl(url)


    def onActionFeedback(self):
        url = QtCore.QUrl('http://dayjaby.wordpress.com')
        QtWidgets.QDesktopServices().openUrl(url)


    def onDefinitionDoubleClicked(self, item):
        row = self.listDefinitions.row(item)
        profile = self.preferences['profiles'].get(self.facts[row]['profile'])
        if profile is not None and self.anki is not None:
            key = self.anki.getModelKey(profile['model'])
            self.anki.browse({key:u'"'+self.facts[row]['word']+u'"',u'note':profile['model']})


    def onVisibilityChanged(self, visible):
        self.actionToggleAnki.setChecked(self.dockAnki.isVisible())


    def onUpdaterSearchResult(self, versions):
        if versions['latest'] > constants.c['appVersion']:
            dialog = updates.DialogUpdates(self, versions)
            dialog.exec_()


    def onContentMouseMove(self, event):
        QtWidgets.QPlainTextEdit.mouseMoveEvent(self.textContent, event)
        self.updateSampleMouseEvent(event)


    def onContentMousePress(self, event):
        QtWidgets.QPlainTextEdit.mousePressEvent(self.textContent, event)
        self.updateSampleMouseEvent(event)

    def findTerm(self, text, wildcards=False):
        maxLength = 0
        self.profiles["vocabulary"].definitions = []
        for key, language in self.languages.items():
            if self.preferences[key]:
                vocabDefs, length = language.findTerm(text, wildcards)
                self.profiles["vocabulary"].definitions += vocabDefs
                if length is not None and length > maxLength:
                    maxLength = length
        return maxLength


    def openFile(self, filename):
        self.closeFile()
        try:
            self.currentFile = FileState(filename, self.preferences['stripReadings'],self.languages,self.profiles)
        except IOError:
            self.setStatus(u'Failed to load file {0}'.format(filename))
            QtWidgets.QMessageBox.critical(self, 'Yomichan', 'Cannot open file for read')
            return
        self.listDefinitions.clear()
        self.facts = []

        self.updateRecentFile()
        self.updateRecentFiles()

        allCards = self.plugin.fetchAllCards()
        if allCards is not None:
            self.currentFile.findVocabulary(self.anki.collection().sched,allCards)
            # if file contains exported vocabs, create the cards
            for k,profile in self.currentFile.profiles.items():
                if self.currentFile.exportedVocab:
                    for notFound in profile['wordsNotFound']:
                        self.ankiAddFact(k,profile['wordsMarkup'][notFound],addToList=False)
                for word,card in profile['wordsAll'].items():
                    self.facts.append({'word':word,'profile':k})
                    self.listDefinitions.addItem(word)
            self.listDefinitions.setCurrentRow(self.listDefinitions.count() - 1)

        content = self.currentFile.content
        self.state.filename = filename
        self.state.scanPosition = self.preferences.filePosition(filename)
        if self.state.scanPosition > len(content):
            self.state.scanPosition = 0
        self.textContent.setPlainText(content)
        if self.state.scanPosition > 0:
            cursor = self.textContent.textCursor()
            cursor.setPosition(self.state.scanPosition)
            self.textContent.setTextCursor(cursor)
            self.textContent.centerCursor()

        self.setWindowTitle(u'Yomisama - {0} ({1})'.format(os.path.basename(filename), self.currentFile.encoding))
        self.setStatus(u'Loaded file {0}'.format(filename))

    def saveFile(self, filename):
        try:
            with io.open(filename,'w',encoding='utf-8') as fp:
                if filename.endswith('.json'):
                    content = self.currentFile.getExportJSON(self.textContent.toPlainText())
                else:
                    content = self.textContent.toPlainText()
                    if len(content)>0 and content[-1] != u'\n':
                        content += u'\n'
                    content+= self.currentFile.getAliasList()
                    content+= self.currentFile.getExportVocabularyList('vocabulary') + u'\n'
                    content+= self.currentFile.getExportVocabularyList('sentence') + u'\n'
                    content+= self.currentFile.getExportVocabularyList('movie') + u'\n'
                    content+= self.currentFile.getExportVocabularyList('kanji')
                fp.write(content)
                fp.close()
        except IOError:
            self.setStatus(u'Failed to save file {0}'.format(filename))
            QtWidgets.QMessageBox.critical(self, 'Yomichan', 'Cannot open file for write')
            return
        self.state.filename = filename
        self.currentFile.filename = filename
        self.updateRecentFile()
        self.updateRecentFiles()
        self.setWindowTitle(u'Yomisama - {0} ({1})'.format(os.path.basename(filename), 'utf-8'))

    def closeFile(self):
        if self.preferences['rememberTextContent']:
            self.preferences['textContent'] = self.textContent.toPlainText()

        self.setWindowTitle('Yomisama')
        self.textContent.setPlainText("")
        self.updateRecentFile(False)
        self.state = self.State()


    def findText(self, text):
        content = self.textContent.toPlainText()
        index = content.find(text, self.state.searchPosition)

        if index == -1:
            wrap = self.state.searchPosition != 0
            self.state.searchPosition = 0
            if wrap:
                self.findText(text)
            else:
                QtWidgets.QMessageBox.information(self, 'Yomisama', 'Search text not found')
        else:
            self.state.searchPosition = index + len(text)
            cursor = self.textContent.textCursor()
            cursor.setPosition(index, QtGui.QTextCursor.MoveAnchor)
            cursor.setPosition(self.state.searchPosition, QtGui.QTextCursor.KeepAnchor)
            self.textContent.setTextCursor(cursor)

        self.state.searchText = text

    def ankiOverwriteFact(self, completeProfile, markup):
        if markup is None:
            self.overwrite = "markup is None"
            return False
        if self.anki is None:
            return False

        profile = self.preferences['profiles'].get(completeProfile)
        if profile is None:
            self.overwrite = "profile is None"
            return False
        fields = reader_util.formatFields(profile['fields'], markup)
        tagsSplit = reader_util.splitTags(self.comboTags.currentText())
        tagsJoined = ' '.join(tagsSplit)
        tagIndex = self.comboTags.findText(tagsJoined)
        if tagIndex > 0:
            self.comboTags.removeItem(tagIndex)
        if tagIndex != 0:
            self.comboTags.insertItem(0, tagsJoined)
        self.preferences.updateFactTags(tagsJoined)
        key = self.anki.getModelKey(profile['model'])                                                  
        value = fields[key]
        ids = self.anki.getNotes(profile['model'],key,value)
        if len(ids) == 0:
            self.overwrite = "len(ids)==0"
            return False
        
        # Overwrite the fields in the note
        # or add a line, if a + is at the end of field name
        note = self.anki.collection().getNote(ids[0])   
        self.overwrite = {
            "note": note,
            "fields": fields
        }
        for name, v in fields.items():
            if name in note:
                if name[-1] == '+':
                    if not v in note[name].split(u'<br>'):
                        if len(note[name])>0:
                            note[name]+= u'<br>' + v
                        else:
                            note[name] = v
                else:
                    note[name] = v 
        note.flush()
        self.currentFile.profiles[completeProfile]['freshlyAdded'].append(value)
        cids = self.anki.getCardsByNote(profile['model'],key,value)
        if len(cids) == 0:
            return False
        
        did = self.anki.collection().decks.id(profile['deck'])
        self.anki.updateCards(cids,did)
        card = self.anki.collection().getCard(cids[0])
        self.currentFile.overwriteVocabulary(completeProfile,value,card)
        self.currentFile.addMarkup(completeProfile,value,markup)
        self.facts.append({'word':value,'profile':completeProfile})
        self.listDefinitions.addItem(value)
        self.listDefinitions.setCurrentRow(self.listDefinitions.count() - 1)
        for profile in self.profiles.values():
            profile.updateDefinitions(scroll=True)
        return True

    def ankiAddFact(self, completeProfile, markup, addToList = True):
        if markup is None:
            self.add = "markup is None"
            return False
        if self.anki is None:
            self.add = "anki is None"
            return False
        profile = self.preferences['profiles'].get(completeProfile)
        if profile is None:
            self.add = "profile is None"
            return False
        fields = reader_util.formatFields(profile['fields'], markup)
        if not self.anki.canAddNote(profile['deck'], profile['model'], fields):
            return self.ankiOverwriteFact(completeProfile, markup)
        self.fields = (fields,profile['fields'],markup)
        tagsSplit = reader_util.splitTags(self.comboTags.currentText())
        tagsJoined = ' '.join(tagsSplit)

        tagIndex = self.comboTags.findText(tagsJoined)
        if tagIndex > 0:
            self.comboTags.removeItem(tagIndex)
        if tagIndex != 0:
            self.comboTags.insertItem(0, tagsJoined)
        self.preferences.updateFactTags(tagsJoined)
        self.addNote = [profile['deck'],profile['model'],fields,tagsSplit]
        self.factId = self.anki.addNote(profile['deck'], profile['model'], fields, tagsSplit)
        if self.factId is None:
            self.add = "factId is None"
            return False
            
        key = self.anki.getModelKey(profile['model'])
        value = fields[key]
        # Put the vocabulary out of 'new' state and add it to the vocabulary list
        self.cardByNote = (profile['model'],key,value)
        ids = self.anki.getCardsByNote(profile['model'],key,value)
        if len(ids) == 0:
            self.add = "len(ids == 0)"
            return False
        card = self.anki.collection().getCard(ids[0])
        self.currentFile.profiles[completeProfile]['freshlyAdded'].append(value)
        self.currentFile.addVocabulary(completeProfile,value,card,addToBadListToo = False)
        self.currentFile.addMarkup(completeProfile,value,markup)
        if value in self.currentFile.profiles[completeProfile]['wordsNotFound']:
            self.currentFile.profiles[completeProfile]['wordsNotFound'].remove(value)
        if self.preferences['unlockVocab']:
            self.anki.collection().sched.earlyAnswerCard(card,2)
        if addToList:
            self.facts.append({'word':value,'profile':completeProfile})
            self.listDefinitions.addItem(value)
            self.listDefinitions.setCurrentRow(self.listDefinitions.count() - 1)
        self.setStatus(u'Added fact {0}; {1} new fact(s) total'.format(value, len(self.facts)))

        for profile in self.profiles.values():
            profile.updateDefinitions(scroll=True)
        return True

    def executeDefCommand(self, command, index):
        commands = command.split("_")
        profile = commands.pop(0)
        self.profiles[profile].runCommand(commands,index)

    def updateSampleMouseEvent(self, event):
        cursor = self.textContent.cursorForPosition(event.pos())
        self.state.scanPosition = cursor.position()
        if event.buttons() & QtCore.Qt.MidButton or event.modifiers() &\
        QtCore.Qt.ShiftModifier or event.buttons() & QtCore.Qt.XButton1:
            self.updateSampleFromPosition()

    def createAlias(self):
        self.updateSampleFromPosition()
        text, ok = QtWidgets.QInputDialog.getText(self, 'Create Alias', 'Replace with:')
        if ok:
            content = self.textContent.toPlainText()
            self.currentFile.alias[text] = content[self.samplePosStart:self.samplePosEnd]
            content = content[:self.samplePosStart] + text + content[self.samplePosEnd:]
            self.samplePosEnd = self.samplePosStart + len(text)
            self.textContent.setPlainText(content)
            cursor = self.textContent.textCursor()
            cursor.setPosition(self.samplePosStart, QtGui.QTextCursor.MoveAnchor)
            cursor.setPosition(self.samplePosEnd, QtGui.QTextCursor.KeepAnchor)
            self.textContent.setTextCursor(cursor)

    def createSubscription(self):
        source, ok = QtWidgets.QInputDialog.getText(self, 'Create Subscription', 'Source: ')
        if ok:
            target, ok = QtWidgets.QInputDialog.getText(self, 'Create Subscription', 'Target: ')
        if ok:
            target = os.path.join(os.path.join(aqt.mw.col.media.dir(),'Yomichan'),target)
            if not os.path.exists(os.path.dirname(target)):
                os.makedirs(os.path.dirname(target))
            self.preferences['subscriptions'].append({'source':source,'target':target})
            self.plugin.loadSubscriptions()

    def getSample(self):
        return self.textContent.toPlainText()[self.samplePosStart:self.samplePosEnd]
            
    def updateSampleFromPosition(self):
        self.samplePosEnd = self.state.scanPosition + self.preferences['scanLength']
        d = dict()
        cursor = self.textContent.textCursor()
        d['content'] = self.textContent.toPlainText()
        d['samplePosStart'] = self.state.scanPosition
        if d['samplePosStart'] >= len(d['content']):
            return
        if self.samplePosEnd > len(d['content']):
            self.samplePosEnd = len(d['content'])
        d['contentSample'] = d['content'][d['samplePosStart']:self.samplePosEnd]
        alias = None
        if self.currentFile is not None:
            for eng,jpn in self.currentFile.alias.items():
                if d['content'][d['samplePosStart']:].startswith(eng):
                    d['contentSample'] = jpn
                    d['contentSampleFlat'] = jpn
                    alias = eng
                    break
        if alias is None:
            d['contentSample'] = d['content'][d['samplePosStart']:self.samplePosEnd]
            d['contentSampleFlat'] = d['contentSample'].replace('\n', '')

        if len(d['content']) == 0:
            return
            
        lengthMatched = 0

        for profile in self.getSortedProfiles():
            lengthMatched = profile.onLookup(d,lengthMatched)

        lengthSelect = 0
        for c in d['contentSample'] or lengthSelect > lengthMatched:
            if lengthMatched <= 0:
                break
            lengthSelect += 1
            if c != u'\n':
                lengthMatched -= 1
        if alias is not None:
            lengthSelect = len(d['contentSample'])
        self.samplePosStart = d['samplePosStart']
        self.samplePosEnd = self.samplePosStart + lengthSelect
        cursor.setPosition(self.samplePosStart, QtGui.QTextCursor.MoveAnchor)
        cursor.setPosition(self.samplePosStart + lengthSelect, QtGui.QTextCursor.KeepAnchor)
        self.textContent.setTextCursor(cursor)

    def clearRecentFiles(self):
        self.preferences.clearRecentFiles()
        self.updateRecentFiles()


    def updateRecentFiles(self):
        self.menuOpenRecent.clear()

        filenames = self.preferences.recentFiles()
        if len(filenames) == 0:
            return

        for filename in filenames:
            self.menuOpenRecent.addAction(filename, lambda f=filename: self.openFile(f))

        self.menuOpenRecent.addSeparator()
        self.menuOpenRecent.addAction('Clear file history', self.clearRecentFiles)


    def updateRecentFile(self, addIfNeeded=True):
        if self.state.filename:
            if addIfNeeded or self.state.filename in self.preferences.recentFiles():
                self.preferences.updateRecentFile(self.state.filename, self.state.scanPosition)

    def updateVocabDefs(self, prfl, **options):
        self.currentFile.profiles[prfl]['longestMatch'] = None
        self.currentFile.profiles[prfl]['longestMatchKey'] = u''
        self.profiles[prfl].updateDefinitions()
        longestMatch = self.currentFile.profiles[prfl]['longestMatch']
        longestMatchKey = self.currentFile.profiles[prfl]['longestMatchKey']
        if self.currentFile is not None:
            # User had to look up the word, put it into the wrong list
            if longestMatchKey in self.currentFile.profiles[prfl]['wordsAll']:
                if longestMatchKey in self.currentFile.profiles[prfl]['freshlyAdded']:
                    self.currentFile.profiles[prfl]['freshlyAdded'].remove(longestMatchKey)
                else:
                    self.recentIncorrect = (prfl,longestMatchKey)
                    self.currentFile.profiles[prfl]['wordsBad'][longestMatchKey] = self.currentFile.profiles[prfl]['wordsAll'][longestMatchKey]
                    self.setStatus(u'{0} has been put into the incorrectly answered set'.format(longestMatchKey))
                    
    def restoreRecentIncorrect(self):
        if self.recentIncorrect:
            prfl, word = self.recentIncorrect
            if word in self.currentFile.profiles[prfl]['wordsBad']:
                del self.currentFile.profiles[prfl]['wordsBad'][word]
                self.setStatus(u'{0} was taken out of the wrongly answered vocabulary list.'.format(word))
                self.recentIncorrect = None
            
    def showNotFoundWords(self):
        QtWidgets.QMessageBox.critical(self, 'Yomichan', u'\n'.join(self.currentFile.profiles['vocabulary']['wordsNotFound']))
        if len(self.currentFile.profiles['vocabulary']['wordsNotFound']) > 0:
            txt = self.currentFile.profiles['vocabulary']['wordsNotFound'][0]
            lbracket = txt.find(u'[')
            if lbracket > 0:
                txt = txt[:lbracket]
            self.findText(txt)

    def importWordList(self, words):
        for profile in self.profiles.values():
            profile.definitions = []
            
        for word in words:
            for key, language in self.languages.items():
                if self.preferences[key]:
                    self.profiles["vocabulary"].definitions += language.dictionary.findTerm(word)

            self.profiles["kanji"].definitions += self.languages['japanese'].findCharacters(word)

        for profile in self.profiles.values():
            profile.updateDefinitions()


    def setStatus(self, status):
        self.statusBar.showMessage(status)
