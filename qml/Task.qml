import QtQuick

Element {
    id: task
    border.color: MyStyle.task.color
    border.width: MyStyle.task.border.width
    textSize: MyStyle.task.textSize
    textColor: MyStyle.task.color
    creationDateVisible: true
    dueDateVisible: true

    dragTarget: dropArea
    dragAxis: Drag.YAxis
    dragMinimumY: 0
    dragMaximumY: taskList.contentItem.height - headerItem.height - footerItem.height - task.height
}