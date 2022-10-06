from PySide6.QtCore import (QAbstractListModel, QByteArray, QModelIndex, Qt, Slot)
from todojson import TodoJSON
from tasklistmodel import TaskListModel

class ProjectListModel(QAbstractListModel):

    TaskRole = Qt.UserRole + 1
    IsUndoAvailableRole = Qt.UserRole + 2
    TestRole = Qt.UserRole + 3
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.todoData = TodoJSON()

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
        elif role == self.TestRole:
            ret = "Test"
        elif role == self.IsUndoAvailableRole:
            ret = self.todoData.isUndoAvailable()
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
        default[self.IsUndoAvailableRole] = QByteArray(b"isUndoAvailable")
        default[self.TestRole] = QByteArray(b"test")
        return default
