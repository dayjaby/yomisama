rm yomichan.zip
7z a yomichan.zip -x!yomi_base/japanese -x!yomi_base/chinese -x!yomi_base/korean -x!yomi_base/mplayer/subfont.ttf yomichan.py UserList.py yomi_base 
cd pysrt
7z a ..\yomichan.zip pysrt