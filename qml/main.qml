import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Dialogs
import "."
import ProjectListModel

ApplicationWindow {
    id: windowMainWindow

    property bool reallyClose: false

    width: 640
    height: 480
    visible: false
    color: MyStyle.general.color

    title: appName
    Binding on title {
        when: projectListModel.unsavedChanges
        value: appName + " *"
    }

    Component.onCompleted: {
        projectListModel.saveData()
        hideCompletedButton.checked = settings.hideCompleted
    }

    Connections {
        target: trayIcon

        function onExitClicked() {
            projectListModel.saveData()
        }

        function onIconClicked() {
            if(!windowMainWindow.visible) {
                windowMainWindow.visible = true
                windowMainWindow.raise()
                windowMainWindow.requestActivate()
            } else {
                windowMainWindow.hide()
            }
        }
    }
    
    onClosing: function(close) {
        if (!reallyClose){
            close.accepted = false
            windowMainWindow.hide()
        }
        else {
            projectListModel.saveData()
        }
    }

    ProjectListModel {
        id: projectListModel

        todoDataFile: settings.datafile
    }

    Dialog {
        id: settingsDialog
        title: "Einstellungen"
        modal: true
        standardButtons: Dialog.Ok// | Dialog.Cancel

        FileDialog {
            id: fileDialog
            nameFilters: ["JSON Dateien (*.json)", "Alle Dateien (*)"]
            defaultSuffix: "json"
            fileMode: FileDialog.SaveFile
            options: FileDialog.DontConfirmOverwrite

            onAccepted: settings.datafile = selectedFile.toString().replace("file:///","")
        }

        GridLayout {
            columns: 3
            Label {
                Layout.column: 0
                text: "Speicherort der ToDo-Daten:"
            }
            TextField {
                id: filePathTextField
                Layout.row: 0
                Layout.column: 1
                readOnly: true

                width: 300

                text: settings.datafile
            }
            Button {
                Layout.row: 0
                Layout.column: 2

                text: "Durchsuchen..."
                onClicked: fileDialog.open()
            }
        }
    }

    header: ToolBar {
        RowLayout {
            ToolButton {
                id: undoButton
                icon.source: "../images/undo.svg"
                enabled: projectListModel.isUndoAvailable
                opacity: 0.5
                Binding on opacity {
                    when: undoButton.enabled
                    value: 1
                }
                MyToolTip {
                    text: "Rückgängig"
                }
                onClicked: projectListModel.undo()
            }
            ToolButton {
                id: redoButton
                icon.source: "../images/redo.svg"
                enabled: projectListModel.isRedoAvailable
                opacity: 0.5
                Binding on opacity {
                    when: redoButton.enabled
                    value: 1
                }
                MyToolTip {
                    text: "Wiederherstellen"
                }
                onClicked: projectListModel.redo()
            }
            ToolButton {
                id: hideCompletedButton
                checkable: true
                icon.source: "../images/eye.svg"
                MyToolTip {
                    text: "Erledigte Tasks ausblenden"
                }
                onToggled: settings.hideCompleted = checked
            }
            ToolButton {
                id: settingsButoon
                icon.source: "../images/gear.svg"
                MyToolTip {
                    text: "Einstellungen"
                }
                onClicked: settingsDialog.open()
            }
            ToolButton {
                id: closeButton
                icon.source: "../images/close.svg"
                enabled: true
                MyToolTip {
                    text: "Beenden"
                }
                onClicked: {
                    reallyClose = true
                    windowMainWindow.close()
                }
            }
        }
    }

    footer: ToolBar {
        RowLayout {
            anchors.fill: parent
            Slider {
                id: slider
                Layout.alignment: Qt.AlignRight
                from: .4
                value: 1
                to: 5
                onMoved: MyStyle.general.scale = value
                ToolTip {
                    parent: slider.handle
                    visible: slider.pressed
                    text: slider.value.toFixed(1)
                    background: Rectangle {
                        color: "white"
                        border.color: "black"
                    }
                }
            }
        }
    }

    ScrollView {
        id: scrollView
        
        anchors.fill: parent

        contentWidth: availableWidth

        Flow{
            id: flow

            anchors.fill: parent

            spacing: MyStyle.element.margins

            Repeater {
                id: projectList

                anchors.fill: parent

                model: projectListModel

                delegate: Column {
                    id: column
                    
                    Project {
                        id: project
                        
                        text: display
                        onTextChanged: model.edit = text
                        onClose: projectListModel.remove(index)
                    }
                    Repeater {
                        id: taskList
                        model: tasks
                        delegate: Task {
                            text: display
                            creationDateText: creationDate
                            dueDateText: dueDate
                            isTaskDue: isDue
                            completionDateText: completionDate
                            isTaskCompleted: isCompleted
                            visible: true
                            Binding on visible {
                                when: (hideCompletedButton.checked && isTaskCompleted)
                                value: false
                            }
                            onTextChanged: model.edit = text
                            onClose: taskList.model.remove(index)
                            onComplete: taskList.model.toggleCompletion(index)
                            onCreationDateChanged: model.creationDateChanged = creationDateText
                            onDueDateChanged: model.dueDateChanged = dueDateText
                            onCompletionDateChanged: model.completionDateChanged = completionDateText
                        }
                    }

                    AddTaskButton {
                        id: addTaskButton
                        onClicked: {
                            taskList.model.append()
                        }
                    }
                }

            }
            AddProjectButton {
                Layout.alignment: Qt.AlignTop
                onClicked: {
                    projectList.model.append()
                }
            }
        }
    }
}