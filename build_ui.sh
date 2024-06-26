#!/bin/bash
pushd ui
pyuic6 -o ../yomi_base/gen/about.py about.ui
pyuic6 -o ../yomi_base/gen/preferences.py preferences.ui
pyuic6 -o ../yomi_base/gen/reader.py reader.ui
pyuic6 -o ../yomi_base/gen/updates.py updates.ui
# pyqt6rc -o ../yomi_base/gen about.ui
# pyqt6rc -o ../yomi_base/gen preferences.ui
# pyqt6rc -o ../yomi_base/gen reader.ui
# pyqt6rc -o ../yomi_base/gen updates.ui
popd
pyside6-rcc ui/resources.qrc | sed '0,/PySide6/s//PyQt6/' > yomi_base/gen/resources_rc.py
