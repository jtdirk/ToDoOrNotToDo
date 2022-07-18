import QtQuick
import QtQuick.Controls

ListView {
    id: projectList
    //anchors.fill:parent

    property alias projectText: project.text
    //property alias taskListModel: listViewTasks.model

    Project {
        id: project
    }
/*
    ListView {
        id: listViewTasks

        delegate: Task {
            text: tasks
        }
    }
    */
}