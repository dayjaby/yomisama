# -*- coding: utf-8 -*-

# Copyright (C) 2016 David Jablonski
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

from aqt.webview import AnkiWebView
from PyQt4 import QtGui,QtCore
from profile import *
from anki.utils import isWin
import subprocess
import os
import codecs
import time
import re
import signal
import pysrt
import aqt

import sys
import threading
import Queue
ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(profile,out,queue):
    for line in iter(out.readline,b''):
        profile.lines2.append(line)
        queue.put(line)


markupTimingPattern = re.compile("(\d*?\.\d*?)\-(\d*?\.\d*?)")
timingPattern = re.compile(".*? S: (\d\d):(\d\d):(\d\d)\.(\d\d) E: (\d\d):(\d\d):(\d\d)\.(\d\d)")
# e.g. ANS_time_pos=14.473000
timePosPattern = re.compile("ANS_time_pos=(\d*?\.\d*)")
streamPosPattern = re.compile("ANS_stream_pos")
durationPattern = re.compile(".*?Duration: (\d\d):(\d\d):(\d\d)\.(\d\d)")

if isWin:
    si = subprocess.STARTUPINFO() 
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
else:
    si = None
devnull = file(os.devnull,"w")


class MPlayerKeyFilter(QtCore.QObject):
    profile = None
    
    def eventFilter(self, unused, event):
        mp = self.profile.mplayer
        if event.type() != QtCore.QEvent.KeyPress or mp is None:
            return False
        if QtCore.Qt.Key_Pause == event.key() or QtCore.Qt.Key_Space == event.key():
            self.profile.pause()
        elif event.key() == QtCore.Qt.Key_E:
            mp.stdin.write(self.profile.reader.textContent.toPlainText() + "\n")
        elif event.key() == QtCore.Qt.Key_R:
            self.profile.repeatSubtitle()
        elif event.key() == QtCore.Qt.Key_Left and self.profile.srtIndex>1 and self.profile.srt is not None:
            srt = self.profile.srt[self.profile.srtIndex-2]
            start = srt.start.hours*3600+srt.start.minutes*60+srt.start.seconds+srt.start.milliseconds/1000.00
            mp.stdin.write("seek "+str(start)+" 2\n")
        elif event.key() == QtCore.Qt.Key_Right and self.profile.srt is not None:
            srt = self.profile.srt[self.profile.srtIndex]
            start = srt.start.hours*3600+srt.start.minutes*60+srt.start.seconds+srt.start.milliseconds/1000.00
            mp.stdin.write("seek "+str(start)+" 2\n")
        
            
        return True


