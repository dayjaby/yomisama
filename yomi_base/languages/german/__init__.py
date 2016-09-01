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

import dictionary
import os.path
import translate


def initLanguage(preferences,load=True):
    directory = os.path.dirname(__file__)
    dic = dictionary.Dictionary(os.path.join(directory, 'de-eng.txt'), load=load)
    if load:
        return translate.Translator(None,dic)
        
