from PySide6.QtCore import QObject, Property, Signal
import json

class Settings(QObject):

    filename = 'settings.json'
    defaultSettings = {"datafile": "todo.json", "hideCompleted": False}

    def __init__(self):
        QObject.__init__(self)

        try:
            json_file = open(Settings.filename, encoding='utf-8')
        except FileNotFoundError:
            json_file = open(Settings.filename, "x", encoding='utf-8')
            self.saveSettings(Settings.defaultSettings)
            json_file = open(Settings.filename, encoding='utf-8')
        finally:
            self.data = json.load(json_file)
        
    def saveSettings(self, settings):
        with open(Settings.filename, mode="w", encoding='utf-8') as json_file:
            json.dump(settings, json_file, ensure_ascii=False)

    def getDatafile(self):
        return self.data["datafile"]
    
    def setDatafile(self, value):
        self.data["datafile"] = value
        self.saveSettings(self.data)
        self.datafile_changed.emit()

    datafile_changed = Signal()

    datafile = Property(str, getDatafile, setDatafile, notify=datafile_changed)

    def getHideCompleted(self):
        return self.data["hideCompleted"]
    
    def setHideCompleted(self, value):
        self.data["hideCompleted"] = value
        self.saveSettings(self.data)
        self.hideCompleted_changed.emit()

    hideCompleted_changed = Signal()

    hideCompleted = Property(bool, getHideCompleted, setHideCompleted, notify=hideCompleted_changed)
