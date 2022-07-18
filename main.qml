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

            Component {
                id: projectList
                ListView {
                    id: taskList
                    
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    width: 100

                    header: Project {
                        text: project
                    }
                    
                    model: tasks
                    delegate: Task {
                        text: taskText
                    }

                    footer: AddTaskButton {}
                }
            }
            model: ProjectListModel {}
            delegate: projectList
        }
    }
}