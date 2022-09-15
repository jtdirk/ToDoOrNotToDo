from PySide6.QtCore import (QAbstractListModel, QByteArray, QModelIndex, Qt, Slot)
import pytodotxt
from datetime import datetime, timedelta
from timeloop import Timeloop

triggerTimeStamp = datetime.max

class TaskListModel(QAbstractListModel):
    CreationDateRole = Qt.UserRole + 1
    CompletionDateRole = Qt.UserRole + 2
    IsCompletedRole = Qt.UserRole + 3
    CreationDateChangedRole = Qt.UserRole + 4
    CompletionDateChangedRole = Qt.UserRole + 5

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.tasks = []

    def modified(self):
        global triggerTimeStamp
        triggerTimeStamp = datetime.now()

    def rowCount(self, parent=QModelIndex()):
        return len(self.tasks)

    def data(self, index, role: int):
        if not self.tasks:
            ret = None
        elif not index.isValid():
            ret = None
        elif role == Qt.DisplayRole:
            ret = self.tasks[index.row()]["text"]
        elif role == self.CreationDateRole:
            ret = self.tasks[index.row()]["creationDate"]
        elif role == self.CompletionDateRole:
            ret = self.tasks[index.row()]["completionDate"]
        elif role == self.IsCompletedRole:
            ret = self.tasks[index.row()]["isCompleted"]
        else:
            ret = None

        return ret

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        if role == Qt.EditRole:
            self.tasks[index.row()]["text"] = value
            self.modified()
        elif role == self.CreationDateChangedRole:
            self.tasks[index.row()]["creationDate"] = value
            self.modified()
        elif role == self.CompletionDateChangedRole:
            self.tasks[index.row()]["completionDate"] = value
            self.modified()
        return True

    def roleNames(self):
        default = super().roleNames()
        default[self.CreationDateRole] = QByteArray(b"creationDate")
        default[self.CompletionDateRole] = QByteArray(b"completionDate")
        default[self.IsCompletedRole] = QByteArray(b"isCompleted")
        default[self.CreationDateChangedRole] = QByteArray(b"creationDateChanged")
        default[self.CompletionDateChangedRole] = QByteArray(b"completionDateChanged")
        return default

    @Slot(result=bool)
    def append(self, task = "neuer Task", creationDate = datetime.today().strftime("%d.%m.%Y"), completionDate = "01.01.0001", is_completed = False):
        """Slot to append a row at the end"""
        result = self.insertRow(self.rowCount())
        if result:
            self.tasks[self.rowCount() - 1]["text"] = task
            self.tasks[self.rowCount() - 1]["creationDate"] = creationDate
            self.tasks[self.rowCount() - 1]["completionDate"] = completionDate
            self.tasks[self.rowCount() - 1]["isCompleted"] = is_completed
            self.dataChanged.emit(self.index(self.rowCount() - 1), self.index(self.rowCount() - 1))
            self.modified()
        return result


    def insertRow(self, row):
        """Insert a single row at row"""
        return self.insertRows(row, 0)

    def insertRows(self, row: int, count, index=QModelIndex()):
        """Insert n rows (n = 1 + count)  at row"""

        self.beginInsertRows(QModelIndex(), row, row + count)
        self.tasks.append({"text": "", "creationDate": "", "completionDate": "", "isCompleted": False})
        self.endInsertRows()

        return True

    @Slot(int, result=bool)
    def remove(self, row: int):
        """Slot to remove one row"""
        if self.removeRow(row):
            ret = True
            self.modified()
        return ret

    def removeRow(self, row, parent=QModelIndex()):
        """Remove one row at index row"""
        return self.removeRows(row, 0, parent)

    def removeRows(self, row: int, count: int, parent=QModelIndex()):
        """Remove n rows (n=1+count) starting at row"""
        self.beginRemoveRows(QModelIndex(), row, row + count)

        # start database work
        self.tasks = self.tasks[:row] + self.tasks[row + count + 1 :]
        # end database work

        self.endRemoveRows()
        return True

    @Slot(int, str, result = bool)
    def completeTask(self, row: int, completionDate):
        self.tasks[row]["isCompleted"] = not self.tasks[row]["isCompleted"]
        if self.tasks[row]["isCompleted"]:
            self.tasks[row]["completionDate"] = completionDate
        self.dataChanged.emit(self.index(row), self.index(row))
        
        self.modified()

        return True

