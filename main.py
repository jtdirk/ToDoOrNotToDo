# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
from model import ProjectListModel, TodoTXTModel

from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType

CURRENT_DIRECTORY = Path(__file__).resolve().parent

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    qmlRegisterType(ProjectListModel, "ProjectListModel", 1, 0, "ProjectListModel")
    qmlRegisterType(TodoTXTModel, "TodoTXTModel", 1, 0, "TodoTXTModel")

    filename = os.fspath(CURRENT_DIRECTORY / "main.qml")
    url = QUrl.fromLocalFile(filename)

    # setup()
    engine.load(url)
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())