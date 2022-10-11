import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import "."
import ProjectListModel

ApplicationWindow {
    id: windowMainWindow
    width: 640
    height: 480
    visible: true
    color: MyStyle.general.color
    title: "ToDoOrNotToDo"
    Binding on title {
        when: projectListModel.unsavedChanges
        value: "ToDoOrNotToDo *"
    }

    Component.onCompleted: projectListModel.saveData()
    onClosing: projectListModel.saveData()

    ProjectListModel {
        id: projectListModel
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
                icon.source: "redo.svg"
                enabled: projectListModel.isRedoAvailable
                onClicked: projectListModel.redo()
            }
        }
    }

    footer: ToolBar {
        RowLayout {
            anchors.fill: parent
            Slider {
                Layout.alignment: Qt.AlignRight
                from: 4
                value: 10
                to: 50
                onMoved: MyStyle.general.scale = value / 10
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