# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reader.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindowReader(object):
    def setupUi(self, MainWindowReader):
        MainWindowReader.setObjectName(_fromUtf8("MainWindowReader"))
        MainWindowReader.resize(900, 650)
        MainWindowReader.setAcceptDrops(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/img/img/icon_logo_32.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindowReader.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindowReader)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.textContent = QtGui.QPlainTextEdit(self.centralwidget)
        self.textContent.setMouseTracking(True)
        self.textContent.setReadOnly(True)
        self.textContent.setObjectName(_fromUtf8("textContent"))
        self.verticalLayout_4.addWidget(self.textContent)
        MainWindowReader.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindowReader)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuOpenRecent = QtGui.QMenu(self.menuFile)
        self.menuOpenRecent.setObjectName(_fromUtf8("menuOpenRecent"))
        self.menuImport = QtGui.QMenu(self.menuFile)
        self.menuImport.setObjectName(_fromUtf8("menuImport"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        self.menuTextSize = QtGui.QMenu(self.menuView)
        self.menuTextSize.setObjectName(_fromUtf8("menuTextSize"))
        MainWindowReader.setMenuBar(self.menubar)
        self.toolBar = QtGui.QToolBar(MainWindowReader)
        self.toolBar.setIconSize(QtCore.QSize(16, 16))
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindowReader.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.dockVocab = QtGui.QDockWidget(MainWindowReader)
        self.dockVocab.setObjectName(_fromUtf8("dockVocab"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.textVocabDefs = QtGui.QTextBrowser(self.dockWidgetContents)
        self.textVocabDefs.setAcceptDrops(False)
        self.textVocabDefs.setOpenLinks(False)
        self.textVocabDefs.setObjectName(_fromUtf8("textVocabDefs"))
        self.verticalLayout.addWidget(self.textVocabDefs)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(self.dockWidgetContents)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.textVocabSearch = QtGui.QLineEdit(self.dockWidgetContents)
        self.textVocabSearch.setObjectName(_fromUtf8("textVocabSearch"))
        self.horizontalLayout_3.addWidget(self.textVocabSearch)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.dockVocab.setWidget(self.dockWidgetContents)
        MainWindowReader.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockVocab)
        self.statusBar = QtGui.QStatusBar(MainWindowReader)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindowReader.setStatusBar(self.statusBar)
        self.dockAnki = QtGui.QDockWidget(MainWindowReader)
        self.dockAnki.setObjectName(_fromUtf8("dockAnki"))
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName(_fromUtf8("dockWidgetContents_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.listDefinitions = QtGui.QListWidget(self.dockWidgetContents_2)
        self.listDefinitions.setObjectName(_fromUtf8("listDefinitions"))
        self.verticalLayout_2.addWidget(self.listDefinitions)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(self.dockWidgetContents_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.comboTags = QtGui.QComboBox(self.dockWidgetContents_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboTags.sizePolicy().hasHeightForWidth())
        self.comboTags.setSizePolicy(sizePolicy)
        self.comboTags.setEditable(True)
        self.comboTags.setObjectName(_fromUtf8("comboTags"))
        self.horizontalLayout_2.addWidget(self.comboTags)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.removeVocabulary = QtGui.QPushButton(self.dockWidgetContents_2)
        self.removeVocabulary.setObjectName(_fromUtf8("removeVocabulary"))
        self.verticalLayout_5.addWidget(self.removeVocabulary)
        self.learnVocabulary = QtGui.QPushButton(self.dockWidgetContents_2)
        self.learnVocabulary.setObjectName(_fromUtf8("learnVocabulary"))
        self.verticalLayout_5.addWidget(self.learnVocabulary)
        self.moveVocabulary = QtGui.QPushButton(self.dockWidgetContents_2)
        self.moveVocabulary.setObjectName(_fromUtf8("moveVocabulary"))
        self.verticalLayout_5.addWidget(self.moveVocabulary)
        self.verticalLayout_2.addLayout(self.verticalLayout_5)
        self.dockAnki.setWidget(self.dockWidgetContents_2)
        MainWindowReader.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockAnki)
        self.dockKanji = QtGui.QDockWidget(MainWindowReader)
        self.dockKanji.setObjectName(_fromUtf8("dockKanji"))
        self.dockWidgetContents_3 = QtGui.QWidget()
        self.dockWidgetContents_3.setObjectName(_fromUtf8("dockWidgetContents_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.dockWidgetContents_3)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.textKanjiDefs = QtGui.QTextBrowser(self.dockWidgetContents_3)
        self.textKanjiDefs.setAcceptDrops(False)
        self.textKanjiDefs.setOpenLinks(False)
        self.textKanjiDefs.setObjectName(_fromUtf8("textKanjiDefs"))
        self.verticalLayout_3.addWidget(self.textKanjiDefs)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_2 = QtGui.QLabel(self.dockWidgetContents_3)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_4.addWidget(self.label_2)
        self.textKanjiSearch = QtGui.QLineEdit(self.dockWidgetContents_3)
        self.textKanjiSearch.setObjectName(_fromUtf8("textKanjiSearch"))
        self.horizontalLayout_4.addWidget(self.textKanjiSearch)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.dockKanji.setWidget(self.dockWidgetContents_3)
        MainWindowReader.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockKanji)
        self.actionOpen = QtGui.QAction(MainWindowReader)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/img/img/icon_action_open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon1)
        self.actionOpen.setIconVisibleInMenu(True)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionQuit = QtGui.QAction(MainWindowReader)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/img/img/icon_action_quit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon2)
        self.actionQuit.setIconVisibleInMenu(True)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionPreferences = QtGui.QAction(MainWindowReader)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/img/img/icon_action_preferences.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPreferences.setIcon(icon3)
        self.actionPreferences.setIconVisibleInMenu(True)
        self.actionPreferences.setObjectName(_fromUtf8("actionPreferences"))
        self.actionAbout = QtGui.QAction(MainWindowReader)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/img/img/icon_action_about.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon4)
        self.actionAbout.setIconVisibleInMenu(True)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionZoomIn = QtGui.QAction(MainWindowReader)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/img/img/icon_action_zoom_in.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomIn.setIcon(icon5)
        self.actionZoomIn.setIconVisibleInMenu(True)
        self.actionZoomIn.setObjectName(_fromUtf8("actionZoomIn"))
        self.actionZoomOut = QtGui.QAction(MainWindowReader)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/img/img/icon_action_zoom_out.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomOut.setIcon(icon6)
        self.actionZoomOut.setIconVisibleInMenu(True)
        self.actionZoomOut.setObjectName(_fromUtf8("actionZoomOut"))
        self.actionZoomReset = QtGui.QAction(MainWindowReader)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/img/img/icon_action_zoom_reset.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomReset.setIcon(icon7)
        self.actionZoomReset.setIconVisibleInMenu(True)
        self.actionZoomReset.setObjectName(_fromUtf8("actionZoomReset"))
        self.actionFind = QtGui.QAction(MainWindowReader)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/img/img/icon_action_find.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFind.setIcon(icon8)
        self.actionFind.setIconVisibleInMenu(True)
        self.actionFind.setObjectName(_fromUtf8("actionFind"))
        self.actionFindNext = QtGui.QAction(MainWindowReader)
        self.actionFindNext.setObjectName(_fromUtf8("actionFindNext"))
        self.actionToggleWrap = QtGui.QAction(MainWindowReader)
        self.actionToggleWrap.setCheckable(True)
        self.actionToggleWrap.setChecked(True)
        self.actionToggleWrap.setObjectName(_fromUtf8("actionToggleWrap"))
        self.actionToggleVocab = QtGui.QAction(MainWindowReader)
        self.actionToggleVocab.setCheckable(True)
        self.actionToggleVocab.setObjectName(_fromUtf8("actionToggleVocab"))
        self.actionHomepage = QtGui.QAction(MainWindowReader)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8(":/img/img/icon_action_homepage.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHomepage.setIcon(icon9)
        self.actionHomepage.setIconVisibleInMenu(True)
        self.actionHomepage.setObjectName(_fromUtf8("actionHomepage"))
        self.actionToggleAnki = QtGui.QAction(MainWindowReader)
        self.actionToggleAnki.setCheckable(True)
        self.actionToggleAnki.setObjectName(_fromUtf8("actionToggleAnki"))
        self.actionFeedback = QtGui.QAction(MainWindowReader)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(_fromUtf8(":/img/img/icon_action_feedback.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFeedback.setIcon(icon10)
        self.actionFeedback.setObjectName(_fromUtf8("actionFeedback"))
        self.actionToggleKanji = QtGui.QAction(MainWindowReader)
        self.actionToggleKanji.setCheckable(True)
        self.actionToggleKanji.setObjectName(_fromUtf8("actionToggleKanji"))
        self.actionKindleDeck = QtGui.QAction(MainWindowReader)
        self.actionKindleDeck.setObjectName(_fromUtf8("actionKindleDeck"))
        self.actionWordList = QtGui.QAction(MainWindowReader)
        self.actionWordList.setObjectName(_fromUtf8("actionWordList"))
        self.actionSave = QtGui.QAction(MainWindowReader)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(_fromUtf8(":/img/img/icon_copy_definition.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon11)
        self.actionSave.setIconVisibleInMenu(True)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionToggleJapanese = QtGui.QAction(MainWindowReader)
        self.actionToggleJapanese.setCheckable(True)
        self.actionToggleJapanese.setObjectName(_fromUtf8("actionToggleJapanese"))
        self.actionToggleKorean = QtGui.QAction(MainWindowReader)
        self.actionToggleKorean.setCheckable(True)
        self.actionToggleKorean.setObjectName(_fromUtf8("actionToggleKorean"))
        self.actionToggleChinese = QtGui.QAction(MainWindowReader)
        self.actionToggleChinese.setCheckable(True)
        self.actionToggleChinese.setObjectName(_fromUtf8("actionToggleChinese"))
        self.menuImport.addAction(self.actionKindleDeck)
        self.menuImport.addAction(self.actionWordList)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.menuOpenRecent.menuAction())
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuImport.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionFind)
        self.menuEdit.addAction(self.actionFindNext)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionPreferences)
        self.menuHelp.addAction(self.actionHomepage)
        self.menuHelp.addAction(self.actionFeedback)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menuTextSize.addAction(self.actionZoomIn)
        self.menuTextSize.addAction(self.actionZoomOut)
        self.menuTextSize.addSeparator()
        self.menuTextSize.addAction(self.actionZoomReset)
        self.menuView.addAction(self.menuTextSize.menuAction())
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionToggleAnki)
        self.menuView.addAction(self.actionToggleVocab)
        self.menuView.addAction(self.actionToggleKanji)
        self.menuView.addAction(self.actionToggleWrap)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionToggleJapanese)
        self.menuView.addAction(self.actionToggleKorean)
        self.menuView.addAction(self.actionToggleChinese)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionZoomIn)
        self.toolBar.addAction(self.actionZoomOut)
        self.toolBar.addAction(self.actionZoomReset)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionFind)

        self.retranslateUi(MainWindowReader)
        QtCore.QObject.connect(self.actionToggleVocab, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.dockVocab.setVisible)
        QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindowReader.close)
        QtCore.QObject.connect(self.actionToggleAnki, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.dockAnki.setVisible)
        QtCore.QObject.connect(self.actionToggleKanji, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.dockKanji.setVisible)
        QtCore.QMetaObject.connectSlotsByName(MainWindowReader)

    def retranslateUi(self, MainWindowReader):
        MainWindowReader.setWindowTitle(_translate("MainWindowReader", "Yomichan", None))
        self.textContent.setPlainText(_translate("MainWindowReader", "Paste text here or open a .txt file you want to read!", None))
        self.menuFile.setTitle(_translate("MainWindowReader", "&File", None))
        self.menuOpenRecent.setTitle(_translate("MainWindowReader", "Open &recent", None))
        self.menuImport.setTitle(_translate("MainWindowReader", "&Import", None))
        self.menuEdit.setTitle(_translate("MainWindowReader", "&Edit", None))
        self.menuHelp.setTitle(_translate("MainWindowReader", "&Help", None))
        self.menuView.setTitle(_translate("MainWindowReader", "&View", None))
        self.menuTextSize.setTitle(_translate("MainWindowReader", "&Zoom", None))
        self.toolBar.setWindowTitle(_translate("MainWindowReader", "toolBar", None))
        self.dockVocab.setWindowTitle(_translate("MainWindowReader", "Vocabulary", None))
        self.label.setText(_translate("MainWindowReader", "Expression", None))
        self.dockAnki.setWindowTitle(_translate("MainWindowReader", "Anki", None))
        self.label_3.setText(_translate("MainWindowReader", "Active tag(s)", None))
        self.removeVocabulary.setText(_translate("MainWindowReader", "Remove Vocabulary", None))
        self.learnVocabulary.setText(_translate("MainWindowReader", "Learn Vocabulary", None))
        self.moveVocabulary.setText(_translate("MainWindowReader", "Move Vocabulary", None))
        self.dockKanji.setWindowTitle(_translate("MainWindowReader", "Kanji", None))
        self.label_2.setText(_translate("MainWindowReader", "Character", None))
        self.actionOpen.setText(_translate("MainWindowReader", "&Open...", None))
        self.actionOpen.setToolTip(_translate("MainWindowReader", "Open file", None))
        self.actionOpen.setShortcut(_translate("MainWindowReader", "Ctrl+O", None))
        self.actionQuit.setText(_translate("MainWindowReader", "&Quit", None))
        self.actionQuit.setToolTip(_translate("MainWindowReader", "Quit Yomichan", None))
        self.actionPreferences.setText(_translate("MainWindowReader", "&Preferences...", None))
        self.actionPreferences.setToolTip(_translate("MainWindowReader", "Edit preferences", None))
        self.actionAbout.setText(_translate("MainWindowReader", "&About...", None))
        self.actionAbout.setToolTip(_translate("MainWindowReader", "About Yomichan", None))
        self.actionZoomIn.setText(_translate("MainWindowReader", "Zoom &in", None))
        self.actionZoomIn.setShortcut(_translate("MainWindowReader", "Ctrl++", None))
        self.actionZoomOut.setText(_translate("MainWindowReader", "Zoom &out", None))
        self.actionZoomOut.setShortcut(_translate("MainWindowReader", "Ctrl+-", None))
        self.actionZoomReset.setText(_translate("MainWindowReader", "&Reset", None))
        self.actionZoomReset.setToolTip(_translate("MainWindowReader", "Reset zoom", None))
        self.actionZoomReset.setShortcut(_translate("MainWindowReader", "Ctrl+0", None))
        self.actionFind.setText(_translate("MainWindowReader", "&Find...", None))
        self.actionFind.setToolTip(_translate("MainWindowReader", "Find text", None))
        self.actionFind.setShortcut(_translate("MainWindowReader", "Ctrl+F", None))
        self.actionFindNext.setText(_translate("MainWindowReader", "Find &next", None))
        self.actionFindNext.setToolTip(_translate("MainWindowReader", "Find text again", None))
        self.actionFindNext.setShortcut(_translate("MainWindowReader", "F3", None))
        self.actionToggleWrap.setText(_translate("MainWindowReader", "&Word wrap", None))
        self.actionToggleWrap.setToolTip(_translate("MainWindowReader", "Toggle word wrap", None))
        self.actionToggleVocab.setText(_translate("MainWindowReader", "&Vocabulary", None))
        self.actionToggleVocab.setToolTip(_translate("MainWindowReader", "Toggle definitions", None))
        self.actionHomepage.setText(_translate("MainWindowReader", "&Homepage...", None))
        self.actionHomepage.setToolTip(_translate("MainWindowReader", "Yomichan homepage", None))
        self.actionToggleAnki.setText(_translate("MainWindowReader", "&Anki", None))
        self.actionFeedback.setText(_translate("MainWindowReader", "&Feedback...", None))
        self.actionToggleKanji.setText(_translate("MainWindowReader", "&Kanji", None))
        self.actionKindleDeck.setText(_translate("MainWindowReader", "&Kindle deck...", None))
        self.actionWordList.setText(_translate("MainWindowReader", "&Word list...", None))
        self.actionSave.setText(_translate("MainWindowReader", "&Save...", None))
        self.actionSave.setToolTip(_translate("MainWindowReader", "Save file", None))
        self.actionSave.setShortcut(_translate("MainWindowReader", "Ctrl+S", None))
        self.actionToggleJapanese.setText(_translate("MainWindowReader", "&Japanese", None))
        self.actionToggleJapanese.setToolTip(_translate("MainWindowReader", "Enable Japanese dictionary", None))
        self.actionToggleKorean.setText(_translate("MainWindowReader", "&Korean", None))
        self.actionToggleKorean.setToolTip(_translate("MainWindowReader", "Enable Korean dictionary", None))
        self.actionToggleChinese.setText(_translate("MainWindowReader", "&Chinese", None))
        self.actionToggleChinese.setToolTip(_translate("MainWindowReader", "Enable Chinese dictionary", None))

import resources_rc
