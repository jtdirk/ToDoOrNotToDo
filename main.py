# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

CURRENT_DIRECTORY = Path(__file__).resolve().parent

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    filename = os.fspath(CURRENT_DIRECTORY / "main.qml")
    url = QUrl.fromLocalFile(filename)

    engine.load(url)
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())