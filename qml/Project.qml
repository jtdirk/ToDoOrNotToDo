import QtQuick

Element {
    id: project
    border.color: MyStyle.project.color
    border.width: MyStyle.project.border.width
    textBold: true
    textSize: MyStyle.project.textSize
    textCenter: Text.AlignHCenter
    isCompletable: false

    dragTarget: taskList
    dragAxis: Drag.XAndYAxis 
    dragMinimumX: 0
    dragMaximumX: flow.width
    dragMinimumY: 0
    dragMaximumY: flow.height

//    states: [
//        State {
//            when: dragActive
//            AnchorChanges {
//                target: project
//                anchors.left: undefined
//                anchors.right: undefined
//            }
//        }
//    ]
}