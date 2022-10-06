from PySide6.QtCore import QObject, Property, Signal

class PropertiesModel(QObject):
    def __init__(self):
        QObject.__init__(self)
        self._person_name = "Hallo"

    def _name(self):
        return self._person_name

    @Signal
    def name_changed(self):
        pass

    name = Property(str, _name, notify=name_changed)