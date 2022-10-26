from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtCore import Signal, Property



class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        QSystemTrayIcon.__init__(self)

        self.icon = QIcon("Liste.svg")
        self.setIcon(self.icon)

        menu = QMenu(parent)
        self._exit_action = menu.addAction("Exit", self.on_exit_click)

        self.setContextMenu(menu)

        self.activated.connect(self.on_icon_click)
        self.show()

    exitClicked = Signal()
    iconClicked = Signal()

    def on_exit_click(self):
        self.exitClicked.emit()
        exit(0)

    def on_icon_click(self, reason):
        if reason == self.Trigger:
            self.iconClicked.emit()
