# -*- coding: utf-8 -*-

from anki.scheduler.v2 import Scheduler as SchedulerV2
import math
import datetime
import random
import time
import anki
from anki.rsbackend import DeckTreeNode


class Scheduler(SchedulerV2):
    def __init__(self, col: anki.collection.Collection, filecache, 
            scheduleVariationPercent=0.0, 
            minimumGain=0.05,
            hideMinimumGain=False,
            weekDays = [True,True,True,True,True,True,True]
        ):
        SchedulerV2.__init__(self, col)
        self.filecache = filecache
        self.scheduleVariationPercent = int(scheduleVariationPercent)
        # Any occuring vocabulary's ivl will increase by at least 5%
        self.minimumGain = minimumGain
        self.hideMinimumGain = hideMinimumGain
        self.weekDays = weekDays
        self.dueCache = dict()
        self.reset()
        
    def answerCard(self,card,ease):
        if ease == 1:
            for m, value in card.note().items():
                if m[:9] == u"ConnectTo":
                    model = self.col.models.byName(m[9:])
                    if model is None:
                        continue
                    key = model[u"flds"][0][u"name"]
                    cards = self.col.findCards(key + u':"' + value + u'" note:' + m[9:])
                    for connectedCardId in cards:
                        connectedCard = self.col.getCard(connectedCardId)
                        connectedCard.startTimer()
                        anki.sched.Scheduler.answerCard(self,connectedCard,ease)
        anki.sched.Scheduler.answerCard(self,card,ease)
        
    def earlyAnswerCard(self,card,ease,timeUsed=None):
        if card.queue < 0:
            card.queue = 0
        if timeUsed is None:
            card.start_timer()
        else:
            card.timerStarted = time.time() - timeUsed
        self.answerCard(card,ease)
    
    def _updateRevIvl(self, card, ease):
        idealIvl = self._nextRevIvl(card, ease)
        adjIv1 = self._adjRevIvl(card, idealIvl)
        if card.queue == 2:
            card.ivl = card.ivl + math.ceil(self._smoothedIvl(card)*(adjIv1 - card.ivl))
        else:
            card.ivl = adjIvl
        card.ivl = random.randint(int(card.ivl * (1-self.scheduleVariationPercent/100.0)),int(card.ivl * (1+self.scheduleVariationPercent/100)))
        counter = 0
        while counter < 4 and not self.weekDays[(datetime.date.today() + datetime.timedelta(card.ivl)).weekday()] and card.ivl > 1:
            card.ivl += random.randint(0,1) * 2 - 1
            counter = counter + 1
            
    def _smoothedIvl(self,card):
        if card.ivl > 0 and card.queue == 2:
            return max(self.minimumGain,float(card.ivl - self._daysEarly(card))/card.ivl)
        else:
            return 1
        
    def _daysEarly(self, card):
        "Number of days earlier than scheduled."
        due = card.odue if card.odid else card.due
        return max(0, due - self.today)
        
    def deck_due_tree(self, top_deck_id: int = 0):
        data = SchedulerV2.deck_due_tree(self, top_deck_id)
        filecache = self.filecache()
        deck_parents = dict()
        for child in data.children:
            if child.name == "Yomichan" or child.name == "Yomisama":
                deck_parents[child.name] = child
        for deck in filecache:
            id = self.col.decks.id(deck,create=False)
            if id is not None:
                if filecache[deck] is None:
                    due = 0
                    new = 0
                else:
                    if self.hideMinimumGain:
                        due = int(filecache[deck].dueness - filecache[deck].foundvocabs * self.minimumGain)
                    else:
                        due = int(filecache[deck].dueness)
                    new = filecache[deck].count('wordsNotFound')
                path = deck.split("::")
                parent_path = "::".join(path[:-1])
                # try to find parent in the already existing tree
                node = data
                for child_name in path:
                    found = False
                    for child in node.children:
                        if child_name == child.name:
                            node = child
                            found = True
                            break
                    if not found:
                        raise Exception("Could not find child: {} in {}".format(child_name, deck))
                parent = node

                node.review_count = due
                node.learn_count = 0
                node.new_count = new

                if parent_path in deck_parents:
                    parent = deck_parents[parent_path]
                else:
                    raise Exception("Invalid tree path: {}".format(deck))
                deck_parents[deck] = node

                for i in range(1, len(path)):
                    index = "::".join(path[:-i])
                    if index in deck_parents:
                        deck_parents[index].review_count += due
                        deck_parents[index].new_count += new
                    elif index == "Yomisama" or index == "Yomichan":
                        data.review_count += due
                        data.new_count += new

                """node = DeckTreeNode(name=path[-1], deck_id=id, review_count=due, learn_count=0, new_count=new)
                parent.children.append(node)
                deck_parents[deck] = node"""
                print(deck, due)
                self.dueCache[deck] = due
        return data
