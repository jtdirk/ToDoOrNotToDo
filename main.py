# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
from model import BaseModel
import pytodotxt

from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType

projectList = []

def openTodotxt():
    todotxt = pytodotxt.TodoTxt('todo.txt')
    todotxt.parse()

    for task in todotxt.tasks:
        for project in task.projects:
            try:
                projectList.index(project)
            except:
                projectList.append(project)

    print(projectList)

def setup():
    openTodotxt()

CURRENT_DIRECTORY = Path(__file__).resolve().parent

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    qmlRegisterType(BaseModel, "BaseModel", 1, 0, "BaseModel")


    filename = os.fspath(CURRENT_DIRECTORY / "main.qml")
    url = QUrl.fromLocalFile(filename)

    setup()
    #engine.load(url)
    #if not engine.rootObjects():
    #    sys.exit(-1)
    #sys.exit(app.exec())