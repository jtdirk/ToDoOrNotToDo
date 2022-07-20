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
        
        ListView {
            id: projectList

            orientation: ListView.Horizontal
            anchors.fill: parent

            spacing: MyStyle.element.margins

            model: ProjectListModel {}
            delegate: ListView {
                id: taskList
                    
                width: MyStyle.element.width

                model: tasks
                delegate: Task {
                    text: display
                    onTextChanged: model.edit = text
                }

                header: Project {
                    text: display
                    onTextChanged: model.edit = text
                }

                footer: AddTaskButton {
                        onClicked: tasks.append("")
                }
            }
/*
            AddProjectButton {
                Layout.alignment: Qt.AlignTop
            }
*/
        }
    }
}