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
/*
    ListModel {
        id: projectA
        ListElement { taskText: "nichts tun"}
        ListElement { taskText: "diskutieren"}
        ListElement { taskText: "beschuldigen"}
        ListElement { taskText: "leugnen"}
    }
*/
    Component {
        id: taskDelegate
        Task {
            text: taskText;
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

        model: BaseModel
        delegate: taskDelegate
        //header: projectHeader
        //footer: projectFooter
    }
}