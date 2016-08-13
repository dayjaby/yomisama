cd yomi_base/japanese
7z a dictionary.zip dictionary.db

cd ../korean
7z a dictionary.zip dictionary.db

cd ../..

rm yomichan_dicts.zip
7z a yomichan_dicts.zip yomi_base/japanese/dictionary.db yomi_base/chinese/cedict_ts.u8 yomi_base/korean/dictionary.db

rm tools.zip
7z a tools.zip tools yomi_base/mplayer/subfont.ttf

call build_zip_core.bat

