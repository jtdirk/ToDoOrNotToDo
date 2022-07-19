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
        anchors.fill: parent
        ListView {
            id: theBigList
            orientation: ListView.Horizontal
            anchors.fill: parent
            spacing: MyStyle.element.margins

            model: ProjectListModel {}
            delegate: projectList

            Component {
                id: projectList
                ListView {
                    id: taskList
                    
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    width: MyStyle.element.width

                    header: Project {
                        text: display
                        onTextChanged: model.edit = text
                    }

                    model: tasks
                    delegate: Task {
                        text: display
                        onTextChanged: model.edit = text
                    }

                    footer: AddTaskButton {}
                }
            }
        }
    }
}