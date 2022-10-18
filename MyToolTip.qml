import QtQuick
import QtQuick.Controls

ToolTip {
    delay: 1000
    visible: parent.hovered

    background: Rectangle {
        color: "white"
        border.color: "black"
    }
}
