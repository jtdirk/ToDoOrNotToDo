import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import "./"
import ProjectListModel

Window {
    id: windowMainWindow
    width: 640
    height: 480
    visible: true
    title: qsTr("ToDoOrNotToDo")

    ScrollView {
        id: scrollView

        anchors.fill: parent
        Row{
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
                            onTextChanged: model.edit = text
                            onClose: tasks.remove(index)
                        }
                    }

                    AddTaskButton {
                        id: addTaskButton
                        onClicked: {
                            tasks.append("neuer Task")
                        }
                    }
                }

            }
            AddProjectButton {
                Layout.alignment: Qt.AlignTop
                onClicked: {
                    projectList.model.append("neues Projekt")
                    scrollView.ScrollBar.horizontal.position = 1
                }
            }
        }
    }
}