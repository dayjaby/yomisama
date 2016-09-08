rm yomichan.zip
7z a yomichan.zip -x!pattern -x!yomi_base/languages/spanish/es-eng.txt -x!yomi_base/languages/german/de-eng.txt  -x!yomi_base/languages/german/de-eng.txt.db -x!yomi_base/languages/japanese/dictionary.zip -x!yomi_base/languages/japanese/dictionary.db -x!yomi_base/languages/chinese/cedict_ts.u8 -x!yomi_base/languages/korean/dictionary.db -x!yomi_base/languages/korean/dictionary.zip -x!yomi_base/mplayer/subfont.ttf yomichan.py UserList.py yomi_base 
cd pysrt
7z a ../yomichan.zip pysrt
cd ..
