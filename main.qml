import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import "./"
import BaseModel

Window {
    id: windowMainWindow
    width: 640
    height: 480
    visible: true
    title: qsTr("ToDoOrNotToDo")

    Component {
        id: taskDelegate
        Task {
            text: display
        }
    }

    Component {
        id: projectHeader

        Project {
            text: "Projekt A"
        }
    }

    Component {
        id: projectFooter
        AddTaskButton {}
    }

    TableView {
        anchors.fill: parent
        anchors.margins: 5
        clip: true

        model: BaseModel {}
        delegate: Task {
            text: tasktext
        }
        //header: projectHeader
        //footer: projectFooter
    }
}