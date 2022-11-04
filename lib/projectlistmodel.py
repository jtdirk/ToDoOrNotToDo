from PySide6.QtCore import (QAbstractListModel, QByteArray, QModelIndex, Qt, Slot, Property, Signal)
from lib.todojson import TodoJSON
from lib.tasklistmodel import TaskListModel

class ProjectListModel(QAbstractListModel):

    TaskRole = Qt.UserRole + 1
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.todoData = None
    
    def setTodoDatafile(self, file):
        self.todoData = TodoJSON(file)
        self.todoData.isUndoAvailable_changed.connect(self.iua_changed)
        self.todoData.isRedoAvailable_changed.connect(self.ira_changed)
        self.todoData.unsavedChanges_changed.connect(self.uc_changed)
        self.todoDatafile_changed.emit()
        self.layoutChanged.emit()

    def getTodoDatafile(self):
        return self.todoData.todoFile

    todoDatafile_changed = Signal()

    todoDataFile = Property(str, getTodoDatafile, setTodoDatafile, notify=todoDatafile_changed)

    @Slot()
    def saveData(self):
        self.todoData.save()
        
    def _isUndoAvailable(self):
        return self.todoData.isUndoAvailable

    @Slot()
    def iua_changed(self):
        self.isUndoAvailable_changed.emit()

    @Signal
    def isUndoAvailable_changed(self):
        pass

    isUndoAvailable = Property(bool, _isUndoAvailable, notify=isUndoAvailable_changed)

    def _isRedoAvailable(self):
        return self.todoData.isRedoAvailable
        
    @Slot()
    def ira_changed(self):
        self.isRedoAvailable_changed.emit()

    @Signal
    def isRedoAvailable_changed(self):
        pass

    isRedoAvailable = Property(bool, _isRedoAvailable, notify=isRedoAvailable_changed)

    def _unsavedChanges(self):
        if self.todoData.unsavedChanges:
            return True
        else:
            return False

    @Slot()
    def uc_changed(self):
        self.unsavedChanges_changed.emit()

    @Signal
    def unsavedChanges_changed(self):
        pass

    unsavedChanges = Property(bool, _unsavedChanges, notify = unsavedChanges_changed)

    def rowCount(self, parent=QModelIndex()):
        return self.todoData.projectCount()

    def data(self, index, role: int):
        if not self.todoData.getProjects():
            ret = None
        elif not index.isValid():
            ret = None
        elif role == Qt.DisplayRole:
            ret = self.todoData.getProjects()[index.row()]["name"]
        elif role == self.TaskRole:
            ret = TaskListModel(index.row(), self.todoData)
        else:
            ret = None

        return ret

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        if role == Qt.EditRole:
            self.todoData.setProject(index.row(), value)
        
        return True

    @Slot(result=bool)
    def redo(self):
        ret =self.todoData.redo()
        self.layoutChanged.emit()
        
        return ret

    @Slot(result=bool)
    def undo(self):
        ret =self.todoData.undo()
        if not self.todoData.isUndoAvailable:
            self.isUndoAvailable_changed.emit()
        self.layoutChanged.emit()
        
        return ret

    @Slot(result=bool)
    def append(self):
        result = self.insertRow(self.rowCount())
        
        return result

    def insertRow(self, row):
        return self.insertRows(row, 0)

    def insertRows(self, row: int, count, index=QModelIndex()):
        self.beginInsertRows(index, row, row + count)
        self.todoData.appendProject()
        self.endInsertRows()

        return True

    @Slot(int, result=bool)
    def remove(self, row: int):
        if self.removeRow(row):
            ret = True
        return ret

    def removeRow(self, row, parent=QModelIndex()):
        return self.removeRows(row, 0, parent)

    def removeRows(self, row: int, count: int, parent=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), row, row + count)
        self.todoData.removeProjects(row, count)
        self.endRemoveRows()

        return True

    def roleNames(self):
        default = super().roleNames()
        default[self.TaskRole] = QByteArray(b"tasks")
        return default
