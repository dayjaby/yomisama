#!/bin/sh
pyuic5 --import-from=. ui/about.ui -o yomi_base/gen/about_ui.py
pyuic5 --import-from=. ui/preferences.ui -o yomi_base/gen/preferences_ui.py
pyuic5 --import-from=. ui/reader.ui -o yomi_base/gen/reader_ui.py
pyuic5 --import-from=. ui/updates.ui -o yomi_base/gen/updates_ui.py
pyrcc5 ui/resources.qrc -o yomi_base/gen/resources_rc.py