class ProjectListModel(QAbstractListModel):

    projects = []
    timeLoop = Timeloop()

    TaskRole = Qt.UserRole + 1
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.openTodotxt()
        self.timeLoop.start()

    def save():
        todotxtSave = pytodotxt.TodoTxt("todosave.txt")
        for p in ProjectListModel.projects:
            print(p["tasks"])

        #print(ProjectListModel.projects)
        return True

    @timeLoop.job(interval=timedelta(seconds=1))
    def timeLoopJob():
        global triggerTimeStamp
        if (datetime.now() - triggerTimeStamp) >= timedelta(seconds=2):
            ProjectListModel.save()
            triggerTimeStamp = datetime.max

    def modified(self):
        global triggerTimeStamp
        triggerTimeStamp = datetime.now()

    def rowCount(self, parent=QModelIndex()):
        return len(ProjectListModel.projects)

    def data(self, index, role: int):
        if not ProjectListModel.projects:
            ret = None
        elif not index.isValid():
            ret = None
        elif role == Qt.DisplayRole:
            ret = ProjectListModel.projects[index.row()]["project"]
        elif role == ProjectListModel.TaskRole:
            ret = ProjectListModel.projects[index.row()]["tasks"]
        else:
            ret = None

        return ret

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        if role == Qt.EditRole:
            ProjectListModel.projects[index.row()]["project"] = value
            self.modified()
        
        return True

    @Slot(result=bool)
    def append(self, project = "neues Projekt"):
        """Slot to append a row at the end"""
        result = self.insertRow(self.rowCount())
        if result:
            ProjectListModel.projects[self.rowCount() - 1]["project"] = project
            self.dataChanged.emit(self.index(self.rowCount() - 1), self.index(self.rowCount() - 1))
            self.modified()
        return result


    def insertRow(self, row):
        """Insert a single row at row"""
        return self.insertRows(row, 0)

    def insertRows(self, row: int, count, index=QModelIndex()):
        """Insert n rows (n = 1 + count)  at row"""

        self.beginInsertRows(QModelIndex(), row, row + count)
        t = TaskListModel()
        t.append("neuer Task")
        ProjectListModel.projects.append({"project": "", "tasks": t})
        self.endInsertRows()

        return True

    @Slot(int, result=bool)
    def remove(self, row: int):
        """Slot to remove one row"""
        if self.removeRow(row):
            ret = True
            self.modified()
        return ret

    def removeRow(self, row, parent=QModelIndex()):
        """Remove one row at index row"""
        return self.removeRows(row, 0, parent)

    def removeRows(self, row: int, count: int, parent=QModelIndex()):
        """Remove n rows (n=1+count) starting at row"""
        self.beginRemoveRows(QModelIndex(), row, row + count)

        # start database work
        ProjectListModel.projects = ProjectListModel.projects[:row] + ProjectListModel.projects[row + count + 1 :]
        # end database work

        self.endRemoveRows()
        return True

    def roleNames(self):
        default = super().roleNames()
        default[self.TaskRole] = QByteArray(b"tasks")
        return default

    def openTodotxt(self):
        self.todotxt = pytodotxt.TodoTxt('todo.txt')
        self.todotxt.parse()

        for task in self.todotxt.tasks:
            project = ""
            if task.projects:
                project = task.projects[0]

            already_exists = False
            for i in range(len(ProjectListModel.projects)):
                if ProjectListModel.projects[i]["project"] == project:
                    already_exists = True

            if not already_exists:
                ProjectListModel.projects.append({"project": project, "tasks": self.tasksByProject(project)})


    def tasksByProject(self, project):
        tlm = TaskListModel()
        for task in self.todotxt.tasks:
            if task.projects[0] == project:
                if task.completion_date == None:
                    cd = "01.01.0001"
                else:
                    cd = task.completion_date.strftime("%d.%m.%Y")
                    
                tlm.append(task.bare_description(), task.creation_date.strftime("%d.%m.%Y"), cd, task.is_completed)
        
        return tlm

