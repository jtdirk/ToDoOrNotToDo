from PySide6.QtCore import (QAbstractListModel, QByteArray, QModelIndex, Qt, Slot)

class TaskListModel(QAbstractListModel):
    CreationDateRole = Qt.UserRole + 1
    CompletionDateRole = Qt.UserRole + 2
    IsCompletedRole = Qt.UserRole + 3
    CreationDateChangedRole = Qt.UserRole + 4
    CompletionDateChangedRole = Qt.UserRole + 5
    ToggleCompletionRole = Qt.UserRole + 6

    def __init__(self, project, todoData, parent=None):
        super().__init__(parent=parent)
        self.project = project
        self.todoData = todoData

    def rowCount(self, parent=QModelIndex()):
        return self.todoData.taskCount(self.project)

    def data(self, index, role: int):
        if not self.todoData.getTasks(self.project):
            ret = None
        elif not index.isValid():
            ret = None
        elif role == Qt.DisplayRole:
            ret = self.todoData.getTaskText(self.project, index.row())
        elif role == self.CreationDateRole:
            ret = self.todoData.getCreationDate(self.project, index.row())
        elif role == self.CompletionDateRole:
            ret = self.todoData.getCompletionDate(self.project, index.row())
        elif role == self.IsCompletedRole:
            ret = self.todoData.getCompletion(self.project, index.row())
        else:
            ret = None

        return ret

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        if role == Qt.EditRole:
            self.todoData.setText(self.project, index.row(), value)
        elif role == self.CreationDateChangedRole:
            self.todoData.setCreationDate(self.project, index.row(), value)
        elif role == self.CompletionDateChangedRole:
            self.todoData.setCompletionDate(self.project, index.row(), value)
        elif role == self.ToggleCompletionRole:
            self.todoData.toggleCompletion(self.project, index.row())
            self.dataChanged.emit(index.row(), index.row())
        
        return True

    def roleNames(self):
        default = super().roleNames()
        default[self.CreationDateRole] = QByteArray(b"creationDate")
        default[self.CompletionDateRole] = QByteArray(b"completionDate")
        default[self.IsCompletedRole] = QByteArray(b"isCompleted")
        default[self.CreationDateChangedRole] = QByteArray(b"creationDateChanged")
        default[self.CompletionDateChangedRole] = QByteArray(b"completionDateChanged")
        default[self.ToggleCompletionRole] = QByteArray(b"toggleCompletion")

        return default

    @Slot(int, result=bool)
    def toggleCompletion(self, row: int):
        self.todoData.toggleCompletion(self.project, row)
        self.dataChanged.emit(self.index(row), self.index(row))
        return True

    @Slot(result=bool)
    def append(self):
        result = self.insertRow(self.rowCount())

        return result

    def insertRow(self, row):
        return self.insertRows(row, 0)

    def insertRows(self, row: int, count, index=QModelIndex()):
        self.beginInsertRows(index, row, row + count)
        self.todoData.appendTask(self.project)
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
        self.todoData.removeTasks(self.project, row, count) 
        self.endRemoveRows()
        return True
