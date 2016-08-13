./build_zip_core.bat

rm yomichan_dicts.zip
7z a yomichan_dicts.zip yomi_base/japanese/dictionary.db yomi_base/chinese/cedict_ts.u8 yomi_base/korean/dictionary.db

rm tools.zip
7z a tools.zip tools yomi_base/mplayer/subfont.ttf
