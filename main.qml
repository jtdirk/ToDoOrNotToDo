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
            Repeater {
                id: projectList

                anchors.fill: parent
                
                model: ProjectListModel {}
                delegate: Column {
                    id: column

                    Project {
                        id: project
                        
                        text: display
                        onTextChanged: model.edit = text
                    }
                    Repeater {
                        id: taskList
                        model: tasks
                        delegate: Task {
                            text: display
                            onTextChanged: model.edit = text
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
                }
            }
        }
    }
}