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
        RowLayout {
            anchors.fill: parent

            Repeater {
                model: ProjectListModel {}
                delegate: Column {
                    id: taskList
                    
                    Layout.alignment: Qt.AlignTop

                    Project {
                        implicitHeight: MyStyle.element.height
                        text: display
                        onTextChanged: model.edit = text
                    }

                    ListView {
                        model: tasks
                        delegate: Task {
                            implicitHeight: MyStyle.element.height
                            text: display
                            onTextChanged: model.edit = text
                        }
                    }

                    AddTaskButton {
                        onClicked: tasks.append("")
                    }

                }
            }

            AddProjectButton {
                Layout.alignment: Qt.AlignTop
            }

        }
    }
}