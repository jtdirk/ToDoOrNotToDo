from PySide6.QtCore import (QAbstractListModel, QByteArray, QModelIndex, Qt, Slot)
from todojson import TodoJSON
from tasklistmodel import TaskListModel

class ProjectListModel(QAbstractListModel):

    TaskRole = Qt.UserRole + 1
    
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
        elif role == ProjectListModel.TaskRole:
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
