from datetime import datetime, timedelta
import json
from timeloop import Timeloop

class TodoJSON():
    
    tl = Timeloop()
    
    def __init__(self) -> None:
        global d
        with open('todo.json', encoding='utf-8') as json_file:
            self.data = json.load(json_file)
        
        d = self.data
        TodoJSON.tl.start()

    @tl.job(interval=timedelta(seconds=1))
    def save():
        global triggerTimeStamp
        global d
        if (datetime.now() - triggerTimeStamp) >= timedelta(seconds=2):
            with open("todo.json", mode="w", encoding='utf-8') as json_file:
                json.dump(d, json_file, ensure_ascii=False)
            triggerTimeStamp = datetime.max

    def modified(self):
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
            todoData.setCompletionDate(projectNr, taskNr, "")
        else:
            todoData.setCompletionDate(projectNr, taskNr, datetime.today().strftime("%d.%m.%Y"))
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
