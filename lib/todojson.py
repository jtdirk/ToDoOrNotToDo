from PySide6.QtCore import QObject, Property, Signal, QTimer
from datetime import date
import json
import copy

class TodoJSON(QObject):
    
    undoHistorySize = 10
    
    def __init__(self, todoFile) -> None:
        QObject.__init__(self)

        self.todoFile = todoFile
        self.data = {"projects": []}
        self._unsavedChanges = False
        self.undoHistory = []
        self.redoHistory = []

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.save)

        try:
            json_file = open(self.todoFile, encoding='utf-8')
        except FileNotFoundError:
            open(self.todoFile, "x", encoding='utf-8')
            self.appendProject()
        else:
            self.data = json.load(json_file)

    @property
    def todoFile(self):
        return self._todoFile

    @todoFile.setter
    def todoFile(self, value):
        self._todoFile = value

    def save(self):
        with open(self.todoFile, mode="w", encoding='utf-8') as json_file:
            json.dump(self.data, json_file, ensure_ascii=False)
        self._unsavedChanges = False
        self.unsavedChanges_changed.emit()

    def _isUndoAvailable(self):
        if not self.undoHistory:
            return False
        elif (len(self.undoHistory) < 2):
            return False
        return True

    @Signal
    def isUndoAvailable_changed(self):
        pass

    isUndoAvailable = Property(bool, _isUndoAvailable, notify=isUndoAvailable_changed)

    def _isRedoAvailable(self):
        if not self.redoHistory:
            return False
        elif (len(self.redoHistory) < 1):
            return False
        return True

    @Signal
    def isRedoAvailable_changed(self):
        pass

    isRedoAvailable = Property(bool, _isRedoAvailable, notify=isRedoAvailable_changed)

    def _unsavedChanges(self):
        return self._unsavedChanges

    @Signal
    def unsavedChanges_changed(self):
        pass

    unsavedChanges = Property(bool, _unsavedChanges, notify = unsavedChanges_changed)

    def redo(self):
        if self.isRedoAvailable:
            self.data = copy.deepcopy(self.redoHistory[len(self.redoHistory) - 1])
            self.undoHistory.append(copy.deepcopy(self.data))
            self.redoHistory.pop()
            return True
        
        return False

    def undo(self):
        if self.isUndoAvailable:
            self.redoHistory.append(copy.deepcopy(self.undoHistory[len(self.undoHistory) - 1]))
            self.data = copy.deepcopy(self.undoHistory[len(self.undoHistory) - 2])
            self.undoHistory.pop()
            return True
        
        return False

    def modified(self):
        if not self.undoHistory:
            self.undoHistory.append(copy.deepcopy(self.data))
        elif (self.undoHistory[len(self.undoHistory) - 1] != self.data):
            self.undoHistory.append(copy.deepcopy(self.data))
            self.redoHistory.clear()
        while len(self.undoHistory) > TodoJSON.undoHistorySize:
            self.undoHistory.pop(0)
        self.isUndoAvailable_changed.emit()
        self.isRedoAvailable_changed.emit()
        self.timer.start(2000)
        self._unsavedChanges = True
        self.unsavedChanges_changed.emit()

    def projectCount(self):
        return len(self.data["projects"])

    def getProjects(self):
        return self.data["projects"]

    def setProject(self, projectNr, newProject):
        self.data["projects"][projectNr]["name"] = newProject
        self.modified()

    def getTasks(self, projectNr):
        return self.data["projects"][projectNr]["tasks"]

    def getTaskText(self, projectNr, taskNr):
        return self.data["projects"][projectNr]["tasks"][taskNr]["text"]

    def getCreationDate(self, projectNr, taskNr):
        return self.data["projects"][projectNr]["tasks"][taskNr]["creationDate"]

    def getDueDate(self, projectNr, taskNr):
        return self.data["projects"][projectNr]["tasks"][taskNr]["dueDate"]

    def getCompletionDate(self, projectNr, taskNr):
        return self.data["projects"][projectNr]["tasks"][taskNr]["completionDate"]

    def taskCount(self, projectNr):
        return len(self.data["projects"][projectNr]["tasks"])

    def setText(self, projectNr, taskNr, text):
        self.data["projects"][projectNr]["tasks"][taskNr]["text"] = text
        self.modified()

    def setCreationDate(self, projectNr, taskNr, date):
        self.data["projects"][projectNr]["tasks"][taskNr]["creationDate"] = date
        self.modified()

    def setDueDate(self, projectNr, taskNr, date):
        self.data["projects"][projectNr]["tasks"][taskNr]["dueDate"] = date
        self.modified()

    def setCompletionDate(self, projectNr, taskNr, date):
        self.data["projects"][projectNr]["tasks"][taskNr]["completionDate"] = date
        self.modified()
    
    def getCompletion(self, projectNr, taskNr):
        if not (self.data["projects"][projectNr]["tasks"][taskNr]["completionDate"] == ""):
            return True
        
        return False

    def toggleCompletion(self, projectNr, taskNr):
        if self.getCompletion(projectNr, taskNr):
            self.setCompletionDate(projectNr, taskNr, "")
        else:
            self.setCompletionDate(projectNr, taskNr, date.today().strftime("%d.%m.%Y"))
        self.modified()

    def appendTask(self, projectNr):
        self.data["projects"][projectNr]["tasks"].append({"text": "neuer Task", "creationDate": date.today().strftime("%d.%m.%Y"), "dueDate": date.today().strftime("%d.%m.%Y"), "completionDate": ""})
        self.modified()

    def appendProject(self):
        self.data["projects"].append({"name": "neues Projekt", "tasks": []})
        self.appendTask(self.projectCount() - 1)
        self.modified()
        
    def removeTasks(self, projectNr, startNr, count):
        del self.data["projects"][projectNr]["tasks"][startNr:startNr + count + 1]
        self.modified()

    def removeProjects(self, startNr, count):
        del self.data["projects"][startNr:startNr + count + 1]
        self.modified()
