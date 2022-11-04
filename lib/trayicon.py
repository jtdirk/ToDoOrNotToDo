from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtCore import Signal



class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, appName, icon, parent=None):
        QSystemTrayIcon.__init__(self)

        self.appName = appName
        self.icon = icon
        self.setIcon(self.icon)

        menu = QMenu(parent)
        self._exit_action = menu.addAction("Beenden", self.on_exit_click)

        self.setContextMenu(menu)

        self.activated.connect(self.on_icon_click)
        self.messageClicked.connect(self.on_message_clicked)

        self.setToolTip(self.appName)
        self.show()
        self.showMessage(self.appName + " gestartet", "Klicken Sie hier, um das Programmfenster anzuzeigen.", self.icon)

    exitClicked = Signal()
    iconClicked = Signal()

    def on_exit_click(self):
        self.exitClicked.emit()
        exit(0)

    def on_icon_click(self, reason):
        if reason == self.Trigger:
            self.iconClicked.emit()

    def on_message_clicked(self):
        self.iconClicked.emit()
