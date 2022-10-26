from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtCore import Signal, Property



class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        QSystemTrayIcon.__init__(self)

        self.event_exit_click = None

        self._mainwindowIsVisible = True
        self.icon = QIcon("Liste.svg")
        self.setIcon(self.icon)

        menu = QMenu(parent)
        self._exit_action = menu.addAction("Exit", self.on_exit_click)

        self.setContextMenu(menu)

        self.activated.connect(self.on_icon_click)
        self.show()

    def on_exit_click(self):
        self.fire_exit_click()
        exit(0)

    def fire_exit_click(self):
        if self.event_exit_click:
            self.event_exit_click(self)

    def on_icon_click(self, reason):
        if reason == self.Trigger:
            if self._mainwindowIsVisible:
                self._mainwindowIsVisible = False
            else:
                self._mainwindowIsVisible = True
            
            self.mainwindowIsVisible_changed.emit()

    def _mainwindowIsVisible(self):
        return self._mainwindowIsVisible

    def setMainwindowIsVisible(self, value):
        self._mainwindowIsVisible = value
        self.mainwindowIsVisible_changed.emit()

    @Signal
    def mainwindowIsVisible_changed(self):
        pass

    mainwindowIsVisible = Property(bool, _mainwindowIsVisible, setMainwindowIsVisible, notify=mainwindowIsVisible_changed)