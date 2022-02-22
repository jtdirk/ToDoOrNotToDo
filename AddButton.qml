import QtQuick
import QtQuick.Controls

Element {
    id: element

    property color textColor: "black"
    property int borderWidth: 1
    property alias textBold: button.font.bold
    property alias textSize: button.font.pointSize
    isClosable: false

    Button {
        id: button

        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.top: parent.TopToBottom
        anchors.margins: 5
        display: AbstractButton.TextOnly

        width: height

        contentItem: Text {
            text: "+"
            font: button.font
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: element.textColor
        }

        background: Rectangle {
            border.width: element.borderWidth
            border.color: element.textColor
            radius: button.height / 2
        }
    }
}