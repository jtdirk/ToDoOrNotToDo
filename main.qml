import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Dialogs
import "."
import ProjectListModel

ApplicationWindow {
    id: windowMainWindow
    width: 640
    height: 480
    visible: true
    color: MyStyle.general.color

    property string titleText: "ToDoOrNotToDo"
    title: titleText
    Binding on title {
        when: projectListModel.unsavedChanges
        value: titleText + " *"
    }

    Component.onCompleted: projectListModel.saveData()

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
        close.accepted = false
        windowMainWindow.hide()
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
                icon.source: "undo.svg"
                enabled: projectListModel.isUndoAvailable
                onClicked: projectListModel.undo()
            }
            ToolButton {
                id: redoButton
                icon.source: "redo.svg"
                enabled: projectListModel.isRedoAvailable
                onClicked: projectListModel.redo()
            }
            ToolButton {
                id: settingsButoon
                icon.source: "gear.svg"
                onClicked: settingsDialog.open()
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