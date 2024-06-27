# -*- coding: utf-8 -*-

from anki.scheduler.v3 import Scheduler as SchedulerV2
import math
import datetime
import random
import time
import anki
from anki.rsbackend import DeckTreeNode
from anki.consts import CARD_TYPE_NEW, QUEUE_TYPE_NEW


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
        
    # def answerCard(self,card,ease):
    #     if ease == 1:
    #         for m, value in card.note().items():
    #             if m[:9] == u"ConnectTo":
    #                 model = self.col.models.byName(m[9:])
    #                 if model is None:
    #                     continue
    #                 key = model[u"flds"][0][u"name"]
    #                 cards = self.col.findCards(key + u':"' + value + u'" note:' + m[9:])
    #                 for connectedCardId in cards:
    #                     connectedCard = self.col.getCard(connectedCardId)
    #                     connectedCard.startTimer()
    #                     SchedulerV2.answerCard(self, connectedCard, ease)
    #     SchedulerV2.answerCard(self, card, ease)

    def earlyAnswerCard(self, card, ease, timeUsed=None):
        if card.queue < 0:
            card.queue = 0
        if timeUsed is None:
            card.start_timer()
        else:
            card.timer_started = time.time() - timeUsed

        if ease == 1:
            self.set_due_date([card.id], "0!")
        else:
            if card.type == CARD_TYPE_NEW or card.queue == QUEUE_TYPE_NEW:
                self.set_due_date([card.id], "1!")
            else:
                ivl = 1 + card.ivl * 2
                self.set_due_date([card.id], str(ivl) + "!")


    def _smoothedIvl(self, card):
        if card.ivl > 0 and card.queue == 2:
            return max(self.minimumGain,float(card.ivl - self._daysEarly(card)) / card.ivl)
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
            id = self.col.decks.id(deck, create=False)
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
                # print(deck, path, parent_path)
                # try to find parent in the already existing tree
                node = data
                found = False
                for child_name in path:
                    found = False
                    for child in node.children:
                        if child_name == child.name:
                            node = child
                            found = True
                            break
                    if not found:
                        print("Could not find child: {} in {}".format(child_name, deck))
                        break

                if not found:
                    continue
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

                self.dueCache[deck] = due
        return data
