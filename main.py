# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
from projectlistmodel import ProjectListModel
from trayicon import SystemTrayIcon
from settings import Settings
from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide6.QtWidgets import QApplication

CURRENT_DIRECTORY = Path(__file__).resolve().parent

if __name__ == "__main__":
    icon = QIcon("Liste.svg")

    app = QApplication(sys.argv)
    app.setWindowIcon(icon)
    
    trayIcon = SystemTrayIcon()
    settings = Settings()

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("trayIcon", trayIcon)
    engine.rootContext().setContextProperty("settings", settings)

    qmlRegisterType(ProjectListModel, "ProjectListModel", 1, 0, "ProjectListModel")

    filename = os.fspath(CURRENT_DIRECTORY / "main.qml")
    url = QUrl.fromLocalFile(filename)

    engine.load(url)
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())