class MovieProfile(GenericProfile):
    name = "movie"
    descriptor = "MOVIE SNIPPETS"
    displayedName = "Movie"
    sortIndex = 3
    allowedTags = ['summary','start','end','audio','timing','movie','nosub']

    def __init__(self,reader):
        GenericProfile.__init__(self,reader)
        self.mplayer = None
        self.thread = None
        self.subtitleLogPath = os.path.join(self.reader.anki.collection().media.dir(),"..","..","addons","yomi_base","mplayer","subtitle_log")
        os.environ["MPLAYER_HOME"] = os.path.join(self.reader.anki.collection().media.dir(),"..","..","addons","yomi_base",
"mplayer")
        os.environ["PATH"] += ";" + os.path.join(self.reader.anki.collection().media.dir(),"..","..","addons","tools")

        self.inputConfigPath = "input.conf"
        self.lines = []
        self.lines2 = []
        self.srt = None
        self.srtIndex = None
        self.canPlay = False
        self.keyFilter = MPlayerKeyFilter()
        self.keyFilter.profile = self
        self.reader.installEventFilter(self.keyFilter)
        self.createNoteQueue = Queue.Queue()
        
        self.fixTimings = QtGui.QPushButton(self.reader.dockWidgetContents_2)
        self.fixTimings.setObjectName(fromUtf8("fixTimings"))
        self.fixTimings.clicked.connect(self.onFixTimings)
        self.fixTimings.setText(translate("MainWindowReader", "Fix timings", None))
        self.reader.verticalLayout_5.addWidget(self.fixTimings)
        
        self.timer = QtCore.QTimer(self.reader)
        self.timer.timeout.connect(self._updateSubtitle)
        self.timer.start(500)


        self.paused = False
    
    def onFixTimings(self):
        self.loadSubtitles()
        indices = []
        if self.srt:
            for i in self.srt:
                if i.text.strip() in self.reader.currentFile.profiles["movie"]["wordsMarkup"]:
                    markup = self.reader.currentFile.profiles["movie"]["wordsMarkup"][i.text.strip()]
                    newTiming = str(i.start.ordinal/1000.0) + "-" + str(i.end.ordinal/1000.0)
                    if "timing" not in markup:
                        indices.append(i.index-1)
                    elif newTiming != markup["timing"]:
                        dirname = self.reader.currentFile.name
                        out = os.path.join(dirname,markup["timing"]+".mp3")
                        if os.path.isfile(out):
                            os.remove(out)
                        indices.append(i.index-1)
        for index in indices:
            self.createNote(index=index,showNoteAdded=False)
             
            
    def close(self):
        self.mplayer = None
        if self.thread:
            self.thread.stopEvent.set()
            
    def openMovie(self):
        if self.canPlay:
            if self.mplayer:
                self.mplayer.stdin.write("quit\n")
            self.mplayer = subprocess.Popen(
                [
                    "mplayer",
                    "-slave",
                    "-msglevel","all=-1:global=5",
                    "-subcp","utf8",
                    "-utf8",
                    "-vo","directx:noaccel",
                    self.reader.currentFile.name+self.videoFormat],
                startupinfo=si, 
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=devnull,
                bufsize=1)
            self.queue = Queue.Queue()
            self.thread = threading.Thread(target=enqueue_output,args=(self,self.mplayer.stdout,self.queue))
            self.thread.daemon = True
            self.thread.stopEvent = threading.Event()
            self.thread.start()

            self.consumer = threading.Thread(target=self._updateSubtitle)
            self.consumer.daemon = True
            self.consumer.stopEvent = threading.Event()
            self.consumer.start()

            
    def onLookup(self,d,lengthMatched):
        return lengthMatched
        
        
    def runCommand(self,cmd,definition):
        pass
    
    def markup(self, definition):
        return definition

    def updateDefinitions(self,**options):
        pass
        
    def _updateSubtitle(self):
        if self.mplayer is not None:
            try:
                line = self.queue.get_nowait()
            except Queue.Empty:
                pass
            else:
                if line != '':
                    self.lines.append(line)
                    match1 = timePosPattern.match(line)
                    if match1:
                        self.createNote(timestamp=float(match1.group(1)))
                    match2 = streamPosPattern.match(line)
                    if match2:
                        self.repeatSubtitle()
                    
        
    def afterFileLoaded(self):
        if ".mkv" in self.reader.currentFile.loadedExtensions:
            self.videoFormat = ".mkv"
        elif ".mp4" in self.reader.currentFile.loadedExtensions:
            self.videoFormat = ".mp4"
        else:
            self.videoFormat = None
            
        if self.videoFormat is not None:
            self.canPlay = True
            self.openMovie()
            self.loadSubtitles()
        else:
            self.canPlay = False
            self.mplayer = None

    def loadSubtitles(self):
        if ".srt" in self.reader.currentFile.loadedExtensions:
            self.srt = pysrt.open(self.reader.currentFile.name+".srt")
            for x in self.srt:
                x.text = " ".join(x.text.split("\n"))
            self.srt.save(self.reader.currentFile.name+".srt",encoding="utf-8")
            entireText = "\n".join([i.text for i in self.srt])
            #if self.reader.textContent.toPlainText() == "":
            self.reader.textContent.setPlainText(entireText)
                
    def pause(self,value=None):
        if self.mplayer:
            if value is None:
                value = not self.paused
            if value != self.paused:
                self.mplayer.stdin.write("pause\n")
            self.paused = value
        
    def createNote(self,timestamp=None,index=None,showNoteAdded=True):
        nosub = False
        if self.srt is None:
            nosub = True
        else:
            if timestamp is not None:
              subs = self.srt.at(seconds=timestamp)
              if len(subs)>0:
                self.start = subs[0].start.ordinal/1000.0
                self.end = subs[0].end.ordinal/1000.0
                self.subtitle = subs[0].text.strip()
              else:
                nosub = True
            elif index is not None:
                self.start = self.srt[index].start.ordinal/1000.0
                self.end = self.srt[index].end.ordinal/1000.0
                self.subtitle = self.srt[index].text.strip()
        if nosub:
            self.start = timestamp - 10 if timestamp>10 else 0
            self.end = timestamp
            self.subtitle = "NOSUB:"+str(time.time())

        dirname = self.reader.currentFile.name
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        log = open("debug.txt","w+")
        if index is None:
            self.mplayer.stdin.write("pause")
        outMp3 = os.path.join(dirname,str(self.start)+"-"+str(self.end))+".mp3"
        outMp4 = os.path.join(dirname,str(self.start)+"-"+str(self.end))+".mp4"

        ffmpeg = subprocess.call(
            ["ffmpeg",
            "-vn","-y",
            "-i",self.reader.currentFile.name+self.videoFormat,
            "-ac","2",
            "-map","0:1",
            "-ss",str(self.start),
            "-t",str(self.end-self.start),
            "-threads","0",
            "-acodec","libmp3lame",
            outMp3],
            startupinfo=si,stdout=log,stderr=log)

        ffmpeg = subprocess.call(
            ["ffmpeg",
            "-vn","-y",
            "-i",self.reader.currentFile.name+self.videoFormat,
            "-ss",str(self.start),
            "-t",str(self.end-self.start),
            "-threads","0",
            "-acodec","libvo_aacenc",
            "-vcodec","mpeg4",
            outMp4],
            startupinfo=si,stdout=log,stderr=log)

            
        self.definition = {
            'summary': self.subtitle,
            'start': str(self.start),
            'end': str(self.end),
            'timing': str(self.start) + "-" + str(self.end),
            'movie': "[sound:{0}]".format(os.path.relpath(outMp4,self.reader.anki.collection().media.dir()).replace("\\","/")),
            'audio': "[sound:{0}]".format(os.path.relpath(outMp3,self.reader.anki.collection().media.dir()).replace("\\","/")),
            'nosub': "Yes" if nosub else ""
        }
        self.canAddNote = self.ankiIsFactValid("movie",self.definition)
        if self.canAddNote:
            self.fact = "add"
            self.addFact(self.definition)
        else:
            self.fact = "overwrite"
            self.overwrite = self.definition
            self.overwriteFact(self.definition)
        if showNoteAdded:
            self.mplayer.stdin.write("pausing_keep_force osd_show_text 'Note added' 500")
    
    def repeatSubtitle(self):
        self.mplayer.stdin.write("seek "+str(self.start-1)+" 2\n")
