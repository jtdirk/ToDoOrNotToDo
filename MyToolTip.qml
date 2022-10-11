import QtQuick
import QtQuick.Controls

ToolTip {
    text: "Enddatum"
    delay: 1000
    visible: parent.hovered

    background: Rectangle {
        color: "white"
        border.color: "black"
    }
}
