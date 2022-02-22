import QtQuick
import QtQuick.Controls

Rectangle {
    id: element

    width: MyStyle.element.width
    height: MyStyle.element.height
    radius: MyStyle.element.radius
    anchors.margins: MyStyle.element.margins

    property alias text: elementText.text
    property alias textColor: elementText.color
    property alias textBold: elementText.font.bold
    property alias textSize: elementText.font.pointSize
    property alias textCenter: elementText.horizontalAlignment
    property bool isClosable: true

    property bool hovered: {
        if((mouseArea.containsMouse || elementText.hovered || closeButton.hovered) && isClosable)
        {
            true
        } else
        {
            false
        }
    }

    MouseArea {
        id: mouseArea

        anchors.fill: parent

        hoverEnabled: true
        preventStealing: true
        
        TextArea {
            id: elementText

            anchors.fill: parent
            
            hoverEnabled: true

            verticalAlignment: Text.AlignVCenter
            wrapMode: Text.WordWrap
            anchors.margins: 5
            clip: true
        }
    }
    RoundButton {
        id: closeButton

        width: 20
        height: 20
        radius: 10
        text: "X"
        anchors.top: parent.top
        anchors.right: parent.right

        visible: element.hovered

        HoverHandler {
        }
    }
}