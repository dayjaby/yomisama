#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
   jcconv, Japanese Characters CONVerter, interconvert hiragana, katakana, half-width kana.
   This module also treat 'half/wide number', 'half/wide alphabet'.
   
   IMPOTANT: In current version, this works only with utf-8 encoding.


   Simple example of usage is followings

       >>> from jcconv import *
       >>> print hira2kata('あいうえお')   # hiragana to katakana
       アイウエオ
       >>> print kata2hira('カタカナ')     # katakana to hiragana
       かたかな
       >>> print half2hira('ﾊﾝｶｸｶﾀｶﾅ')      # half-width kana to hiragana
       はんかくかたかな       
       >>> print half2wide('hello jcconv') # half-width alphabet to wide-width
       ｈｅｌｌｏ ｊｃｃｏｎｖ
       >>> print wide2half('ＷＩＤＥ')     # wide-width alphabet to half-width
       wide
"""

__author__  = "Matsumoto Taichi (taichino@gmail.com)"
__version__ = "0.1.2"
__license__ = "MIT License"

import re

# convert hiragana to katakana
def hira2kata(text):
  return convert(text, jcconv.HIRA, jcconv.KATA)

# convert katakana to hiragana
def kata2hira(text):
  return convert(text, jcconv.KATA, jcconv.HIRA)

# convert half-width kana to hiragana
def half2hira(text):
  return convert(text, jcconv.HALF, jcconv.HIRA)

# convert hiragana to half-width kana
def hira2half(text):
  return convert(text, jcconv.HIRA, jcconv.HALF)

# convert katakana to half-with kana
def kata2half(text):
  return convert(text, jcconv.KATA, jcconv.HALF)

# convert half-width kana to katakana
def half2kata(text):
  return convert(text, jcconv.HALF, jcconv.KATA)

# expand half width number and alphabet to wide width
def half2wide(text):
  text = convert(text, jcconv.HNUM, jcconv.WNUM)
  return convert(text, jcconv.HALP, jcconv.WALP)

# shrink wide with number and alphabet to half width
def wide2half(text):
  text = convert(text, jcconv.WNUM, jcconv.HNUM)
  return convert(text, jcconv.WALP, jcconv.HALP)

# convert 'frm' charset to 'to' charset
# input text must be unicode or str(utf-8)
# 'frm' and 'to' can be specified with (HIRA, KATA, HALF, WNUM, HNUM, WALP, HALP)
def convert(text, frm, to):
  uflag = isinstance(text, unicode)
  f_set = jcconv.char_sets[frm]
  t_set = jcconv.char_sets[to]

  text = uflag and text or text.decode('utf-8')
  if len(f_set[0].split(' ')) == len(t_set[0].split(' ')):
    for i in range(len(f_set)):
      conv_table = dict(zip(f_set[i].split(' '), t_set[i].split(' ')))
      text = _multiple_replace(text, conv_table)
    return uflag and text or text.encode('utf-8')
  else:
    raise "Invalid Parameter"

def _multiple_replace(text, dic):
  rx = re.compile('|'.join(dic))
  def proc_one(match):
    return dic[match.group(0)]
  return rx.sub(proc_one, text)


# define character sets used in japanese
class jcconv:
  (HIRA, KATA, HALF, WNUM, HNUM, WALP, HALP) = (i for i in range(7))
  hira = [u'が ぎ ぐ げ ご ざ じ ず ぜ ぞ だ ぢ づ で ど ば び ぶ べ ぼ ぱ ぴ ぷ ぺ ぽ',
          u'あ い う え お か き く け こ さ し す せ そ た ち つ て と ' + \
          u'な に ぬ ね の は ひ ふ へ ほ ま み む め も や ゆ よ ら り る れ ろ ' + \
          u'わ を ん ぁ ぃ ぅ ぇ ぉ ゃ ゅ ょ っ']
  kata = [u'ガ ギ グ ゲ ゴ ザ ジ ズ ゼ ゾ ダ ヂ ヅ デ ド バ ビ ブ ベ ボ パ ピ プ ペ ポ',
          u'ア イ ウ エ オ カ キ ク ケ コ サ シ ス セ ソ タ チ ツ テ ト ' + \
          u'ナ ニ ヌ ネ ノ ハ ヒ フ ヘ ホ マ ミ ム メ モ ヤ ユ ヨ ラ リ ル レ ロ ' + \
          u'ワ ヲ ン ァ ィ ゥ ェ ォ ャ ュ ョ ッ']
  half = [u'ｶﾞ ｷﾞ ｸﾞ ｹﾞ ｺﾞ ｻﾞ ｼﾞ ｽﾞ ｾﾞ ｿﾞ ﾀﾞ ﾁﾞ ﾂﾞ ﾃﾞ ﾄﾞ ﾊﾞ ﾋﾞ ﾌﾞ ﾍﾞ ﾎﾞ ﾊﾟ ﾋﾟ ﾌﾟ ﾍﾟ ﾎﾟ',
          u'ｱ ｲ ｳ ｴ ｵ ｶ ｷ ｸ ｹ ｺ ｻ ｼ ｽ ｾ ｿ ﾀ ﾁ ﾂ ﾃ ﾄ ﾅ ﾆ ﾇ ﾈ ﾉ ﾊ ﾋ ﾌ ﾍ ﾎ ﾏ ﾐ ﾑ ﾒ ﾓ ﾔ ﾕ ﾖ ﾗ ﾘ ﾙ ﾚ ﾛ ' + \
          u'ﾜ ｦ ﾝ ｧ ｨ ｩ ｪ ｫ ｬ ｭ ｮ ｯ']
  wnum = [u'０ １ ２ ３ ４ ５ ６ ７ ８ ９']
  hnum = [u'0 1 2 3 4 5 6 7 8 9']
  walp = [u'ａ ｂ ｃ ｄ ｅ ｆ ｇ ｈ ｉ ｊ ｋ ｌ ｍ ｎ ｏ ｐ ｑ ｒ ｓ ｔ ｕ ｖ ｗ ｘ ｙ ｚ ' + \
          u'Ａ Ｂ Ｃ Ｄ Ｅ Ｆ Ｇ Ｈ Ｉ Ｊ Ｋ Ｌ Ｍ Ｎ Ｏ Ｐ Ｑ Ｒ Ｓ Ｔ Ｕ Ｖ Ｗ Ｘ Ｙ Ｚ']
  halp = [u'a b c d e f g h i j k l m n o p q r s t u v w x y z ' + \
          u'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z']
  char_sets = [hira, kata, half, wnum, hnum, walp, halp]

if __name__ == '__main__':
  import codecs, sys
  sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
  
  print convert(u'あいうえお', jcconv.HIRA, jcconv.HALF)
  print convert(u'ばいおりん', jcconv.HIRA, jcconv.HALF)
  print convert(u'ﾊﾞｲｵﾘﾝ', jcconv.HALF, jcconv.HIRA)
  print convert(u'12345', jcconv.HNUM, jcconv.WNUM)
