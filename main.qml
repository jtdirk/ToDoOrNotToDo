import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import "./"
import ProjectListModel
import TodoTXTModel

Window {
    id: windowMainWindow
    width: 640
    height: 480
    visible: true
    title: qsTr("ToDoOrNotToDo")

/* so geht's irgendwie nicht
    ScrollView {
        id: scrollView

        anchors.fill: parent
        Row {
            anchors.fill: parent
            Repeater {
                model: TodoTXTModel {
                    id: todoTXTModel
                }
                delegate: Column {
                    
                    Project {
                        text: project
                    }
                    Repeater {
                        model: todoTXTModel
                        delegate: Task {
                            text: display
                        }
                    }
                }
            }
        }
    }
*/

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
                            creationDateText: creationDate
                            completionDateText: completionDate
                            isTaskCompleted: isCompleted
                            onTextChanged: model.edit = text
                            onClose: tasks.remove(index)
                            onComplete: tasks.complete(index, new Date().toLocaleDateString(Qt.locale("de_DE"), "dd.MM.yyyy"))
                            onCreationDateChanged: model.creationDateChanged = creationDateText;
                            onCompletionDateChanged: model.completionDateChanged = completionDateText
                        }
                    }

                    AddTaskButton {
                        id: addTaskButton
                        onClicked: {
                            tasks.append("neuer Task", new Date().toLocaleDateString(Qt.locale("de_DE"), "dd.MM.yyyy"), "01.01.0001", false);
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