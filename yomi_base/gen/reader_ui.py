# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/reader.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindowReader(object):
    def setupUi(self, MainWindowReader):
        MainWindowReader.setObjectName("MainWindowReader")
        MainWindowReader.resize(900, 650)
        MainWindowReader.setAcceptDrops(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/img/icon_logo_32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindowReader.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindowReader)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.textContent = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.textContent.setMouseTracking(True)
        self.textContent.setReadOnly(True)
        self.textContent.setObjectName("textContent")
        self.verticalLayout_4.addWidget(self.textContent)
        MainWindowReader.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindowReader)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuOpenRecent = QtWidgets.QMenu(self.menuFile)
        self.menuOpenRecent.setObjectName("menuOpenRecent")
        self.menuImport = QtWidgets.QMenu(self.menuFile)
        self.menuImport.setObjectName("menuImport")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuTextSize = QtWidgets.QMenu(self.menuView)
        self.menuTextSize.setObjectName("menuTextSize")
        MainWindowReader.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindowReader)
        self.toolBar.setIconSize(QtCore.QSize(16, 16))
        self.toolBar.setObjectName("toolBar")
        MainWindowReader.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindowReader)
        self.statusBar.setObjectName("statusBar")
        MainWindowReader.setStatusBar(self.statusBar)
        self.dockAnki = QtWidgets.QDockWidget(MainWindowReader)
        self.dockAnki.setObjectName("dockAnki")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.listDefinitions = QtWidgets.QListWidget(self.dockWidgetContents_2)
        self.listDefinitions.setObjectName("listDefinitions")
        self.verticalLayout_2.addWidget(self.listDefinitions)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.comboTags = QtWidgets.QComboBox(self.dockWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboTags.sizePolicy().hasHeightForWidth())
        self.comboTags.setSizePolicy(sizePolicy)
        self.comboTags.setEditable(True)
        self.comboTags.setObjectName("comboTags")
        self.horizontalLayout_2.addWidget(self.comboTags)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.removeVocabulary = QtWidgets.QPushButton(self.dockWidgetContents_2)
        self.removeVocabulary.setObjectName("removeVocabulary")
        self.verticalLayout_5.addWidget(self.removeVocabulary)
        self.learnVocabulary = QtWidgets.QPushButton(self.dockWidgetContents_2)
        self.learnVocabulary.setObjectName("learnVocabulary")
        self.verticalLayout_5.addWidget(self.learnVocabulary)
        self.createSentenceCards = QtWidgets.QPushButton(self.dockWidgetContents_2)
        self.createSentenceCards.setObjectName("createSentenceCards")
        self.verticalLayout_5.addWidget(self.createSentenceCards)
        self.verticalLayout_2.addLayout(self.verticalLayout_5)
        self.dockAnki.setWidget(self.dockWidgetContents_2)
        MainWindowReader.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockAnki)
        self.actionOpen = QtWidgets.QAction(MainWindowReader)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/img/img/icon_action_open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon1)
        self.actionOpen.setIconVisibleInMenu(True)
        self.actionOpen.setObjectName("actionOpen")
        self.actionQuit = QtWidgets.QAction(MainWindowReader)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/img/img/icon_action_quit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon2)
        self.actionQuit.setIconVisibleInMenu(True)
        self.actionQuit.setObjectName("actionQuit")
        self.actionPreferences = QtWidgets.QAction(MainWindowReader)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/img/img/icon_action_preferences.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPreferences.setIcon(icon3)
        self.actionPreferences.setIconVisibleInMenu(True)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionAbout = QtWidgets.QAction(MainWindowReader)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/img/img/icon_action_about.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon4)
        self.actionAbout.setIconVisibleInMenu(True)
        self.actionAbout.setObjectName("actionAbout")
        self.actionZoomIn = QtWidgets.QAction(MainWindowReader)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/img/img/icon_action_zoom_in.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomIn.setIcon(icon5)
        self.actionZoomIn.setIconVisibleInMenu(True)
        self.actionZoomIn.setObjectName("actionZoomIn")
        self.actionZoomOut = QtWidgets.QAction(MainWindowReader)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/img/img/icon_action_zoom_out.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomOut.setIcon(icon6)
        self.actionZoomOut.setIconVisibleInMenu(True)
        self.actionZoomOut.setObjectName("actionZoomOut")
        self.actionZoomReset = QtWidgets.QAction(MainWindowReader)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/img/img/icon_action_zoom_reset.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomReset.setIcon(icon7)
        self.actionZoomReset.setIconVisibleInMenu(True)
        self.actionZoomReset.setObjectName("actionZoomReset")
        self.actionFind = QtWidgets.QAction(MainWindowReader)
        self.actionFind.setCheckable(False)
        self.actionFind.setChecked(False)
        self.actionFind.setEnabled(True)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/img/img/icon_action_find.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFind.setIcon(icon8)
        self.actionFind.setVisible(True)
        self.actionFind.setIconVisibleInMenu(True)
        self.actionFind.setObjectName("actionFind")
        self.actionFindNext = QtWidgets.QAction(MainWindowReader)
        self.actionFindNext.setObjectName("actionFindNext")
        self.actionToggleWrap = QtWidgets.QAction(MainWindowReader)
        self.actionToggleWrap.setCheckable(True)
        self.actionToggleWrap.setChecked(True)
        self.actionToggleWrap.setObjectName("actionToggleWrap")
        self.actionToggleVocab = QtWidgets.QAction(MainWindowReader)
        self.actionToggleVocab.setCheckable(True)
        self.actionToggleVocab.setObjectName("actionToggleVocab")
        self.actionHomepage = QtWidgets.QAction(MainWindowReader)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/img/img/icon_action_homepage.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHomepage.setIcon(icon9)
        self.actionHomepage.setIconVisibleInMenu(True)
        self.actionHomepage.setObjectName("actionHomepage")
        self.actionToggleAnki = QtWidgets.QAction(MainWindowReader)
        self.actionToggleAnki.setCheckable(True)
        self.actionToggleAnki.setObjectName("actionToggleAnki")
        self.actionFeedback = QtWidgets.QAction(MainWindowReader)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/img/img/icon_action_feedback.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFeedback.setIcon(icon10)
        self.actionFeedback.setObjectName("actionFeedback")
        self.actionToggleKanji = QtWidgets.QAction(MainWindowReader)
        self.actionToggleKanji.setCheckable(True)
        self.actionToggleKanji.setObjectName("actionToggleKanji")
        self.actionKindleDeck = QtWidgets.QAction(MainWindowReader)
        self.actionKindleDeck.setObjectName("actionKindleDeck")
        self.actionWordList = QtWidgets.QAction(MainWindowReader)
        self.actionWordList.setObjectName("actionWordList")
        self.actionSave = QtWidgets.QAction(MainWindowReader)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/img/img/icon_copy_definition.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon11)
        self.actionSave.setIconVisibleInMenu(True)
        self.actionSave.setObjectName("actionSave")
        self.actionToggleKorean = QtWidgets.QAction(MainWindowReader)
        self.actionToggleKorean.setCheckable(True)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/img/img/icon_action_ko.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionToggleKorean.setIcon(icon12)
        self.actionToggleKorean.setObjectName("actionToggleKorean")
        self.actionToggleChinese = QtWidgets.QAction(MainWindowReader)
        self.actionToggleChinese.setCheckable(True)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/img/img/icon_action_ch.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionToggleChinese.setIcon(icon13)
        self.actionToggleChinese.setObjectName("actionToggleChinese")
        self.actionToggleJapanese = QtWidgets.QAction(MainWindowReader)
        self.actionToggleJapanese.setCheckable(True)
        self.actionToggleJapanese.setChecked(False)
        self.actionToggleJapanese.setEnabled(True)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/img/img/icon_action_jp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionToggleJapanese.setIcon(icon14)
        self.actionToggleJapanese.setVisible(True)
        self.actionToggleJapanese.setIconVisibleInMenu(True)
        self.actionToggleJapanese.setObjectName("actionToggleJapanese")
        self.actionToggleGerman = QtWidgets.QAction(MainWindowReader)
        self.actionToggleGerman.setCheckable(True)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/img/img/icon_action_de.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionToggleGerman.setIcon(icon15)
        self.actionToggleGerman.setObjectName("actionToggleGerman")
        self.actionToggleSpanish = QtWidgets.QAction(MainWindowReader)
        self.actionToggleSpanish.setCheckable(True)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/img/img/icon_action_es.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionToggleSpanish.setIcon(icon16)
        self.actionToggleSpanish.setObjectName("actionToggleSpanish")
        self.actionToggleFrench = QtWidgets.QAction(MainWindowReader)
        self.actionToggleFrench.setCheckable(True)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(":/img/img/icon_action_fr.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionToggleFrench.setIcon(icon17)
        self.actionToggleFrench.setObjectName("actionToggleFrench")
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
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionToggleWrap)
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
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionToggleJapanese)
        self.toolBar.addAction(self.actionToggleChinese)
        self.toolBar.addAction(self.actionToggleKorean)
        self.toolBar.addAction(self.actionToggleGerman)
        self.toolBar.addAction(self.actionToggleSpanish)
        self.toolBar.addAction(self.actionToggleFrench)

        self.retranslateUi(MainWindowReader)
        self.actionQuit.triggered.connect(MainWindowReader.close)
        self.actionToggleAnki.toggled['bool'].connect(self.dockAnki.setVisible)
        QtCore.QMetaObject.connectSlotsByName(MainWindowReader)

    def retranslateUi(self, MainWindowReader):
        _translate = QtCore.QCoreApplication.translate
        MainWindowReader.setWindowTitle(_translate("MainWindowReader", "Yomichan"))
        self.textContent.setPlainText(_translate("MainWindowReader", "Paste text here or open a .txt file you want to read!"))
        self.menuFile.setTitle(_translate("MainWindowReader", "&File"))
        self.menuOpenRecent.setTitle(_translate("MainWindowReader", "Open &recent"))
        self.menuImport.setTitle(_translate("MainWindowReader", "&Import"))
        self.menuEdit.setTitle(_translate("MainWindowReader", "&Edit"))
        self.menuHelp.setTitle(_translate("MainWindowReader", "&Help"))
        self.menuView.setTitle(_translate("MainWindowReader", "&View"))
        self.menuTextSize.setTitle(_translate("MainWindowReader", "&Zoom"))
        self.toolBar.setWindowTitle(_translate("MainWindowReader", "toolBar"))
        self.dockAnki.setWindowTitle(_translate("MainWindowReader", "Anki"))
        self.label_3.setText(_translate("MainWindowReader", "Active tag(s)"))
        self.removeVocabulary.setText(_translate("MainWindowReader", "Remove Vocabulary"))
        self.learnVocabulary.setText(_translate("MainWindowReader", "Learn Vocabulary"))
        self.createSentenceCards.setText(_translate("MainWindowReader", "Create sentence cards"))
        self.actionOpen.setText(_translate("MainWindowReader", "&Open..."))
        self.actionOpen.setToolTip(_translate("MainWindowReader", "Open file"))
        self.actionOpen.setShortcut(_translate("MainWindowReader", "Ctrl+O"))
        self.actionQuit.setText(_translate("MainWindowReader", "&Quit"))
        self.actionQuit.setToolTip(_translate("MainWindowReader", "Quit Yomichan"))
        self.actionPreferences.setText(_translate("MainWindowReader", "&Preferences..."))
        self.actionPreferences.setToolTip(_translate("MainWindowReader", "Edit preferences"))
        self.actionAbout.setText(_translate("MainWindowReader", "&About..."))
        self.actionAbout.setToolTip(_translate("MainWindowReader", "About Yomichan"))
        self.actionZoomIn.setText(_translate("MainWindowReader", "Zoom &in"))
        self.actionZoomIn.setShortcut(_translate("MainWindowReader", "Ctrl++"))
        self.actionZoomOut.setText(_translate("MainWindowReader", "Zoom &out"))
        self.actionZoomOut.setShortcut(_translate("MainWindowReader", "Ctrl+-"))
        self.actionZoomReset.setText(_translate("MainWindowReader", "&Reset"))
        self.actionZoomReset.setToolTip(_translate("MainWindowReader", "Reset zoom"))
        self.actionZoomReset.setShortcut(_translate("MainWindowReader", "Ctrl+0"))
        self.actionFind.setText(_translate("MainWindowReader", "&Find..."))
        self.actionFind.setToolTip(_translate("MainWindowReader", "Find text"))
        self.actionFind.setShortcut(_translate("MainWindowReader", "Ctrl+F"))
        self.actionFindNext.setText(_translate("MainWindowReader", "Find &next"))
        self.actionFindNext.setToolTip(_translate("MainWindowReader", "Find text again"))
        self.actionFindNext.setShortcut(_translate("MainWindowReader", "F3"))
        self.actionToggleWrap.setText(_translate("MainWindowReader", "&Word wrap"))
        self.actionToggleWrap.setToolTip(_translate("MainWindowReader", "Toggle word wrap"))
        self.actionToggleVocab.setText(_translate("MainWindowReader", "&Vocabulary"))
        self.actionToggleVocab.setToolTip(_translate("MainWindowReader", "Toggle definitions"))
        self.actionHomepage.setText(_translate("MainWindowReader", "&Homepage..."))
        self.actionHomepage.setToolTip(_translate("MainWindowReader", "Yomichan homepage"))
        self.actionToggleAnki.setText(_translate("MainWindowReader", "&Anki"))
        self.actionFeedback.setText(_translate("MainWindowReader", "&Feedback..."))
        self.actionToggleKanji.setText(_translate("MainWindowReader", "&Kanji"))
        self.actionKindleDeck.setText(_translate("MainWindowReader", "&Kindle deck..."))
        self.actionWordList.setText(_translate("MainWindowReader", "&Word list..."))
        self.actionSave.setText(_translate("MainWindowReader", "&Save..."))
        self.actionSave.setToolTip(_translate("MainWindowReader", "Save file"))
        self.actionSave.setShortcut(_translate("MainWindowReader", "Ctrl+S"))
        self.actionToggleKorean.setText(_translate("MainWindowReader", "&Korean"))
        self.actionToggleKorean.setToolTip(_translate("MainWindowReader", "Enable Korean dictionary"))
        self.actionToggleKorean.setShortcut(_translate("MainWindowReader", "Ctrl+K"))
        self.actionToggleChinese.setText(_translate("MainWindowReader", "&Chinese"))
        self.actionToggleChinese.setToolTip(_translate("MainWindowReader", "Enable Chinese dictionary"))
        self.actionToggleChinese.setShortcut(_translate("MainWindowReader", "Ctrl+H"))
        self.actionToggleJapanese.setText(_translate("MainWindowReader", "&Japanese"))
        self.actionToggleJapanese.setToolTip(_translate("MainWindowReader", "Enable Japanese dictionary"))
        self.actionToggleJapanese.setShortcut(_translate("MainWindowReader", "Ctrl+J"))
        self.actionToggleGerman.setText(_translate("MainWindowReader", "&German"))
        self.actionToggleGerman.setToolTip(_translate("MainWindowReader", "Enable German dictionary"))
        self.actionToggleGerman.setShortcut(_translate("MainWindowReader", "Ctrl+G"))
        self.actionToggleSpanish.setText(_translate("MainWindowReader", "Spanish"))
        self.actionToggleSpanish.setToolTip(_translate("MainWindowReader", "Enable Spanish dictionary"))
        self.actionToggleSpanish.setShortcut(_translate("MainWindowReader", "Ctrl+E"))
        self.actionToggleFrench.setText(_translate("MainWindowReader", "&French"))
        self.actionToggleFrench.setToolTip(_translate("MainWindowReader", "Enable French dictionary"))
from . import resources_rc
