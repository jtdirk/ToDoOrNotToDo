from datetime import datetime, timedelta
import json
from timeloop import Timeloop
import copy

class TodoJSON():
    
    tl = Timeloop()
    undoHistorySize = 10
    
    def __init__(self) -> None:
        global d
        with open('todo.json', encoding='utf-8') as json_file:
            self.data = json.load(json_file)
        
        d = self.data
        self.undoHistory = []
        self.redoHistory = []
        # TodoJSON.tl.start()

    @tl.job(interval=timedelta(seconds=1))
    def save():
        global triggerTimeStamp
        global d
        if (datetime.now() - triggerTimeStamp) >= timedelta(seconds=2):
            with open("todo.json", mode="w", encoding='utf-8') as json_file:
                json.dump(d, json_file, ensure_ascii=False)
            triggerTimeStamp = datetime.max

    def isUndoAvailable(self):
        if not self.undoHistory:
            return False
        elif (len(self.undoHistory) < 2):
            return False
        return True

    def isRedoAvailable(self):
        if not self.redoHistory:
            return False
        elif (len(self.redoHistory) < 1):
            return False
        return True

    def redo(self):
        if self.isRedoAvailable():
            self.data = copy.deepcopy(self.redoHistory[len(self.redoHistory) - 1])
            self.undoHistory.append(copy.deepcopy(self.data))
            self.redoHistory.pop()
            return True
        
        return False

    def undo(self):
        if self.isUndoAvailable():
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
        global triggerTimeStamp
        triggerTimeStamp = datetime.now()

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
            self.setCompletionDate(projectNr, taskNr, datetime.today().strftime("%d.%m.%Y"))
        self.modified()

    def appendTask(self, projectNr):
        self.data["projects"][projectNr]["tasks"].append({"text": "neuer Task", "creationDate": datetime.today().strftime("%d.%m.%Y"), "completionDate": ""})
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
