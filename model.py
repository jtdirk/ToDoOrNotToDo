from PySide6.QtCore import (QAbstractListModel, QByteArray, QModelIndex, Qt, Slot)
import pytodotxt
from datetime import datetime, timedelta
from timeloop import Timeloop

triggerTimeStamp = datetime.max

class TodoTxtData():
    def __init__(self, parent=None):
        self.openTodotxt()

    def openTodotxt(self):
        self.todotxt = pytodotxt.TodoTxt('todo.txt')
        self.todotxt.parse()

    def getProjects(self):
        projects = []
        
        for task in self.todotxt.tasks:
            project = ""
            if task.projects:
                project = task.projects[0]

            already_exists = False
            for i in range(len(projects)):
                if projects[i] == project:
                    already_exists = True

            if not already_exists:
                projects.append(project)
        
        return projects

    def projectCount(self):
        return len(self.getProjects())

    def setProject(self, nr, newProject):
        oldProject = self.getProjects()[nr]
        for t in self.todotxt.tasks:
            t.replace_project(oldProject, newProject)

    def getTasks(self, project):
        tasks = []
        
        for task in self.todotxt.tasks:
            if task.projects:
                if task.projects[0] == project:
                    tasks.append(task)
        
        return tasks

    def taskCount(self, project):
        return len(self.getTasks(project))

    def setDescription(self, project, nr, description):
        tasks = self.getTasks(project)
        tasks[nr].description = description + ' +' + project

    def setCreationDate(self, project, nr, date):
        tasks = self.getTasks(project)
        tasks[nr].creation_date = datetime.strptime(date, "%d.%m.%Y")

    def setCompletionDate(self, project, nr, date):
        tasks = self.getTasks(project)
        tasks[nr].completion_date = datetime.strptime(date, "%d.%m.%Y")

    def getCompletion(self, project, nr):
        tasks = self.getTasks(project)
        return tasks[nr].is_completed

    def setCompletion(self, project, nr, isCompleted):
        tasks = self.getTasks(project)
        tasks[nr].is_completed = isCompleted

    def appendTask(self, description, creationDate, completionDate, project, isCompleted):
        task = pytodotxt.Task()
        task.description = description + " +" + project
        task.creation_date = datetime.strptime(creationDate, "%d.%m.%Y")
        task.completion_date = datetime.strptime(completionDate, "%d.%m.%Y")
        task.is_completed = isCompleted
        self.todotxt.add(task)
    
todoTxtData = TodoTxtData()

class TaskListModel(QAbstractListModel):
    CreationDateRole = Qt.UserRole + 1
    CompletionDateRole = Qt.UserRole + 2
    IsCompletedRole = Qt.UserRole + 3
    CreationDateChangedRole = Qt.UserRole + 4
    CompletionDateChangedRole = Qt.UserRole + 5

    def __init__(self, project, parent=None):
        super().__init__(parent=parent)
        self.project = project

    def rowCount(self, parent=QModelIndex()):
        ret = todoTxtData.taskCount(self.project)
        return ret

    def data(self, index, role: int):
        if not todoTxtData.getTasks(self.project): #self.tasks:
            ret = None
        elif not index.isValid():
            ret = None
        elif role == Qt.DisplayRole:
            ret = todoTxtData.getTasks(self.project)[index.row()].bare_description()
        elif role == self.CreationDateRole:
            ret = todoTxtData.getTasks(self.project)[index.row()].creation_date.strftime("%d.%m.%Y")
        elif role == self.CompletionDateRole:
            if todoTxtData.getTasks(self.project)[index.row()].completion_date == None:
                ret = "01.01.0001"
            else:
                ret = todoTxtData.getTasks(self.project)[index.row()].completion_date.strftime("%d.%m.%Y")
        elif role == self.IsCompletedRole:
            ret = todoTxtData.getTasks(self.project)[index.row()].is_completed
        else:
            ret = None

        return ret

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        if role == Qt.EditRole:
            todoTxtData.setDescription(self.project, index.row(), value)
        elif role == self.CreationDateChangedRole:
            todoTxtData.setCreationDate(self.project, index.row(), value)
        elif role == self.CompletionDateChangedRole:
            todoTxtData.setCompletionDate(self.project, index.row(), value)
        elif role == self.IsCompletedRole:
            todoTxtData.setCompletion(self.project, index.row(), value)
            self.dataChanged.emit(index, index, role)
        
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
    # def append(self, task = "neuer Task", creationDate = datetime.today().strftime("%d.%m.%Y"), completionDate = "01.01.0001", is_completed = False):
    def append(self):
        """Slot to append a row at the end"""
        self.layoutAboutToBeChanged.emit()
        result = self.insertRow(self.rowCount())
        self.layoutChanged.emit()

        return result


    def insertRow(self, row):
        """Insert a single row at row"""
        return self.insertRows(row, 0)

    def insertRows(self, row: int, count, index=QModelIndex()):
        """Insert n rows (n = 1 + count)  at row"""

        self.beginInsertRows(QModelIndex(), row, row + count)
        todoTxtData.appendTask("neuer Task", datetime.today().strftime("%d.%m.%Y"), "01.01.0001", self.project, False)
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

class ProjectListModel(QAbstractListModel):

    timeLoop = Timeloop()

    TaskRole = Qt.UserRole + 1
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.timeLoop.start()

    def save():
        todotxtSave = pytodotxt.TodoTxt("todosave.txt")
        for p in todoTxtData.getProjects(): # ProjectListModel.projects:
            for t in todoTxtData.getTasks(p): # p["tasks"].dataList():
                # print(t.bare_description())
                pass

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
        return todoTxtData.projectCount()

    def data(self, index, role: int):
        if not todoTxtData.getProjects():
            ret = None
        elif not index.isValid():
            ret = None
        elif role == Qt.DisplayRole:
            ret = todoTxtData.getProjects()[index.row()]
        elif role == ProjectListModel.TaskRole:
            ret = TaskListModel(todoTxtData.getProjects()[index.row()])
        else:
            ret = None

        return ret

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        if role == Qt.EditRole:
            todoTxtData.setProject(index.row(), value)
        
        return True

    @Slot(result=bool)
    def append(self, project = "neues Projekt"):
        """Slot to append a row at the end"""
        result = self.insertRow(self.rowCount())
        if result:
            ProjectListModel.projects[self.rowCount() - 1]["project"] = project
            self.dataChanged.emit(self.index(self.rowCount() - 1), self.index(self.rowCount() - 1))
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
