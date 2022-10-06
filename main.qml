import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import "./"
import ProjectListModel
import PropertiesModel

ApplicationWindow {
    id: windowMainWindow
    width: 640
    height: 480
    visible: true
    title: qsTr("ToDoOrNotToDo")

    PropertiesModel {
        id: pm
    }

    header: ToolBar {
        RowLayout {
            ToolButton {
                id: undoButton
                text: "untu"
                //enabled: projectListModel.isUndoAvailable
                onClicked: projectListModel.undo()
            }
            ToolButton {
                text: "nochmal"
                //enabled: windowMainWindow.isUndoAvailable
                onClicked: projectListModel.redo()
            }
                Text {
        text: pm.name
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

                model: ProjectListModel {
                    id: projectListModel
                }
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
                            completionDateText: completionDate
                            isTaskCompleted: isCompleted
                            onTextChanged: model.edit = text
                            onClose: taskList.model.remove(index)
                            onComplete: taskList.model.toggleCompletion(index)
                            onCreationDateChanged: model.creationDateChanged = creationDateText
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
                    //scrollView.ScrollBar.vertical.position = 1
                }
            }
        }
    }
}