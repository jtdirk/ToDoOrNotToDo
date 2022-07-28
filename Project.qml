import QtQuick

Element {
    border.color: MyStyle.project.color
    border.width: MyStyle.project.border.width
    textBold: true
    textSize: MyStyle.project.textSize
    textCenter: Text.AlignHCenter
    isCompletable: false
}