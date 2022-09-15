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

        contentWidth: availableWidth

        Flow{
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
                        onComplete: projectListModel.completeProject(index, new Date().toLocaleDateString(Qt.locale("de_DE"), "dd.MM.yyyy"))
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
                            onClose: tasks.remove(index)
                            onComplete: tasks.completeTask(index, new Date().toLocaleDateString(Qt.locale("de_DE"), "dd.MM.yyyy"))
                            onCreationDateChanged: model.creationDateChanged = creationDateText;
                            onCompletionDateChanged: model.completionDateChanged = completionDateText
                        }
                    }

                    AddTaskButton {
                        id: addTaskButton
                        onClicked: {
                            tasks.append()
                        }
                    }
                }

            }
            AddProjectButton {
                Layout.alignment: Qt.AlignTop
                onClicked: {
                    projectList.model.append()
                    scrollView.ScrollBar.vertical.position = 1
                }
            }
        }
    }
}