rm yomichan.zip
7z a yomichan.zip -x!yomi_base/japanese -x!yomi_base/chinese -x!yomi_base/korean -x!yomi_base/mplayer/subfont.ttf yomichan.py UserList.py yomi_base 
cd pysrt
7z a ..\yomichan.zip pysrt

rm yomichan_dicts.zip
7z a yomichan_dicts.zip yomi_base/japanese yomi_base/chinese yomi_base/korean

rm tools.zip
7z a tools.zip tools yomi_base/mplayer/subfont.ttf
