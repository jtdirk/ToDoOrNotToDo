import QtQuick
import QtQuick.Controls

Rectangle {
    id: element

    width: MyStyle.element.width
    radius: MyStyle.element.radius
    anchors.margins: MyStyle.element.margins

    implicitHeight: mouseArea.implicitHeight

    property alias text: elementText.text
    property alias textColor: elementText.color
    property alias textBold: elementText.font.bold
    property alias textSize: elementText.font.pointSize
    property alias textCenter: elementText.horizontalAlignment
    property bool creationDateVisible: false
    property alias creationDateText: creationDate.text
    property bool isClosable: true

    signal close
    
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
        implicitHeight: {
            if(creationDateVisible)
            {
                creationDate.implicitHeight + elementText.implicitHeight + 2 * MyStyle.element.margins
            } else {
                elementText.implicitHeight + 2 * MyStyle.element.margins
            }
        }

        hoverEnabled: true
        preventStealing: true
        
        TextArea {
            id: elementText

            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.margins: MyStyle.element.margins

            hoverEnabled: true

            //verticalAlignment: Text.AlignVCenter
            wrapMode: Text.Wrap
            clip: true
        }
        TextInput {
            id: creationDate

            anchors.top: elementText.bottom
            anchors.left: parent.left
            anchors.leftMargin: MyStyle.element.margins
            font.pointSize: elementText.font.pointSize - 2

            visible: creationDateVisible
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

        onClicked: element.close()
    }
}