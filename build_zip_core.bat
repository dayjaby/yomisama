rm yomichan.zip
7z a yomichan.zip -x!yomi_base/japanese/dictionary.zip -x!yomi_base/japanese/dictionary.db -x!yomi_base/chinese/cedict_ts.u8 -x!yomi_base/korean/dictionary.db -x!yomi_base/korean/dictionary.zip -x!yomi_base/mplayer/subfont.ttf yomichan.py UserList.py yomi_base 
cd pysrt
7z a ..\yomichan.zip pysrt
cd ..